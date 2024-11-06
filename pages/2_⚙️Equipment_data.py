import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if 'newFlag' not in st.session_state:
    st.session_state.newFlag = 'new'
if 'addphaseStarted' not in st.session_state:
    st.session_state.addphaseStarted = False    
if 'dataEqp' not in st.session_state:
    st.session_state['dataEqp'] = []

st.title('⚙️Vibating machine data')

power = st.number_input('Motor Power [kW]')
st.subheader('Machine elements')
col1,col2,col3 = st.columns([2,0.5,1])
options = ['Pump', 'Motor', 'Coupling', 'Baseplate','Other']
item = col1.selectbox('Select item', options= options)

# Custom CSS per allineare le opzioni su una riga
st.markdown(
    """
    <style>
    .stRadio > div {
        flex-direction: row;
    }
    .col3Radio > div {
        flex-direction: row;
    }

    </style>
    """,
    unsafe_allow_html=True
    )

tipoEqp  = col3.radio("Equipment type", options= ['Dynamic', 'Static'], index= 0)

nome_eqp = st.text_input('Equipment name', value = item)


col1, col2, col3, col4,col5,col6 = st.columns([1.5,1,1,1,1,1])
pW = col1.number_input ('Weight [kg]', min_value= 0.00)
rotMass = col2.number_input('Rot.mass [kg]', value= 0.4*pW, min_value= 0.00)
veloc = col3.number_input('veloc.[RPM]', min_value = 0.00)
pcx = col4.number_input('CoG X [mm]')
pcy = col5.number_input('CoG Y [mm]')
pcz = col6.number_input('CoG Z [mm]')



if nome_eqp == 'Motor':
    power_value = power
else:
    power_value = power

if tipoEqp == 'Dynamic':
    velocity_value = veloc
else:
    velocity_value = 0.0

add_eqp = st.button('Add item')
if add_eqp:
    
    # Aggiungi l'elemento alla lista
    st.session_state['dataEqp'].append({
        'name': nome_eqp,
        'type': tipoEqp,
        'power': power_value,
        'weight': pW,
        'rot_mass': rotMass,
        'velocity': velocity_value,
        'CoG_X': pcx,
        'CoG_Y': pcy,
        'CoG_Z': pcz
    })
    
    st.success('Item added successfully!')
    st.session_state.addphaseStarted = True 

   
if st.session_state.addphaseStarted == True:
    df = pd.DataFrame(st.session_state['dataEqp'])
    st.subheader('Summary of machine data')

    st.dataframe(df, hide_index= True)
    df.to_csv("files/DatiEqp.csv")   # salva dati su DatiPiping

if st.session_state.newFlag == 'stored':
    df = pd.read_csv('files/DatiEqp.csv', index_col=False)   # lettura file e creazione
    st.dataframe(df, hide_index= True)


























