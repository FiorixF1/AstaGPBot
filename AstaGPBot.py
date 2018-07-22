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
insulti = ['pirla', 'scem', 'cretino', 'baccalà', 'pollo', 'baggiano', 'strunz', 'pagliaccio', 'scemo pagliaccio', 'aò', 'cafone']
admins = ["FiorixF1", "YuriVarrella", "F1News_Marcuss"]

asta_corrente = None
offerta_corrente = None

CANCELLAZIONE = False
BID_IN_PROGRESS = False



# Data structures
class Asta:
    def __init__(self):
        self.partecipanti = []      # nickname dei partecipanti
        self.saldo = dict()         # chiave = username, valore = saldo
        self.piloti = dict()        # chiave = username, valore = piloti
        
    def aggiungiPartecipante(self, nickname):
        if nickname not in self.partecipanti:
            self.partecipanti.append(nickname)
            self.saldo[nickname] = 300
            self.piloti[nickname] = []
            
    def rimuoviPartecipante(self, nickname):
        if nickname in self.partecipanti:
            self.partecipanti.remove(nickname)
            del self.saldo[nickname]
            del self.piloti[nickname]
        
    def ottieniSaldo(self, nickname):
        if nickname in self.partecipanti:
            return self.saldo[nickname]
        else:
            return None
            
    def ottieniPiloti(self, nickname):
        if nickname in self.partecipanti:
            return self.piloti[nickname]
        else:
            return None
            
    def prelevaSaldo(self, nickname, prelievo):
        if nickname in self.partecipanti:
            if self.saldo[nickname] >= prelievo:
                self.saldo[nickname] -= prelievo
                
    def contaPiloti(self, nickname):
        if nickname in self.partecipanti:
            return len(self.piloti[nickname])
        return 0
    
    def aggiungiPilota(self, nickname, pilota):
        if nickname in self.partecipanti:
            if pilota not in self.piloti[nickname]:
                self.piloti[nickname].append(pilota)

class Offerta:
    def __init__(self, pilota):
        self.pilota = pilota
        self.partecipante = None
        self.offerta = 0
        
class BidThread(threading.Thread):
    def __init__(self, update):
        threading.Thread.__init__(self)
        self.update = update
    def run(self):
        global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
        time.sleep(115)
        self.update.message.reply_text("5")
        time.sleep(1)
        self.update.message.reply_text("4")
        time.sleep(1)
        self.update.message.reply_text("3")
        time.sleep(1)
        self.update.message.reply_text("2")
        time.sleep(1)
        self.update.message.reply_text("1")
        time.sleep(1)
        
        BID_IN_PROGRESS = False
        if offerta_corrente.partecipante != None:
            asta_corrente.aggiungiPilota(offerta_corrente.partecipante, offerta_corrente.pilota)
            asta_corrente.prelevaSaldo(offerta_corrente.partecipante, offerta_corrente.offerta)
            self.update.message.reply_text(offerta_corrente.pilota + " assegnato a " + offerta_corrente.partecipante + " per " + str(offerta_corrente.offerta) + " fantamilioni")
        else:
            self.update.message.reply_text("Nessuno ha comprato " + offerta_corrente.pilota)
        offerta_corrente = None


        
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

# Funzioni per soli amministratori
def aggiungi_admin(bot, update, args):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins:
        return
    if args[0] not in admins:
        admins.append(args[0])
        update.message.reply_text('Utente ' + args[0] + ' aggiunto come amministratore')
    else:
        update.message.reply_text(args[0] + ' è già amministratore')
        
def rimuovi_admin(bot, update, args):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins:
        return
    if args[0] in admins:
        if args[0] == update.message.from_user.username:
            update.message.reply_text('Non puoi rimuovere te stesso dagli amministratori, ' + random.choice(insulti) + '!')
        elif args[0] == "FiorixF1":
            update.message.reply_text('Non puoi rimuovere gli admin supremi!')
        else:
            admins.remove(args[0])
            update.message.reply_text('Utente ' + args[0] + ' rimosso dagli amministratori')

def aggiungi_partecipante(bot, update, args):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins:
        return
    if asta_corrente != None:
        if args[0] not in asta_corrente.partecipanti and not CANCELLAZIONE and not BID_IN_PROGRESS:
            asta_corrente.aggiungiPartecipante(args[0])
            update.message.reply_text('Utente ' + args[0] + ' aggiunto ai partecipanti')
    else:
        update.message.reply_text("Nessuna asta attiva")
            
def rimuovi_partecipante(bot, update, args):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins:
        return
    if asta_corrente != None:
        if args[0] in asta_corrente.partecipanti and not CANCELLAZIONE and not BID_IN_PROGRESS:
            asta_corrente.rimuoviPartecipante(args[0])
            update.message.reply_text('Utente ' + args[0] + ' rimosso dai partecipanti')
    else:
        update.message.reply_text("Nessuna asta attiva")
        
def crea_asta(bot, update):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins:
        return
    if asta_corrente == None:
        if not CANCELLAZIONE and not BID_IN_PROGRESS:
            asta_corrente = Asta()
            update.message.reply_text("Asta creata, ricorda di aggiungere i partecipanti!")
    else:
        update.message.reply_text("E' necessario cancellare l'asta esistente per crearne una nuova")

def cancella_asta(bot, update):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if BID_IN_PROGRESS or update.message.from_user.username not in admins:
        return
    if asta_corrente != None:
        CANCELLAZIONE = True
        update.message.reply_text("Sei sicuro di voler cancellare l'asta [s/n]? Perderai tutte le informazioni!")
    else:
        update.message.reply_text("Non ci sono aste attive")
   
def cancella_definitivamente(bot, update):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if not CANCELLAZIONE or BID_IN_PROGRESS or update.message.from_user.username not in admins:
        return
    if update.message.text.lower() == "s":
        asta_corrente = None
        CANCELLAZIONE = False
        update.message.reply_text("Asta cancellata")
    elif update.message.text.lower() == "n":
        CANCELLAZIONE = False
        update.message.reply_text("Cancellazione annullata")
        
def avvia_offerta(bot, update, args):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if update.message.from_user.username not in admins:
        return
    if asta_corrente != None:
        if not BID_IN_PROGRESS and not CANCELLAZIONE:
            BID_IN_PROGRESS = True
            offerta_corrente = Offerta(args[0])
            thread = BidThread(update)
            thread.start()
            update.message.reply_text("Asta avviata per " + args[0] + ": l'offerta scade fra 2 minuti")
    else:
        update.message.reply_text("Nessuna asta attiva")
        
# Funzioni per soli partecipanti
def bid(bot, update, args):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if asta_corrente != None and BID_IN_PROGRESS:
        if update.message.from_user.username not in asta_corrente.partecipanti:
            return
        try:
            bid = int(args[0])
            if bid <= asta_corrente.ottieniSaldo(update.message.from_user.username) and bid > offerta_corrente.offerta and asta_corrente.contaPiloti(update.message.from_user.username) < 2:
                offerta_corrente.partecipante = update.message.from_user.username
                offerta_corrente.offerta = bid
        except:
            return

# Funzioni per tutti
def mostra_admin(bot, update):
    ans = "Admin del bot:"
    for admin in admins:
        ans += "\n" + admin
    update.message.reply_text(ans)

def mostra_saldo(bot, update):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if asta_corrente != None:
        ans = "Saldo dei partecipanti:"
        saldi = []
        for partecipante in asta_corrente.partecipanti:
            saldi.append((asta_corrente.ottieniSaldo(partecipante), partecipante))
        saldi.sort()
        for s in saldi:
            ans += "\n" + s[1] + "\t" + str(s[0]) + " fantamilioni"
        update.message.reply_text(ans)
            
def mostra_piloti_assegnati(bot, update):
    global asta_corrente, offerta_corrente, CANCELLAZIONE, BID_IN_PROGRESS
    if asta_corrente != None:
        ans = "Piloti assegnati:"
        for partecipante in asta_corrente.partecipanti:
            ans += "\n" + partecipante + "\t" + ' - '.join(asta_corrente.ottieniPiloti(partecipante))
        update.message.reply_text(ans)



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
    dp.add_handler(CommandHandler("aggiungipartecipante", aggiungi_partecipante, pass_args=True))
    dp.add_handler(CommandHandler("rimuovipartecipante", rimuovi_partecipante, pass_args=True))
    dp.add_handler(CommandHandler("creaasta", crea_asta))
    dp.add_handler(CommandHandler("avviaofferta", avvia_offerta, pass_args=True))
    dp.add_handler(CommandHandler("cancellaasta", cancella_asta))
    dp.add_handler(CommandHandler("b", bid, pass_args=True))
    dp.add_handler(CommandHandler("mostraadmin", mostra_admin))
    dp.add_handler(CommandHandler("mostrasaldo", mostra_saldo))
    dp.add_handler(CommandHandler("mostrapilotiassegnati", mostra_piloti_assegnati))

    # on noncommand i.e message 
    dp.add_handler(MessageHandler(Filters.text, cancella_definitivamente))
    
    # on unknown command - notify user
    #dp.add_handler(MessageHandler(Filters.command, unknown))
    
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