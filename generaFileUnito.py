import streamlit as st
import pandas as pd
from datetime import datetime

def SalvaDati(fileNamePath):
    # Carica i file CSV
    dati_generali = pd.read_csv("files/DatiGenerali.csv")
    dati_eqp = pd.read_csv("files/DatiEqp.csv")
    dati_fond = pd.read_csv("files/DatiFooting.csv")
    dati_loads = pd.read_csv("files/LoadsCond.csv")
    dati_combs = pd.read_csv("files/Combs.csv")

    # Crea una colonna vuota
    #colonna_vuota = pd.DataFrame(['' for _ in range(max(len(dati_generali), len(dati_piping)))], columns=[''])
    colonna_app = pd.DataFrame({'': [None] * max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))})
    colonna_vuota1 = pd.DataFrame({'': [None] * max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))})
    colonna_vuota2 = pd.DataFrame({'': [None] * max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))})
    colonna_vuota3 = pd.DataFrame({'': [None] * max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))})
    colonna_vuota4 = pd.DataFrame({'': [None] * max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))})
    
    # Inserisci l'intestazione personalizzata nella colonna vuota
    colonna_app.columns = [f"VibratingMachines1 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
    colonna_vuota1.columns = ["separator_1"]
    colonna_vuota2.columns = ["separator_2"]
    colonna_vuota3.columns = ["separator_3"]
    colonna_vuota4.columns = ["separator_4"]

    # Allinea le righe dei due file in modo che abbiano la stessa lunghezza
    dati_generali = dati_generali.reindex(range(max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))))
    dati_eqp = dati_eqp.reindex(range(max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))))
    dati_fond = dati_fond.reindex(range(max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))))
    dati_loads = dati_loads.reindex(range(max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))))
    dati_combs = dati_combs.reindex(range(max(len(dati_generali), len(dati_eqp), len(dati_fond), len(dati_loads), len(dati_combs))))

    # Unisci i due DataFrame con la colonna vuota tra di loro
    dati_uniti = pd.concat([colonna_app, dati_generali, colonna_vuota1, dati_eqp, colonna_vuota2, dati_fond, colonna_vuota3, dati_loads, colonna_vuota4, dati_combs], axis=1)

    # Permetti all'utente di scaricare il file
    csv = dati_uniti.to_csv(index=False)

    st.download_button(label=f"💾 Download file {fileNamePath}", data=csv, file_name=f"{fileNamePath}", mime="text/csv", help= '***click here to save data in your personal drive***')
