# AstaGP Bot

Si tratta di un bot Telegram per fornire un aiuto nella gestione delle aste per il FantaGP di F1inGenerale.

In questa prima versione, il bot prevede che ci siano tre tipi di utenti:
* Gli **amministratori**
* I **partecipanti** all'asta
* Gli altri utenti

A seconda della categoria a cui un utente appartiene, esso potrà eseguire o meno determinati comandi.

Segue una documentazione dei comandi esistenti, catalogati per tipo di utente. Al termine si fornirà un esempio d'esecuzione di un'asta ordinaria.

## Comandi

### Amministratori

* **/aggiungiadmin** permette di aggiungere un utente come amministratore del bot. Il comando inserisce un solo utente alla volta che va inserito come parametro attraverso il suo username. Se per esempio vogliamo aggiungere "Pinco" e "Pallino" agli admin del bot, i comandi da dare saranno:
    /aggiungiadmin Pinco
    /aggiungiadmin Pallino
    
* **/rimuoviadmin** rimuove un amministratore del bot. Come il comando precedente, l'utente è fornito come parametro attraverso il suo username.
    /rimuoviadmin Pinco
    /rimuoviadmin Pallino

* **/aggiungipartecipante** aggiunge un utente tra i partecipanti dell'asta corrente. Analogamente ai comandi precedenti, inserisce un solo utente per volta fornito come parametro tramite username.
    /aggiungipartecipante Rick
    /aggiungipartecipante Morty
    
* **/rimuovipartecipante** è il duale del comando precedente.

* **/creaasta** inizializza un'asta vuota. Il bot può trovarsi nello stato di nessun'asta attiva oppure di averne una attiva. Questo comando permette di passare dallo stato di "Asta disattivata" a quello di "Asta attiva". Esso non riceve parametri e darà un messaggio di errore se esiste già un'asta attiva.

* **/cancellasta** rimuove l'asta correntemente attiva con tutte le sue informazioni. Fa passare il bot dallo stato di "Asta attiva" a quello di "Asta disattivata". Essendo un'operazione delicata, il bot richiederà una conferma dell'operazione, scrivendo "s" per confermare oppure "n" per annullare. Durante questa fase tutti gli altri comandi sono disabilitati.

* **/avviaofferta** avvia l'asta per un pilota. Il pilota viene fornito come parametro del comando e farà partire l'asta per i prossimi due minuti. Durante quel periodo di tempo i partecipanti potranno fare le loro offerte, mentre gli altri comandi saranno disabilitati.
    /avviaofferta Vettel
    
### Partecipanti

* **/b** permette ad un partecipante di fare un'offerta. Esso prende come parametro un numero che indica la quantità di fantamilioni offerti. Se un partecipante offre più soldi di quanti ne ha oppure possiede già due piloti, questo comando ignorerà l'offerta silenziosamente. **ATTENZIONE: se si inserisce un'offerta con il solo numero senza il comando /b davanti, essa verrà IGNORATA dal bot!**
    /b 20
    
### Altri utenti

* **/mostraadmin** invia una lista degli amministratori del bot.

* **/mostrasaldo** invia una lista con il saldo rimanente in fantamilioni di ogni partecipante dell'asta.

* **/mostrapilotiassegnati** invia una lista con i piloti assegnati ad ogni partecipante dell'asta.

## Esempio di asta

Simuliamo l'esecuzione di un'asta, assumendo che gli amministratori ed i partecipanti si trovino all'interno dello stesso gruppo.

L'amministratore crea l'asta con il comando **/creaasta**. Se richiesto, cancellerà l'asta precedente ancora attiva con **/cancellaasta**.

L'amministratore aggiunge i partecipanti dell'asta. Questo è un passaggio **IMPORTANTISSIMO**: se si dimentica di fare ciò, tutte le offerte fatte dai partecipanti non verranno considerate!
    /aggiungipartecipante A
    /aggiungipartecipante B
    /aggiungipartecipante C
    ...
    
A questo punto si può dare inizio alle offerte. L'amministratore dà il via con il seguente comando:
    /avviaasta Hamilton
    
I partecipanti dovranno fare le loro offerte con l'apposito comando:
    /b 10
    /b 20
    /b 50
    ...
    
Allo scadere del tempo, il bot assegnerà il pilota al partecipante che ha dato l'offerta maggiore. Il risultato si potrà verificare tramite i comandi **/mostrasaldo** e **/mostrapilotiassegnati**.

Finite tutte le offerte e registrate nel leggendario database di F1inGenerale, si può resettare il bot con **/cancellaasta**.

## Note importanti

* Gli utenti (sia amministratori che partecipanti) sono identificati con il loro **USERNAME**. Se un utente cambia il proprio username durante l'asta, il bot non lo riconoscerà più (né come amministratore né come partecipante).
* I comandi che aggiungono e rimuovono utenti operano su un solo utente alla volta. Esso deve essere fornito tramite username **SENZA** il simbolo @ davanti.
* Il comando **/rimuoviadmin** non permette di eliminare se stessi dagli amministratori. Inoltre esistono alcuni admin definiti "supremi" che non possono essere cancellati da nessuno. Questo per prevenire la situazione paradossale in cui il bot si ritrovi senza nessun admin e nessuno lo possa più controllare senza un hard reset.
* Ribadiamo che all'inizio di ogni asta l'amministratore deve ricordarsi di aggiungere i partecipanti.
* I partecipanti devono ricordarsi di usare il comando /b per fare le loro offerte, se non vogliono che siano ignorate.
* Il bot può gestire una sola asta alla volta ed il suo stato è **GLOBALE**. Per questo motivo **NON** può essere utilizzato contemporaneamente su due o più gruppi. Esso vedrebbe i diversi gruppi come appartenenti ad un'unica asta più grande, di conseguenza i partecipanti si interferirebbero tra loro creando un macello.

## Changelog

Versione 1:
* First release