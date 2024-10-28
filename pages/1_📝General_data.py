import streamlit as st

import pandas as pd
import csv
import os



# inizializza session_state
if 'newFlag' not in st.session_state:
    st.session_state.newFlag = 'new'
if 'dataGen' not in st.session_state:
    st.session_state['dataGen'] = []
if 'JAccount' not in st.session_state:
    st.session_state.JAccount = ""
if 'Project' not in st.session_state:
    st.session_state.Project = ""
if 'Location' not in st.session_state:
    st.session_state.Location = ""
if 'Fwx' not in st.session_state:
    st.session_state.Fwx = 0.00
if 'Mwy' not in st.session_state:
    st.session_state.Mwy = 0.00
if 'Fwy' not in st.session_state:
    st.session_state.Fwy = 0.00
if 'Mwx' not in st.session_state:
    st.session_state.Mwx = 0.00
if 'acc' not in st.session_state:
    st.session_state.acc = 0.00    
if 'dataConfirmed' not in st.session_state:
    st.session_state.dataConfirmed = False   
file_path = os.path.join(os.path.dirname(__file__), 'files/datiGenerali.csv')
#leggi dati di input da DatiGenerali.csv
with open('files/DatiGenerali.csv') as file_gen:
    dfgen = pd.read_csv(file_gen, index_col=False)   # lettura file e creazione
    dfgen.drop(dfgen.columns[dfgen.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)
st.session_state.JAccount = dfgen.loc[0,'JAccount']
st.session_state.Project = dfgen.loc[0,'Project']
st.session_state.Location = dfgen.loc[0,'Location']
st.session_state.Fwx = dfgen.loc[0,'Fwx']
st.session_state.Mwy = dfgen.loc[0,'Mwy']
st.session_state.Fwy = dfgen.loc[0,'Fwy']
st.session_state.Mwx = dfgen.loc[0,'Mwx']
st.session_state.acc = dfgen.loc[0,'acc']
st.title('📝General data')
col1, col2 = st.columns([1,3])
JAccount = col1.text_input('Job Account', value = st.session_state.JAccount)
Project = col2.text_input('Project', value = st.session_state.Project)
Location = col2.text_input('Location', value = st.session_state.Location)
st.write('---')
st.subheader ('🌬️Wind actions on the equipment ')
st.write('(At the top of footing)')
st.write('**Wind in X direction**')
col1, col2 = st.columns([1,1])
Fwx = col1.number_input('Wind Force X [kN]', min_value=0.0, step=0.1, value= st.session_state.Fwx )
Mwy = col2.number_input('Wind Moment @ Y [kN*m]', min_value=0.0, step=0.1, value= st.session_state.Mwy )
st.write ('**Wind in Y direction**')
col1, col2 = st.columns([1,1])
Fwy = col1.number_input('Wind Force Y [kN]', min_value=0.0, step=0.1, value= st.session_state.Fwy )
Mwx = col2.number_input('Wind Moment @ X [kN*m]', min_value=0.0, step=0.1, value= st.session_state.Mwx )
st.write('---')
st.subheader('🫨Seismic data')
col1, col2 = st.columns([1,1])
acc = col1.number_input('Sesimic acceleration [a/ag]', min_value=0.0, step=0.1,  value= st.session_state.acc)
col1, col2, col3 = st.columns([1,1,1])
checkbox_state = col1.checkbox('Data confirmed', value=st.session_state.dataConfirmed)
if checkbox_state:
    #os.remove("files/DatiGenerali.csv")
    st.session_state['dataGen'] = [{
        'JAccount': JAccount,
        'Project': Project,
        'Location': Location,
        'Fwx': Fwx,
        'Mwy': Mwy,
        'Fwy': Fwy,
        'Mwx': Mwx,
        'acc': acc
    }]
    st.session_state.dataConfirmed = True
    st.success('Data confirmed and stored successfully! Double click to untick checkbox.')
    df = pd.DataFrame(st.session_state['dataGen'])
    st.subheader('Summary of general data')
    st.dataframe(df, hide_index= True)
    df.to_csv("files/DatiGenerali.csv")   # salva dati su DatiPiping  

else:
    
    st.session_state.dataConfirmed = False
    st.warning('Data not confirmed! Double click to tick checkbox and confirm input data.')

