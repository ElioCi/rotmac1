import streamlit as st
import pandas as pd
from LoadFileData import loadData
import json

st.set_page_config(
    page_title= "Vibrating Machines rel.1",
    page_icon= "⚙️"
    )


# Legge il valore dal file temporaneo
try:
    with open("prot_status.json", "r") as file:
        data = json.load(file)
        st.session_state.prot = data.get("prot", False)
except FileNotFoundError:
    st.session_state.prot = False


#if 'navigate_to_first_page' not in st.session_state:
#    st.session_state['navigate_to_first_page'] = False

st.write(f"User authorized: 🛂{st.session_state.prot}")



#st.session_state.flagPro = True
#print ('prot main', st.session_state.prot)

    
# Funzione per svuotare il contenuto dei file mantenendo solo la prima riga
def reset_files(general_data_path, eqp_data_path, footing_data_path, new_values=None, new_fondvalues=None):
    # Carica i dati da entrambi i file
    df_general = pd.read_csv(general_data_path)
    dffond = pd.read_csv(footing_data_path)
    st.session_state.dfeqp = pd.read_csv(eqp_data_path)
    #st.session_state.dffond = pd.read_csv(footing_data_path)
    #df_general['JAccount', 'Project', 'Location'] = df_general['JAccount', 'Project', 'Location'].astype(str)
    # Mantieni solo la prima riga per entrambi i file
    df_general = df_general.iloc[:1, :]
    dffond = dffond.iloc[:1, :]
    st.session_state.dfeqp = st.session_state.dfeqp.iloc[:0, :]
    #st.session_state.dffond = st.session_state.dffond.iloc[:0, :]
    # Converti le colonne in stringhe prima di assegnare i valori
    df_general['JAccount'] = df_general['JAccount'].astype(str)
    df_general['Project'] = df_general['Project'].astype(str)
    df_general['Location'] = df_general['Location'].astype(str)
    #df_general['Wind'] = df_general['Wind'].astype(str)
    #df_general['Ta'] = df_general['Ta'].astype(str)
    # Sostituisci i campi specifici nel file GeneralData.csv
    if new_values:
        df_general.loc[0, 'JAccount'] = new_values.get('JAccount', '')
        df_general.loc[0, 'Project'] = new_values.get('Project', '')
        df_general.loc[0, 'Location'] = new_values.get('Location', '')
        df_general.loc[0, 'Fwx'] = new_values.get('Fwx', '')
        df_general.loc[0, 'Mwy'] = new_values.get('Mwy', '')
        df_general.loc[0, 'Fwy'] = new_values.get('Fwy', '')
        df_general.loc[0, 'Mwx'] = new_values.get('Mwx', '')
    # Sostituisci i campi specifici nel file GeneralData.csv
    if new_fondvalues:
        dffond.loc[0, 'a'] = new_fondvalues.get('a', '')
        dffond.loc[0, 'b'] = new_fondvalues.get('b', '')
        dffond.loc[0, 'Lx'] = new_fondvalues.get('Lx', '')
        dffond.loc[0, 'Ly'] = new_fondvalues.get('Ly', '')
        dffond.loc[0, 'Hz'] = new_fondvalues.get('Hz', '')
        dffond.loc[0, 'Elev'] = new_fondvalues.get('Elev', '')
        dffond.loc[0, 'allP'] = new_fondvalues.get('allP', '')
        dffond.loc[0, 'gconc'] = new_fondvalues.get('gconc', '')
        
    # Salva i file aggiornati
    df_general.to_csv(general_data_path, index=False)
    st.session_state.dfeqp.to_csv(eqp_data_path, index=False)
    #st.session_state.dffond.to_csv(footing_data_path, index=False)
    dffond.to_csv(footing_data_path, index=False)
    st.success("Calculation files successfully initialized.")
if 'statoPulsante1' not in st.session_state:
    st.session_state.statoPulsante1 = 'noclick'
if 'statoPulsante2' not in st.session_state:
    st.session_state.statoPulsante2 = 'noclick'
if 'preset' not in st.session_state:
    st.session_state.preset = 0    
if 'DatiCaricati' not in st.session_state:
    st.session_state.DatiCaricati = False
st.info(
        ":smile: Hi --- This Application allows you to analyse shallow footings for vibrating machines with weight < 4000 kg."
        )
    
st.markdown("---")
#st.title("⚙️ Vibrating machine analysis")
st.markdown("<h1 style='text-align: center;'>⚙️ Footings for vibrating machine</h1>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.page_link("https://enginapps.it", label="www.enginapps.it", icon="🏠")
sceltaNew = col3.radio("Select an option", options= ('New Project', 'Stored Project'))
if 'newFlag' not in st.session_state:
    st.session_state.newFlag = 'none'
if 'addphaseStarted' not in st.session_state:
    st.session_state.addphaseStarted = False      
# Se cambio da New Project a Stored Project, resetto tutto ciò che riguarda New Project
if sceltaNew == 'Stored Project' and st.session_state.newFlag == 'new':
    st.session_state.statoPulsante1 = 'noclick'
    st.session_state.newFlag = 'stored'
    st.rerun()
if sceltaNew == 'New Project' and st.session_state.newFlag == 'stored':
    st.session_state.statoPulsante2 = 'noclick'
    st.session_state.newFlag = 'new'
    st.rerun()
posPulsante = st.empty()
if sceltaNew == 'New Project':
    st.session_state.newFlag = 'new'
    if posPulsante.button('🎬 Start !'):
        #st.session_state.newFlag = 'new'
        st.sidebar.info(st.session_state.newFlag)
        
        st.session_state.statoPulsante1 = 'clicked'
        col1, col2, col3 = st.columns([5, 0.6, 1])
        col1.warning('**Warning**: if you continue, all data will be initialized. Are you sure?')
        
#print(st.session_state.newFlag, st.session_state.statoPulsante1, st.session_state.statoPulsante2)
if (st.session_state.statoPulsante1 == 'clicked'):
    if col2.button('Yes'):
        
        new_values = {
            'JAccount': 'job code',  # Sostituisci con valore vuoto
            'Project': 'project title',   # Sostituisci con valore vuoto
            'Location': 'location',  # Sostituisci con valore vuoto o specifico
            'Fwx': 0.00,    # Sostituisci con valore vuoto
            'Mwy': 0.00,    # Sostituisci con valore vuoto
            'Fwy': 0.00,    # Sostituisci con valore vuoto
            'Mwx': 0.00,    # Sostituisci con valore vuoto
        }
        new_fondvalues = {
            'a': 0.00,  # Sostituisci con valore vuoto
            'b': 0.00,   # Sostituisci con valore vuoto
            'Lx': 0.00,  # Sostituisci con valore vuoto o specifico
            'Ly': 0.00,    # Sostituisci con valore vuoto
            'Hz': 0.00,    # Sostituisci con valore vuoto
            'Elev': 0.00,    # Sostituisci con valore vuoto
            'allP': 0.00,    # Sostituisci con valore vuoto
            'gconc':0.00,
        }
        reset_files('files/DatiGenerali.csv', 'files/DatiEqp.csv', 'files/DatiFooting.csv', new_values=new_values, new_fondvalues=new_fondvalues)
        st.session_state['data'] = []
        st.session_state['dataEqp'] = []
        st.session_state[''] = []
        st.session_state.statoPulsante1 = 'noclick'
        st.session_state.addphaseStarted = False  
        pagina = 'pages/1_📝General_data.py'
        st.switch_page(pagina)
        #st.markdown("[Go to General Data](📝General_data)")
    
    
    if col3.button('No'):
        st.session_state.statoPulsante1 = 'noclick'
        st.rerun()

if sceltaNew == 'Stored Project':
    st.session_state.newFlag = 'stored'
    st.sidebar.info(st.session_state.newFlag )
    st.session_state.statoPulsante2 = 'clicked'
    st.session_state.statoPulsante1 = 'noclick'
    
    col1, col2, col3 = st.columns([5, 0.6, 1])
    col1.warning('**Warning**: if you continue, all data will be replaced with those in the archive.')
    loadData()
    if st.session_state.DatiCaricati == True:
        st.session_state.statoPulsante2 = 'noclick'
        if st.button('🎬 Start !'):  
            pagina = 'pages/1_📝General_data.py'
            st.switch_page(pagina)
                        
#flag_ns = col2.radio("Select one option", ["New Calculation", "Saved Calculation"])
st.markdown("")
st.info("-- App developed by ing. Pasquale Aurelio Cirillo - @ 2024 --")
#st.page_link("pages/page_1.py", label="New Calculation", icon="1️⃣")
#col1.markdown("")
#col1.markdown("")
# col1.page_link("pages/new_calculation.py", label="Calculation Sheet", icon="📝")
# st.page_link("pages/saved_calculation.py", label="Saved Calculation", icon="📂", disabled=False)
#st.page_link("http://www.google.com", label="Google", icon="🌎")
