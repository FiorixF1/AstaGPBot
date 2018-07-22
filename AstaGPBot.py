from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import threading
import random
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



# State global variables
insulti = ['pirla', 'scem', 'cretino', 'baccalà', 'pollo', 'baggiano', 'strunz', 'pagliaccio', 'scemo pagliaccio', 'aò', 'cafone', 'burino', 'beduino']
admin_supremi = ["FiorixF1", "F1News_Marcuss"]
admins = ["FiorixF1", "YuriVarrella", "F1News_Marcuss"]

CANCELLAZIONE = False
BID_IN_PROGRESS = False



# Data structures
class Asta:
    def __init__(self):
        self.partecipanti = []      # username dei partecipanti
        self.saldo = dict()         # chiave = username, valore = saldo (intero)
        self.piloti = dict()        # chiave = username, valore = piloti (lista di stringhe)
        
    def reset(self):
        self.partecipanti = []
        self.saldo = dict()
        self.piloti = dict()
        
    def aggiungiPartecipante(self, username):
        if username not in self.partecipanti:
            self.partecipanti.append(username)
            self.saldo[username] = 300
            self.piloti[username] = []
            
    def rimuoviPartecipante(self, username):
        if username in self.partecipanti:
            self.partecipanti.remove(username)
            del self.saldo[username]
            del self.piloti[username]
        
    def ottieniSaldo(self, username):
        if username in self.partecipanti:
            return self.saldo[username]
        else:
            return None
            
    def ottieniPiloti(self, username):
        if username in self.partecipanti:
            return self.piloti[username]
        else:
            return None
            
    def prelevaSaldo(self, username, prelievo):
        if username in self.partecipanti:
            if self.saldo[username] >= prelievo:
                self.saldo[username] -= prelievo
                
    def contaPiloti(self, username):
        if username in self.partecipanti:
            return len(self.piloti[username])
        return 0
    
    def aggiungiPilota(self, username, pilota):
        if username in self.partecipanti:
            if pilota not in self.piloti[username]:
                self.piloti[username].append(pilota)

class Offerta:
    def __init__(self, pilota):
        self.pilota = pilota
        self.partecipante = None
        self.offerta = 0
        
class BidThread(threading.Thread):
    def __init__(self, update):
        threading.Thread.__init__(self)
        self.update = update
        self.STOP = False
        
    def run(self):
        global asta_corrente, offerta_corrente, BID_IN_PROGRESS
        
        time.sleep(90)
        if self.STOP: return
        self.update.message.reply_text("30 secondi")
        
        time.sleep(25)
        if self.STOP: return
        self.update.message.reply_text("5")
        
        time.sleep(1)
        if self.STOP: return
        self.update.message.reply_text("4")
        
        time.sleep(1)
        if self.STOP: return
        self.update.message.reply_text("3")
        
        time.sleep(1)
        if self.STOP: return
        self.update.message.reply_text("2")
        
        time.sleep(1)
        if self.STOP: return
        self.update.message.reply_text("1")
        
        time.sleep(1)
        if self.STOP: return
        
        BID_IN_PROGRESS = False
        if offerta_corrente.partecipante != None:
            asta_corrente.aggiungiPilota(offerta_corrente.partecipante, offerta_corrente.pilota)
            asta_corrente.prelevaSaldo(offerta_corrente.partecipante, offerta_corrente.offerta)
            self.update.message.reply_text(offerta_corrente.pilota + " assegnato a " + offerta_corrente.partecipante + " per " + str(offerta_corrente.offerta) + " fantamilioni")
        else:
            self.update.message.reply_text("Nessuno ha comprato " + offerta_corrente.pilota)
        offerta_corrente = None
        
    def stop(self):
        self.STOP = True

asta_corrente = Asta()
offerta_corrente = None
bid_thread = None


        
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def aggiungi_admin(bot, update, args):
    if update.message.from_user.username not in admins:
        return
    if len(args) == 0:
        update.message.reply_text("Uso: /aggiungiadmin @admin1 @admin2...")
        return
    for arg in args:
        if arg[0] == "@" and len(arg) > 1:
            arg = arg[1:]
        if arg not in admins:
            admins.append(arg)
            update.message.reply_text('Utente ' + arg + ' aggiunto come amministratore')
        else:
            update.message.reply_text(arg + ' è già amministratore')
        
def rimuovi_admin(bot, update, args):
    if update.message.from_user.username not in admins:
        return
    if len(args) == 0:
        update.message.reply_text("Uso: /rimuoviadmin @admin1 @admin2...")
        return
    for arg in args:
        if arg[0] == "@" and len(arg) > 1:
            arg = arg[1:]
        if arg in admins:
            if arg == update.message.from_user.username:
                update.message.reply_text('Non puoi rimuovere te stesso dagli amministratori, ' + random.choice(insulti) + '!')
            elif arg in admin_supremi:
                update.message.reply_text('Non puoi rimuovere gli admin supremi!')
            else:
                admins.remove(arg)
                update.message.reply_text('Utente ' + arg + ' rimosso dagli amministratori')

def aggiungi_partecipanti(bot, update, args):
    global asta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins or CANCELLAZIONE or BID_IN_PROGRESS:
        return
    if len(args) == 0:
        update.message.reply_text("Uso: /aggiungipartecipanti @user1 @user2...")
        return
    for arg in args:
        if arg[0] == "@" and len(arg) > 1:
            arg = arg[1:]
        if arg not in asta_corrente.partecipanti:
            asta_corrente.aggiungiPartecipante(arg)
            update.message.reply_text('Utente ' + arg + ' aggiunto ai partecipanti')
            
def rimuovi_partecipanti(bot, update, args):
    global asta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins or CANCELLAZIONE or BID_IN_PROGRESS:
        return
    if len(args) == 0:
        update.message.reply_text("Uso: /rimuovipartecipanti @user1 @user2...")
        return
    for arg in args:
        if arg[0] == "@" and len(arg) > 1:
            arg = arg[1:]
        if arg in asta_corrente.partecipanti:
            asta_corrente.rimuoviPartecipante(arg)
            update.message.reply_text('Utente ' + arg + ' rimosso dai partecipanti')
        
def reset(bot, update):
    global CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins or CANCELLAZIONE or BID_IN_PROGRESS:
        return
    CANCELLAZIONE = True
    update.message.reply_text("Sei sicuro di voler resettare l'asta [s/n]? Perderai tutte le informazioni!")
    
def avvia_offerta(bot, update, args):
    global offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS, bid_thread
    if update.message.from_user.username not in admins or CANCELLAZIONE or BID_IN_PROGRESS:
        return
    if len(args) == 0:
        update.message.reply_text("Uso: /avviaofferta pilota")
        return
    BID_IN_PROGRESS = True
    offerta_corrente = Offerta(args[0])
    bid_thread = BidThread(update)
    bid_thread.start()
    update.message.reply_text("Asta avviata per " + args[0] + ": l'offerta scade fra 2 minuti")
        
def ferma_offerta(bot, update):
    global offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS, bid_thread
    if update.message.from_user.username not in admins:
        return
    if BID_IN_PROGRESS and not CANCELLAZIONE:
        BID_IN_PROGRESS = False
        bid_thread.stop()
        bid_thread = None
        offerta_corrente = None
        update.message.reply_text("Asta annullata!")
        
def mostra_admin(bot, update):
    if update.message.from_user.username not in admins:
        return
    ans = "Admin del bot:"
    for admin in admins:
        ans += "\n" + admin
    update.message.reply_text(ans)

def mostra_saldo(bot, update):
    global asta_corrente
    if update.message.from_user.username not in admins:
        return
    ans = "Saldo dei partecipanti:"
    saldi = []
    for partecipante in asta_corrente.partecipanti:
        saldi.append((asta_corrente.ottieniSaldo(partecipante), partecipante))
    saldi.sort()
    saldi.reverse()
    for s in saldi:
        ans += "\n" + s[1] + "\t" + str(s[0]) + " fantamilioni"
    update.message.reply_text(ans)
            
def mostra_piloti_assegnati(bot, update):
    global asta_corrente
    if update.message.from_user.username not in admins:
        return
    ans = "Piloti assegnati:"
    for partecipante in asta_corrente.partecipanti:
        ans += "\n" + partecipante + "\t" + ' - '.join(asta_corrente.ottieniPiloti(partecipante))
    update.message.reply_text(ans)

def controllore_di_stato(bot, update):
    # questa funzione controlla:
    # - il reset dell'asta se siamo nello stato di CANCELLAZIONE
    # - le offerte fatte se siamo nello stato di BID_IN_PROGRESS
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    
    if CANCELLAZIONE and not BID_IN_PROGRESS and update.message.from_user.username in admins:
        if update.message.text.lower() == "s":
            asta_corrente.reset()
            CANCELLAZIONE = False
            update.message.reply_text("Asta resettata")
        elif update.message.text.lower() == "n":
            CANCELLAZIONE = False
            update.message.reply_text("Reset annullato")    
    elif BID_IN_PROGRESS and not CANCELLAZIONE and update.message.from_user.username in asta_corrente.partecipanti:
        try:
            bid = int(update.message.text)
            if bid > asta_corrente.ottieniSaldo(update.message.from_user.username):
                update.message.reply_text(update.message.from_user.username + ", non hai abbastanza soldi!")
                return
            if asta_corrente.contaPiloti(update.message.from_user.username) == 2:
                update.message.reply_text(update.message.from_user.username + ", hai già due piloti!")
                return
            if bid > offerta_corrente.offerta:
                offerta_corrente.partecipante = update.message.from_user.username
                offerta_corrente.offerta = bid
        except:
            return    



def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


    

def main():
    """Start the bot"""
    # Create the EventHandler and pass it your bot's token
    updater = Updater("439586411:AAEDLt76-KiDgmYeqKnRD98vJUxWdjy9DjM")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("aggiungiadmin", aggiungi_admin, pass_args=True))
    dp.add_handler(CommandHandler("rimuoviadmin", rimuovi_admin, pass_args=True))
    dp.add_handler(CommandHandler("aggiungipartecipanti", aggiungi_partecipanti, pass_args=True))
    dp.add_handler(CommandHandler("rimuovipartecipanti", rimuovi_partecipanti, pass_args=True))
    dp.add_handler(CommandHandler("avviaofferta", avvia_offerta, pass_args=True))
    dp.add_handler(CommandHandler("fermaofferta", ferma_offerta))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("mostraadmin", mostra_admin))
    dp.add_handler(CommandHandler("mostrasaldo", mostra_saldo))
    dp.add_handler(CommandHandler("mostrapilotiassegnati", mostra_piloti_assegnati))

    # on noncommand i.e message 
    dp.add_handler(MessageHandler(Filters.text, controllore_di_stato))
    
    # on unknown command - notify user
    # dp.add_handler(MessageHandler(Filters.command, unknown))
    
    # log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()