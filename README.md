# HelpMeNow - Chatbot di Emergenza
HelpMeNow è un chatbot basato su LLAMA, progettato per fornire risposte rapide e affidabili in situazioni di emergenza. Utilizza Streamlit per l'interfaccia utente e Ollama per integrare il modello LLAMA.

Requisiti
Python: Versione 3.8 o successiva.
Pip: Per la gestione dei pacchetti Python.
Ollama: Installazione e configurazione del modello LLAMA.
Streamlit: Per avviare l'interfaccia utente.
Istruzioni di Installazione
1. Clonare il repository
Scarica o clona questo progetto nel tuo sistema locale:
 
git clone https://github.com/tuo-utente/helpmenow.git
cd helpmenow
2. Creare un ambiente virtuale
Crea un ambiente virtuale per isolare le dipendenze:
 
python -m venv venv
source venv/bin/activate  # Su macOS/Linux
venv\Scripts\activate     # Su Windows
3. Installare le dipendenze
Installa i pacchetti necessari:
 
pip install -r requirements.txt
4. Installare e configurare Ollama
Scarica e configura Ollama seguendo i passi qui sotto:

a. Installare Ollama
Visita il sito Ollama per scaricare e installare Ollama sul tuo sistema operativo.

b. Verificare l'installazione
Dopo l'installazione, verifica che Ollama sia funzionante:

ollama --version
c. Scaricare il modello LLAMA
Scarica il modello LLAMA che verrà utilizzato dal bot:

ollama pull llama3.1:latest

Avviare il Bot in Locale
Per avviare l'applicazione con Streamlit:
 
streamlit run app.py
Dove app.py è il nome del file Python contenente il codice del bot.

Uso
Dopo aver avviato Streamlit, si aprirà una finestra nel browser con l'interfaccia utente.
Inserisci una domanda nella casella di testo, come:
"Dove posso trovare il punto di raccolta più vicino a Piazza Navona?"
"Come trattare una frattura?"
"Cosa fare durante un terremoto?"
Il bot fornirà una risposta appropriata basata sul modello LLAMA.