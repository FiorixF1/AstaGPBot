# AstaGP Bot

Si tratta di un bot Telegram per fornire un aiuto nella gestione delle aste per il FantaGP di F1inGenerale.

Il bot prevede che ci siano tre tipi di utenti: gli **amministratori** (gli unici che possono interagire con il bot usandone i comandi), i **partecipanti** delle aste (che possono fare le offerte) e gli altri utenti che non possono svolgere nessuna operazione.

Segue una descrizione dei comandi esistenti, dopo i quali si fornirà un esempio d'esecuzione di un'asta ordinaria.

## Comandi

* **/aggiungiadmin** permette di aggiungere degli utenti come amministratori del bot. Essi vanno inseriti come parametri del comando separati da uno spazio. È necessario usare il loro username, che può essere preceduto dal simbolo @. Se per esempio vogliamo aggiungere "Pinco" e "Pallino" agli admin del bot, lo si può fare nei seguenti modi:
```
    /aggiungiadmin @Pinco @Pallino
    /aggiungiadmin Pinco Pallino
    /aggiungiadmin @Pinco Pallino
    /aggiungiadmin Pinco @Pallino
``` 

* **/rimuoviadmin** rimuove degli amministratori dal bot. Come il comando precedente, gli utenti sono forniti come parametri attraverso il loro username, eventualmente preceduto da @.
```
    /rimuoviadmin @Pinco @Pallino
```

* **/aggiungipartecipanti** aggiunge degli utenti tra i partecipanti dell'asta corrente. Analogamente ai comandi precedenti, inserisce gli utenti forniti come parametro tramite username, eventualmente preceduto da @.
```
    /aggiungipartecipanti Rick Morty @BojackHorseman
```
    
* **/rimuovipartecipanti** è il duale del comando precedente.

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
```
    /aggiungipartecipanti A B C...
```
    
A questo punto si può dare inizio alle offerte. L'amministratore dà il via con il seguente comando:
```
    /avviaasta Hamilton
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

* Gli utenti (sia amministratori che partecipanti) sono identificati con il loro **USERNAME**. Se un utente cambia il proprio username durante l'asta, il bot non lo riconoscerà più (né come amministratore né come partecipante).
* Il comando **/rimuoviadmin** non permette di eliminare se stessi dagli amministratori. Inoltre esistono alcuni admin definiti "supremi" che non possono essere cancellati da nessuno. Questo per prevenire la situazione paradossale in cui il bot si ritrovi senza nessun admin e nessuno lo possa più controllare senza un hard reset.
* Ribadiamo che all'inizio di ogni asta l'amministratore deve ricordarsi di aggiungere i partecipanti.
* Il bot può gestire una sola asta alla volta ed il suo stato è **GLOBALE**. Per questo motivo **NON** può essere utilizzato contemporaneamente su due o più gruppi. Esso vedrebbe i diversi gruppi come appartenenti ad un'unica asta più grande, di conseguenza i partecipanti si interferirebbero tra loro creando un macello.
* Si sconsiglia l'uso del comando **/fermaofferta** a pochi secondi dal termine dell'asta. Non essendoci sistemi di lock sulle variabili (per semplicità ed efficienza), usare questo comando allo scadere dell'asta potrebbe generare comportamenti indeterminati.

## Changelog

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