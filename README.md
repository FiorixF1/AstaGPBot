# AstaGP Bot

Si tratta di un bot Telegram per fornire un aiuto nella gestione delle aste per il FantaGP di F1inGenerale.

Il bot prevede che ci siano tre tipi di utenti: gli **amministratori** (gli unici che possono interagire con il bot usandone i comandi), i **partecipanti** delle aste (che possono fare le offerte) e gli altri utenti che non possono svolgere nessuna operazione.

Segue una descrizione dei comandi esistenti, dopo i quali si fornirà un esempio d'esecuzione di un'asta ordinaria.

## Comandi

* **/aggiungiadmin** permette di aggiungere un utente come amministratore del bot. Il comando si utilizza rispondendo ad un messaggio dell'utente che vogliamo aggiungere.

* **/rimuoviadmin** rimuove un amministratore dal bot. Il comando si utilizza rispondendo ad un messaggio dell'utente che vogliamo rimuovere.

* **/aggiungipartecipante** aggiunge un utente tra i partecipanti dell'asta corrente. Analogamente ai comandi precedenti, si utilizza rispondendo ad un messaggio dell'utente che vogliamo aggiungere.
    
* **/rimuovipartecipante** è il duale del comando precedente.

* **/reset** svuota l'asta corrente rimuovendone i partecipanti con i loro saldi e piloti. Essendo un'operazione delicata, il bot richiederà una conferma dell'operazione, scrivendo "s" per confermare oppure "n" per annullare. Durante questa fase tutti gli altri comandi sono disabilitati.

* **/avviaofferta** avvia l'asta per un pilota. Il pilota viene fornito come parametro del comando e farà partire l'asta per i prossimi due minuti. Durante quel periodo di tempo i partecipanti potranno fare le loro offerte, mentre gli altri comandi saranno disabilitati.
```
    /avviaofferta Vettel
```

* **/fermaofferta** sospende l'asta corrente. Ogni offerta fatta in precedenza viene annullata. Può servire in caso di imprevisti.

* **/mostraadmin** invia una lista degli amministratori del bot.

* **/mostrasaldo** invia una lista con il saldo rimanente in fantamilioni di ogni partecipante dell'asta.

* **/mostrapilotiassegnati** invia una lista con i piloti assegnati ad ogni partecipante dell'asta.

## Esempio di asta

Simuliamo l'esecuzione di un'asta, assumendo che gli amministratori ed i partecipanti si trovino all'interno dello stesso gruppo.

L'amministratore prepara l'asta con il comando **/reset**, che rimuove informazioni rimaste da eventuali aste precedenti.

L'amministratore aggiunge i partecipanti dell'asta. Questo è un passaggio **IMPORTANTISSIMO**: se si dimentica di fare ciò, tutte le offerte fatte dai partecipanti non verranno considerate!
    
A questo punto si può dare inizio alle offerte. L'amministratore dà il via con il seguente comando:
```
    /avviaofferta Hamilton
```
    
I partecipanti dovranno fare le loro offerte semplicemente scrivendo la quantità di fantamilioni che vogliono pagare, esattamente come farebbero in un'asta manuale senza bot.
```
    A: 10
    B: 20
    C: 50
    ...
```
    
Allo scadere del tempo, il bot assegnerà il pilota al partecipante che ha dato l'offerta maggiore. Il risultato si potrà verificare tramite i comandi **/mostrasaldo** e **/mostrapilotiassegnati**.

Finite tutte le offerte e registrate nel leggendario database di F1inGenerale, si può resettare il bot con **/reset**.

## Note importanti

* Il comando **/rimuoviadmin** non permette di eliminare se stessi dagli amministratori. Inoltre esistono alcuni admin definiti "supremi" che non possono essere cancellati da nessuno. Questo per prevenire la situazione paradossale in cui il bot si ritrovi senza nessun admin e nessuno lo possa più controllare senza un hard reset.
* **Ribadiamo** che all'inizio di ogni asta l'amministratore deve ricordarsi di aggiungere i partecipanti!
* Durante gli ultimi secondi dell'asta, potrebbe verificarsi un bug per cui il bot interrompe il countdown bloccando l'asta. Non è ben chiaro se il bug sia causato dalle API di Telegram o da un rallentamento momentaneo della connessione di rete. In ogni caso, per risvegliare il bot è necessario dare il comando **/fermaofferta** e riavviare l'asta.
* Nel caso in cui sia necessario riavviare il bot, interrompere tutte le aste in corso e dare il comando nascosto **/serialize**. Esso salverà lo stato attuale del bot nel database in modo che possa essere ripristinato a seguito del riavvio.

## Deployment

Se si vuole eseguire il bot sulla propria macchina, sono necessari i seguenti strumenti:
* [Python 3.6](https://www.python.org/getit/) o superiore
* La libreria [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* Un bot di Telegram con la sua API Token da inserire come parametro nel codice e la seguente descrizione dei comandi:
```
    aggiungiadmin - Rendi amministratore un utente
    rimuoviadmin - Rimuovi un utente dagli amministratori
    aggiungipartecipante - Aggiungi un utente all'asta
    rimuovipartecipante - Rimuovi un utente dall'asta
    avviaofferta - Avvia l'asta per un pilota
    fermaofferta - Annulla l'asta corrente
    mostraadmin - Mostra la lista degli admin del bot
    mostrasaldo - Mostra il saldo di ogni partecipante
    mostrapilotiassegnati - Mostra i piloti di ogni partecipante
    reset - Cancella i dati dell'asta
    help - Aiuto
```

## Changelog

Versione 3:
* Gli amministratori ed i partecipanti sono ora identificati tramite il loro ID anziché username.
* I comandi per aggiungere/rimuovere amministratori e partecipanti si usano inviandoli in risposta ad un messaggio dell'utente interessato.
* Il bot è diventato utilizzabile contemporaneamente su diverse chat, senza che si interferiscano a vicenda.
* Lo stato del bot può essere salvato su disco con il comando **/serialize** per essere ripristinato a seguito di un reboot.
* Aggiunti i comandi **/help** e **/start** che riportano un link a questa pagina.
* Miglioramento generale del codice con l'uso di nuove classi e dei decoratori per il controllo dell'accesso.
* Inserita un'immagine del modello a stati finiti del bot.

Versione 2:
* Tutti i comandi del bot sono attivabili solo dagli amministratori, anche quelli che non alterano lo stato.
* Rimossi i comandi per aggiungere e cancellare un'asta: ve ne è sempre una attiva. Esiste solo un comando per resettarla.
* Aggiunti messaggi di risposta se un partecipante fa un'offerta senza avere abbastanza soldi o se possiede già due piloti.
* Si possono aggiungere/rimuovere più admin e partecipanti chiamando il comando apposito una sola volta.
* Si può usare @ all'inizio di uno username quando si aggiungono/rimuovono admin e partecipanti.
* Viene mostrato un messaggio di risposta se si invoca un comando che richiede argomenti ma non ce ne sono.
* **Rimosso il comando /b:** gli utenti devono solo scrivere un numero per fare un'offerta.
* Aggiunto comando **/fermaofferta** per sospendere l'asta dopo che è stata avviata.

Versione 1:
* First release