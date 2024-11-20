# MySQL Backup & Restore

## Descrizione
Questo progetto è un'app interattiva che consente di effettuare backup completi dei database MySQL e di ripristinare i backup esistenti.

### Funzionalità:
- Creazione di backup specificando il nome del file `.sql`.
- Ripristino da backup esistenti con elenco selezionabile.
- Interfaccia web user-friendly.

## Istruzioni per l'uso

### Esecuzione tramite Docker Compose
1. Assicurati che Docker e Docker Compose siano installati sul tuo sistema.
2. Costruisci e avvia i servizi:
```bash
   docker-compose up --build -d
 ```  

L'app sarà disponibile all'indirizzo http://localhost:5000.
La directory ./data conterrà i backup creati.

### Arresto
Per arrestare i servizi, esegui:

```bash
docker-compose down
```