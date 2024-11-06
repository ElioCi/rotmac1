import streamlit as st
import json

#st.info(
#        ":train:  --- Footing design for vibrating --- This Application allows you to analyse shallow footings for rotating machines with weight < 3000 kg."
#        )
    
if 'prot' not in st.session_state or not st.session_state.prot:
    st.session_state.prot = False
    

  
st.markdown("---")
#st.title("⚙️ Vibrating machine analysis")
st.markdown("<h1 style='text-align: center;'>⚙️ Footings for vibrating machines</h1>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.page_link("https://enginapps.it", label="www.enginapps.it", icon="🏠")
#st.write("Application Start")

# Salva in un file temporaneo
st.session_state.prot = True
with open("prot_status.json", "w") as file:
    json.dump({"prot": st.session_state.prot}, file)

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

st.session_state.update({'prot': True})
#st.rerun()

# Inserisci il bottone nella pagina
st.markdown(button_html, unsafe_allow_html=True)
 
print ('prot', st.session_state.prot)
