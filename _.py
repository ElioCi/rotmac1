import streamlit as st

from urllib.parse import urlparse, parse_qs
import requests
import jwt
from jwt import PyJWTError
import time

# Chiave segreta utilizzata per firmare il token
SECRET_KEY = 'EC1'

# Funzione per verificare il token
def verify_token(token):
    try:
        # Decodifica e verifica il token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except PyJWTError as e:
        # Token non valido o scaduto
        st.error("Token non valido o scaduto: " + str(e))
        return None

# Acquisisci il token dai parametri dell'URL
query_params = st.experimental_get_query_params()
token = query_params.get("token", [None])[0]

if token:
    # Verifica il token
    decoded_token = verify_token(token)
    if decoded_token:
        st.success("Accesso autorizzato!")
        st.write("Token decodificato:", decoded_token)
        # Inserisci qui il codice dell'applicazione Streamlit
    else:
        st.error("Accesso negato: token non valido o scaduto.")
        st.stop()
else:
    st.error("Nessun token fornito, accesso negato.")
    st.stop()
#  ***********************************************************

st.set_page_config(
    page_title= "Vibratin Machines rel.1",
    page_icon= "⚙️"
    )

#st.info(
#        ":train:  --- Footing design for vibrating --- This Application allows you to analyse shallow footings for rotating machines with weight < 3000 kg."
#        )
    
st.markdown("---")
#st.title("⚙️ Vibrating machine analysis")
st.markdown("<h1 style='text-align: center;'>⚙️ Footings for vibrating machines</h1>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.page_link("https://enginapps.it", label="www.enginapps.it", icon="🏠")
#st.write("Application Start")

# Utilizza un link HTML per fare il redirect a "pages/main.py"
# Codice HTML e CSS per il pulsante con hover
button_html = """
    <style>
    .button-container {
        display: flex;
        justify-content: center; /* Centra il pulsante orizzontalmente */
        align-items: center; /* Centra il pulsante verticalmente, se necessario */
        height: 20vh; /* Imposta l'altezza del contenitore al 30% dell'altezza della vista */
    }
    .hover-button {
        padding: 10px 30px;
        font-size: 16px;
        cursor: pointer;
        color: white;
        background-color: #4CAF50; /* Colore iniziale del pulsante */
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease, transform 0.3s ease; /* Transizioni per un effetto fluido */
    }

    /* Effetto hover */
    .hover-button:hover {
        background-color: #45a049; /* Colore al passaggio del mouse */
        color: #000000;
        transform: scale(1.05); /* Leggero ingrandimento */
    }
    </style>
    <div class="button-container">
    <a href="main" target="_self">
        <button class="hover-button">GoTo main page</button>
    </a>
"""



# Inserisci il bottone nella pagina
st.markdown(button_html, unsafe_allow_html=True)

