import streamlit as st
import pandas as pd
import csv
from math import sqrt, log, pi, exp
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import numpy as np


if 'newFlag' not in st.session_state:
    st.session_state.newFlag = 'new'


if 'loadingFactors' not in st.session_state:
    st.session_state.loadingFactors = []
    
st.title ('Loading Factors')

if st.session_state.newFlag == 'new':

    st.session_state['loadingFactors'] = {
        'Comb_name': ['ShortCircuit', 'Operation', 'Wind', 'Quake','SCT_Ovr','SLS' ],
        'DL': [1.3,1.3,0.9,1.0,0.9,1.0],
        'SCT': [1.5,0.0,0.0,0.0,2.0,0.0],
        'DYN': [0.0,1.3,1.0,1.0,0.0,1.0],
        'WIND': [0.0,0.0,1.5,0.0,0.0,0.0],
        'QUAKE': [0.0,0.0,0.0,1.0,0.0,0.0],   
    }
    dfComb = pd.DataFrame(st.session_state['loadingFactors'])
    dfComb = dfComb.fillna('')

elif st.session_state.newFlag ==  'stored':
    dfComb = pd.read_csv('files/Combs.csv', index_col=False)
    dfComb.drop(dfComb.columns[dfComb.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)


st.subheader('Summary of Combination Factors')
#st.dataframe(dfComb, hide_index= True)
#dfComb.to_csv("files/Combs.csv")   # salva dati su LoadsCond 

# Configura la griglia con opzioni personalizzate
gb = GridOptionsBuilder.from_dataframe(dfComb)
gb.configure_default_column(editable=True, autoSizeColumns= True)  # Rendi tutte le colonne editabili
gb.configure_grid_options(domLayout='autoHeight', suppressSizeToFit=True)
gb.configure_column("QUAKE", maxWidth=100)
gridOptions = gb.build()

# Visualizza la griglia editabile
grid_response = AgGrid(
    dfComb,
    gridOptions=gridOptions,
    update_mode=GridUpdateMode.MODEL_CHANGED,  # Aggiorna quando i dati cambiano
    height=300,
    allow_unsafe_jscode=True,  # Se necessario
)

# Recupera i dati modificati
updated_df = grid_response['data']
st.info('You can edit and change the values directly in the table.')
# Visualizza il DataFrame aggiornato
#st.write(updated_df)
updated_df.to_csv("files/Combs.csv")   # salva dati su Combs.csv

