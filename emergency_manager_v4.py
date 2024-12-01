import json
import requests
from geopy.distance import geodesic
import ollama
import streamlit as st

# Prompt iniziale per specializzare LLAMA
INITIAL_PROMPT = """
Sei un assistente virtuale specializzato nella gestione delle emergenze. 
Il tuo scopo è fornire istruzioni rapide, pratiche e affidabili per aiutare gli utenti a gestire situazioni critiche come terremoti, alluvioni, incendi o emergenze mediche. 
Le tue risposte devono essere:
1. Chiare e concise.
2. Basate su linee guida standard di sicurezza e primo soccorso.
3. Fornite passo passo quando si tratta di emergenze mediche o di sicurezza.
Ora sei pronto per rispondere.
"""

# Funzione per caricare il dataset
def load_dataset(filename="rome_emergency_dataset.json"):
    """
    Carica il dataset combinato da un file JSON.
    """
    with open(filename, "r") as file:
        return json.load(file)

# Funzione per interrogare LLAMA tramite Ollama
def ask_ollama(prompt):
    """
    Interroga il modello LLAMA con il prompt iniziale e la domanda dell'utente.
    """
    try:
        model_name = "llama3.1:latest"
        full_prompt = f"{INITIAL_PROMPT}\nDomanda: {prompt}\nRisposta:"
        response = ollama.generate(model=model_name, prompt=full_prompt)
        return response.response.strip()
    except Exception as e:
        st.write(e)
        return f"Errore durante l'interrogazione del modello: {e}"

# Funzione per ottenere coordinate con OpenStreetMap (Nominatim)
def get_coordinates_osm(address):
    """
    Ottiene le coordinate GPS di un indirizzo utilizzando OpenStreetMap Nominatim.
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "EmergencyBot/1.0 (youremail@example.com)"}
    try:
        response = requests.get(base_url, params={"q": address, "format": "json"}, headers=headers)
        if response.status_code != 200:
            return f"Errore nell'API: {response.status_code}"
        
        data = response.json()
        if data:
            location = data[0]
            return float(location["lat"]), float(location["lon"])
        else:
            return "Indirizzo non trovato."
    except requests.exceptions.RequestException as e:
        return f"Errore nella connessione: {e}"

# Funzione per trovare il punto di raccolta più vicino
def find_nearest_point(user_location, dataset):
    """
    Trova il punto di raccolta più vicino basandosi sulla posizione dell'utente.
    """
    nearest_point = None
    shortest_distance = float("inf")

    for point in dataset["points_of_collection"]:
        point_location = (float(point["gps"].split(",")[0]), float(point["gps"].split(",")[1]))
        distance = geodesic(user_location, point_location).km
        if distance < shortest_distance:
            nearest_point = point
            shortest_distance = distance

    if nearest_point:
        return nearest_point, shortest_distance
    else:
        return None, None

# Funzione per analizzare la query con LLAMA
def analyze_query_with_llama(query):
    """
    Utilizza LLAMA per analizzare la query dell'utente e determinare il tipo di richiesta.
    """
    prompt = f"""
    L'utente ha chiesto: "{query}"
    Classifica questa domanda come una delle seguenti categorie:
    - location_query: se riguarda una posizione o un punto di raccolta.
    - emergency_medical: se riguarda una situazione di emergenza medica.
    - emergency_natural: se riguarda emergenze naturali come terremoti, alluvioni o incendi.
    - general: se riguarda una richiesta generica o un'emergenza generale non specifica.
    Rispondi solo con una delle categorie sopra elencate.
    Se non riesci a classificare la domanda, rispondi con "unknown".
    """
    try:
        response = ask_ollama(prompt)
        classification = response.strip().lower()
        if classification in ["location_query", "emergency_medical", "emergency_natural", "general"]:
            return classification
        else:
            return "unknown"
    except Exception as e:
        return f"Errore durante l'analisi della query: {e}"

# Funzione per estrarre la località con LLAMA
def extract_location_with_llama(query):
    """
    Utilizza LLAMA per estrarre il nome della città o dell'indirizzo dalla query.
    """
    prompt = f"""
    L'utente ha chiesto: "{query}"
    Identifica il nome della città, dell'indirizzo o della località nella domanda.
    Rispondi solo con il nome della città, dell'indirizzo o della località. Se non trovi un riferimento, rispondi con "Località non specificata".
    """
    try:
        response = ask_ollama(prompt)
        return response.strip()
    except Exception as e:
        return f"Errore durante l'estrazione della località: {e}"
    
# Funzione per gestire query di posizione
# Funzione per gestire query di posizione
def handle_location_query(user_query, dataset):
    """
    Gestisce le richieste basate sulla posizione dell'utente.
    """
    location = extract_location_with_llama(user_query)
    if "Errore" in location or "Località non specificata" in location:
        return "Non sono riuscito a identificare una località valida. Per favore, specifica un indirizzo o una città."

    user_coordinates = get_coordinates_osm(location)
    if isinstance(user_coordinates, tuple):
        nearest_point, distance = find_nearest_point(user_coordinates, dataset)
        if nearest_point:
            return (f"Il punto di raccolta più vicino è {nearest_point['name']} "
                    f"a {distance:.2f} km di distanza. Indirizzo: {nearest_point['address']} "
                    f"Note: {nearest_point['notes']}")
        else:
            return "Non sono riuscito a trovare punti di raccolta vicini."
    else:
        return user_coordinates

# Interfaccia Streamlit
def main():
    st.title("HelpMeNow - Chatbot di Emergenza con LLAMA")
    st.write("Inserisci la tua domanda relativa a emergenze mediche, naturali o punti di raccolta.")
    
    user_query = st.text_input("Digita la tua domanda qui:")
    dataset = load_dataset()

    if user_query:
        query_type = analyze_query_with_llama(user_query)
        if query_type == "location_query":
            st.write("Gestendo la richiesta di punti di raccolta...")
            response = handle_location_query(user_query, dataset)
        elif query_type == "emergency_medical":
            response = ask_ollama(f"Fornisci istruzioni di primo soccorso passo passo per: {user_query}")
        elif query_type == "emergency_natural":
            response = ask_ollama(f"Fornisci istruzioni passo passo per: {user_query}")
        elif query_type == "general":
            response = ask_ollama(user_query)
        else:
            response = "Non sono riuscito a classificare la tua domanda. Per favore, riformula la tua richiesta."
        
        st.success(f"Bot: {response}")

if __name__ == "__main__":
    main()
