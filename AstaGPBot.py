from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functools import wraps
from time import sleep
import logging
import threading
import pickle
import random

# Abilita log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



""" Costanti """
BOT_TOKEN = "439586411:AAEDLt76-KiDgmYeqKnRD98vJUxWdjy9DjM"
FIORIXF1 = 289439604
F1NEWS_MARCUSS = 163233837
ADMIN_SUPREMI = [FIORIXF1, F1NEWS_MARCUSS]
INSULTI = ['pirla', 'scem', 'cretino', 'baccalà', 'pollo', 'baggiano', 'strunz', 'pagliaccio', 'scemo pagliaccio', 'aò', 'cafone', 'burino', 'beduino', 'mona', 'lota']
IDLE, RESET, BIP = (0, 1, 2)
BID_DURATION = 120



""" Variabili di stato globali """
ADMINS = [FIORIXF1, F1NEWS_MARCUSS]
ADMINS_USERNAME = { FIORIXF1: "FiorixF1",
                    F1NEWS_MARCUSS: "F1News_Marcuss"
                  }
CHAT_IDS = []       # lista di identificatori delle chat attive
CHATS = dict()      # chiave = id, valore = chat (oggetto)



""" Strutture dati """
class Chat:
    def __init__(self):
        self.state_handler = StateHandler()
        self.asta = Asta()
        self.ultima_offerta = None
        self.bid_thread = None    
    
class StateHandler:
    def __init__(self):
        self._state = IDLE
        
    def setState(self, state):
        self._state = state
        
    def getState(self):
        return self._state

class Asta:
    def __init__(self):
        self.partecipanti = []      # id dei partecipanti
        self.username = dict()      # chiave = id, valore = username (stringa)
        self.saldo = dict()         # chiave = id, valore = saldo (intero)
        self.piloti = dict()        # chiave = id, valore = piloti (lista di stringhe)
        
    def reset(self):
        self.partecipanti = []
        self.username = dict()
        self.saldo = dict()
        self.piloti = dict()
        
    def aggiungiPartecipante(self, user):
        if user.id not in self.partecipanti:
            self.partecipanti.append(user.id)
            self.username[user.id] = user.username
            self.saldo[user.id] = 300
            self.piloti[user.id] = []
            
    def rimuoviPartecipante(self, user):
        if user.id in self.partecipanti:
            self.partecipanti.remove(user.id)
            del self.username[user.username]
            del self.saldo[user.id]
            del self.piloti[user.id]
        
    def getUsernameById(self, id):
        if id in self.username:
            return self.username[id]
        return None
        
    def ottieniSaldo(self, id):
        if id in self.partecipanti:
            return self.saldo[id]
        return None
            
    def ottieniPiloti(self, id):
        if id in self.partecipanti:
            return self.piloti[id]
        return None
            
    def prelevaSaldo(self, id, prelievo):
        if id in self.partecipanti:
            if self.saldo[id] >= prelievo:
                self.saldo[id] -= prelievo

    def aggiungiPilota(self, id, pilota):
        if id in self.partecipanti:
            if pilota not in self.piloti[id]:
                self.piloti[id].append(pilota)

    def contaPiloti(self, id):
        if id in self.partecipanti:
            return len(self.piloti[id])
        return None

class Offerta:
    def __init__(self, pilota):
        self.pilota = pilota        # stringa
        self.partecipante = None    # id
        self.offerta = 0            # intero
        
class BidThread(threading.Thread):
    def __init__(self, update, chat):
        threading.Thread.__init__(self)
        self.update = update        # per inviare messaggi
        self.chat = chat            # per accedere ai dati della chat
        self.STOP = False           # per fermare l'offerta
        
    def run(self):
        sleep(BID_DURATION-30)
        if self.STOP: return
        self.update.message.reply_text("30 secondi")
        
        sleep(25)
        if self.STOP: return
        self.update.message.reply_text("5")
        
        sleep(1)
        if self.STOP: return
        self.update.message.reply_text("4")
        
        sleep(1)
        if self.STOP: return
        self.update.message.reply_text("3")
        
        sleep(1)
        if self.STOP: return
        self.update.message.reply_text("2")
        
        sleep(1)
        if self.STOP: return
        self.update.message.reply_text("1")
        
        sleep(1)
        if self.STOP: return
        
        self.chat.state_handler.setState(IDLE)
        if self.chat.ultima_offerta.partecipante != None:
            self.chat.asta.aggiungiPilota(self.chat.ultima_offerta.partecipante, self.chat.ultima_offerta.pilota)
            self.chat.asta.prelevaSaldo(self.chat.ultima_offerta.partecipante, self.chat.ultima_offerta.offerta)
            self.update.message.reply_text(self.chat.ultima_offerta.pilota + " assegnato a " + self.chat.asta.getUsernameById(self.chat.ultima_offerta.partecipante) + " per " + str(self.chat.ultima_offerta.offerta) + " fantamilioni")
        else:
            self.update.message.reply_text("Nessuno ha comprato " + self.chat.ultima_offerta.pilota)
        self.chat.ultima_offerta = None
        self.chat.bid_thread = None
        
    def stop(self):
        self.STOP = True



""" Decoratori """
def restricted(f):
    @wraps(f)
    def wrapped(bot, update, *args, **kwargs):
        id = update.effective_user.id
        username = update.effective_user.username
        if id not in ADMINS:
            print("Unauthorized access denied for {} ({}).".format(id, username))
            return
        f(bot, update, *args, **kwargs)
    return wrapped

def chat_finder(f):
    @wraps(f)
    def wrapped(bot, update, *args, **kwargs):
        chat_id = update.message.chat_id
        try:
            chat = CHATS[chat_id]
        except:
            chat = Chat()
            CHAT_IDS.append(chat_id)
            CHATS[chat_id] = chat
        f(bot, update, chat, *args, **kwargs)
    return wrapped
    
def current_state(state):
    def decorator(f):
        @wraps(f)
        def wrapped(bot, update, chat, *args, **kwargs):
            if chat.state_handler.getState() == state:
                f(bot, update, chat, *args, **kwargs)
        return wrapped
    return decorator



""" Comandi """
@restricted
@chat_finder
@current_state(IDLE)
def aggiungi_admin(bot, update, chat):
    try:
        utente = update.message.reply_to_message.from_user
        if utente.id not in ADMINS:
            ADMINS.append(utente.id)
            ADMINS_USERNAME[utente.id] = utente.username
            bot.send_message(chat_id=update.message.chat_id, text="Utente " + utente.username + " aggiunto come amministratore.")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=utente.username + " è già amministratore.")
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Usa questo comando in risposta ad un messaggio.")
        
@restricted
@chat_finder
@current_state(IDLE)
def rimuovi_admin(bot, update, chat):
    try:
        utente = update.message.reply_to_message.from_user
        if utente.id in ADMINS:
            if utente.id == update.message.from_user.id:
                bot.send_message(chat_id=update.message.chat_id, text="Non puoi rimuovere te stesso dagli amministratori, " + random.choice(INSULTI) + "!")
            elif utente.id in ADMIN_SUPREMI:
                bot.send_message(chat_id=update.message.chat_id, text="Non puoi rimuovere gli admin supremi!")
            else:
                ADMINS.remove(utente.id)
                del ADMINS_USERNAME[utente.id]
                bot.send_message(chat_id=update.message.chat_id, text="Utente " + utente.username + " rimosso dagli amministratori.")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=utente.username + " non è un amministratore.")
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Usa questo comando in risposta ad un messaggio.")

@restricted
@chat_finder
@current_state(IDLE)
def aggiungi_partecipante(bot, update, chat):
    try:
        utente = update.message.reply_to_message.from_user
        if utente.id not in chat.asta.partecipanti:
            chat.asta.aggiungiPartecipante(utente)
            bot.send_message(chat_id=update.message.chat_id, text="Utente " + utente.username + " aggiunto ai partecipanti.")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=utente.username + " è già un partecipante.")
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Usa questo comando in risposta ad un messaggio.")

@restricted
@chat_finder
@current_state(IDLE)
def rimuovi_partecipante(bot, update, chat):
    try:
        utente = update.message.reply_to_message.from_user
        if utente.id in chat.asta.partecipanti:
            chat.asta.rimuoviPartecipante(utente)
            bot.send_message(chat_id=update.message.chat_id, text="Utente " + utente.username + " rimosso dai partecipanti.")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=utente.username + " non è un partecipante.")
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Usa questo comando in risposta ad un messaggio.")

@restricted
@chat_finder
@current_state(IDLE)
def reset(bot, update, chat):
    chat.state_handler.setState(RESET)
    bot.send_message(chat_id=update.message.chat_id, text="Sei sicuro di voler resettare l'asta [s/n]? Perderai tutte le informazioni!")

@restricted
@chat_finder
@current_state(IDLE)
def avvia_offerta(bot, update, chat, args):
    try:
        chat.ultima_offerta = Offerta(args[0])
        chat.bid_thread = BidThread(update, chat)
        chat.bid_thread.start()
        bot.send_message(chat_id=update.message.chat_id, text="Asta avviata per " + args[0] + ": l'offerta scade fra 2 minuti.")
        chat.state_handler.setState(BIP)
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Uso: /avviaofferta pilota")

@restricted
@chat_finder
@current_state(BIP)
def ferma_offerta(bot, update, chat):
    chat.state_handler.setState(IDLE)
    chat.bid_thread.stop()
    chat.bid_thread = None
    chat.ultima_offerta = None
    bot.send_message(chat_id=update.message.chat_id, text="Asta annullata!")

@restricted
@chat_finder
@current_state(IDLE)
def mostra_admin(bot, update, chat):
    ans = "Admin del bot:"
    for admin in ADMINS_USERNAME:
        ans += "\n" + ADMINS_USERNAME[admin]
    bot.send_message(chat_id=update.message.chat_id, text=ans)

@restricted
@chat_finder
@current_state(IDLE)
def mostra_saldo(bot, update, chat):
    ans = "Saldo dei partecipanti:"
    saldi = []
    for partecipante in chat.asta.partecipanti:
        saldi.append((chat.asta.ottieniSaldo(partecipante), partecipante))
    saldi.sort()
    saldi.reverse()
    for s in saldi:
        ans += "\n" + chat.asta.getUsernameById(s[1]) + "\t" + str(s[0]) + " fantamilioni"
    bot.send_message(chat_id=update.message.chat_id, text=ans)

@restricted
@chat_finder
@current_state(IDLE)
def mostra_piloti_assegnati(bot, update, chat):
    ans = "Piloti assegnati:"
    for partecipante in chat.asta.partecipanti:
        ans += "\n" + chat.asta.getUsernameById(partecipante) + "\t" + ' - '.join(chat.asta.ottieniPiloti(partecipante))
    bot.send_message(chat_id=update.message.chat_id, text=ans)

@restricted
@chat_finder
@current_state(IDLE)
def help(bot, update, chat):
    bot.send_message(chat_id=update.message.chat_id, text="Benvenuto! Questo è un bot che ti aiuterà nella gestione delle aste del FantaGP. Per maggiori informazioni sul suo funzionamento, visita https://github.com/FiorixF1/AstaGPBot")



""" Funzioni ausiliarie """
@chat_finder
def controllore_di_stato(bot, update, chat):
    # questa funzione controlla:
    # - il reset dell'asta se siamo nello stato di RESET
    # - le offerte fatte se siamo nello stato di BIP
    
    if chat.state_handler.getState() == RESET and update.message.from_user.id in ADMINS:
        if update.message.text.lower() == "s":
            chat.asta.reset()
            chat.state_handler.setState(IDLE)
            bot.send_message(chat_id=update.message.chat_id, text="Asta resettata")
        elif update.message.text.lower() == "n":
            chat.state_handler.setState(IDLE)
            bot.send_message(chat_id=update.message.chat_id, text="Reset annullato")    
    elif chat.state_handler.getState() == BIP and update.message.from_user.id in chat.asta.partecipanti:
        try:
            bid = int(update.message.text)
            if bid > chat.asta.ottieniSaldo(update.message.from_user.id):
                update.message.reply_text(update.message.from_user.username + ", non hai abbastanza soldi!")
                return
            if chat.asta.contaPiloti(update.message.from_user.id) == 2:
                update.message.reply_text(update.message.from_user.username + ", hai già due piloti!")
                return
            if bid > chat.ultima_offerta.offerta:
                chat.ultima_offerta.partecipante = update.message.from_user.id
                chat.ultima_offerta.offerta = bid
        except:
            return    

@restricted
def serialize(bot, update):
    for id in CHAT_IDS:
        if CHATS[id].bid_thread != None or CHATS[id].state_handler.getState() != IDLE:
            bot.send_message(chat_id=update.message.chat_id, text="Ci sono thread in esecuzione: non posso serializzare.")
            return
            
    f_admins = open("admins", "wb")
    pickle.dump(ADMINS, f_admins)
    f_admins.close()
        
    f_admins_username = open("admins_username", "wb")
    pickle.dump(ADMINS_USERNAME, f_admins_username)
    f_admins_username.close()
        
    f_chat_ids = open("chat_ids", "wb")
    pickle.dump(CHAT_IDS, f_chat_ids)
    f_chat_ids.close()
        
    f_chats = open("chats", "wb")
    pickle.dump(CHATS, f_chats)
    f_chats.close()
    
def deserialize():
    global ADMINS, ADMINS_USERNAME, CHAT_IDS, CHATS
    
    try:
        f_admins = open("admins", "rb")
        ADMINS = pickle.load(f_admins)
        f_admins.close()
            
        f_admins_username = open("admins_username", "rb")
        ADMINS_USERNAME = pickle.load(f_admins_username)
        f_admins_username.close()
            
        f_chat_ids = open("chat_ids", "rb")
        CHAT_IDS = pickle.load(f_chat_ids)
        f_chat_ids.close()
            
        f_chats = open("chats", "rb")
        CHATS = pickle.load(f_chats)
        f_chats.close()
    except:
        return
    
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)



def main():
    """Start the bot"""
    # Load previous state
    deserialize()
    
    # Create the EventHandler and pass it your bot's token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("aggiungiadmin", aggiungi_admin))
    dp.add_handler(CommandHandler("rimuoviadmin", rimuovi_admin))
    dp.add_handler(CommandHandler("aggiungipartecipante", aggiungi_partecipante))
    dp.add_handler(CommandHandler("rimuovipartecipante", rimuovi_partecipante))
    dp.add_handler(CommandHandler("avviaofferta", avvia_offerta, pass_args=True))
    dp.add_handler(CommandHandler("fermaofferta", ferma_offerta))
    dp.add_handler(CommandHandler("mostraadmin", mostra_admin))
    dp.add_handler(CommandHandler("mostrasaldo", mostra_saldo))
    dp.add_handler(CommandHandler("mostrapilotiassegnati", mostra_piloti_assegnati))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("help", help))
    
    # hidden commands
    dp.add_handler(CommandHandler("start", help))
    dp.add_handler(CommandHandler("serialize", serialize))

    # on non-command i.e. message 
    dp.add_handler(MessageHandler(Filters.text, controllore_di_stato))
    
    # log all errors
    dp.add_error_handler(error)
    
    # start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()