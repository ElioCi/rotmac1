import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


if 'newFlag' not in st.session_state:
    st.session_state.newFlag = 'new'
if 'dataFootingConfirmed' not in st.session_state:
    st.session_state.dataFootingConfirmed = False
if 'dataFooting' not in st.session_state:
    st.session_state.dataFooting = []
if 'dataConfirmed' not in st.session_state:
    st.session_state.dataConfirmed = False


if 'a' not in st.session_state:
    st.session_state.a = 0.00
if 'b' not in st.session_state:
    st.session_state.b = 0.00    
if 'Lx' not in st.session_state:
    st.session_state.Lx = 0.00
if 'Ly' not in st.session_state:
    st.session_state.Ly = 0.00
if 'Hz' not in st.session_state:
    st.session_state.Hz = 0.00
if 'Elev' not in st.session_state:
    st.session_state.Elev = 0.00    
if 'allP' not in st.session_state:    
    st.session_state.allP = 100.00
if 'gconc' not in st.session_state:
    st.session_state.gconc = 25.00

#leggi dati di input da DatiFooting.csv

with open('files/DatiFooting.csv') as file_footing:
    dffond = pd.read_csv(file_footing)   # lettura file e creazione
    dffond.drop(dffond.columns[dffond.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

st.session_state.a = dffond.loc[0,'a']
st.session_state.b = dffond.loc[0,'b']
st.session_state.Lx = dffond.loc[0,'Lx']
st.session_state.Ly = dffond.loc[0,'Ly']
st.session_state.Hz = dffond.loc[0,'Hz']
st.session_state.Elev = dffond.loc[0,'Elev']
st.session_state.allP = dffond.loc[0,'allP']
st.session_state.gconc = dffond.loc[0,'gconc']
st.title('Footing data')

st.subheader('Skid of machine dimensions (plan)')
col1,col2 = st.columns(2)
a = col1.number_input('Length [m]', key='Lskid', value=st.session_state.a)
b = col2.number_input('Width [m]', key='Wskid',value=st.session_state.b)


st.subheader('Block of foundation')
col1, col2, col3, col4 = st.columns(4)
Lx = col1.number_input('Length [m]', value=st.session_state.Lx)
Ly = col2.number_input('Width [m]', value=st.session_state.Ly)
Hz = col3.number_input('Height [m]',value=st.session_state.Hz)
Elev = col4.number_input('Elev. AG [m]', value=st.session_state.Elev)

allP = col1.number_input('Soil allowable pressure [kN/m^2]', value=st.session_state.allP)
gcls = col2.number_input('Concrete spec. weight [kN/m^3]', value=st.session_state.gconc)

chkFooting_state = st.checkbox('Data confirmed', value=st.session_state.dataFootingConfirmed)


if chkFooting_state:

    st.session_state['dataFooting'] = [{
    'a': a,
    'b': b,
    'Lx': Lx,
    'Ly': Ly,
    'Hz': Hz,
    'Elev': Elev,
    'allP': allP,
    'gconc': gcls
    }]
    st.session_state.dataFootingConfirmed = True
    st.success('Data confirmed and stored successfully! Double click to untick checkbox.')
    df = pd.DataFrame(st.session_state['dataFooting'])
    st.subheader('Summary of footing data')
    st.dataframe(dffond, hide_index= True) 
    df.to_csv("files/DatiFooting.csv")   # salva dati su DatiFooting
   
else:
    
    st.session_state.dataFootingConfirmed = False
    st.warning('Data not confirmed! Double click to tick checkbox and confirm input data.')



st.write('---')
# disegno blocco di fondazione
dx = (Lx-a)/2
dy = (Ly-b)/2
# Creazione della figura 1 e della figura 2 - vista in pianta ed in sezione
fig1, ax1 = plt.subplots(figsize=(10, 10))  # Dimensione della figura per la vista in pianta
fig2, ax2 = plt.subplots(figsize= (10,10))

blocco1 = patches.Rectangle([0,0], width= Lx, height= Ly, hatch='/')
skid = patches.Rectangle([dx,dy], width= a, height= b, linewidth=1, edgecolor='red', facecolor='red', alpha=0.3)
blocco2 = patches.Rectangle([0,0], width= Lx, height= Hz, hatch='/')

ax1.add_patch(blocco1)
ax1.add_patch(skid)
ax2.add_patch(blocco2)

# Impostazione automatica della scala (i limiti vengono scelti automaticamente)
ax1.set_xlim([0, Lx+0.5])
ax1.set_ylim([0, Ly+0.5])

ax2.set_xlim([-0.3, Lx+0.5])
ax2.set_ylim([0, Hz+0.5])

# Impostare lo stesso rapporto di scala sugli assi X e Y
ax1.set_aspect('equal', 'box')  # Rapporto 1:1 tra gli assi
ax2.set_aspect('equal', 'box')  # Rapporto 1:1 tra gli assi

# Rimuovere il contorno del grafico e i tick
ax1.set_frame_on(False)   # Disabilita il rettangolo che racchiude il grafico
ax2.set_frame_on(False) 
# Rimuovere i tick sugli assi ma lasciare le etichette numeriche
#ax.tick_params(axis='both', which='both', length=0)  # Rimuove la lunghezza dei tick, quindi niente linee
ax1.tick_params(axis='both', which='both', length=0, labelsize=14)  # Aumenta la dimensione del carattere delle quote
ax2.tick_params(axis='both', which='both', length=0, labelsize=14)
# Impostare solo le etichette delle quote dei due lati
ax1.set_xlabel('X (m)', fontsize= 14)
ax1.set_ylabel('Y (m)', fontsize= 14)

ax2.set_xlabel('X (m)', fontsize= 14)
ax2.set_ylabel('Z (m)', fontsize= 14)


col1, col2 = st.columns(2)
lbl1 = "Plan view"
ax1.text(Lx/2, Ly+0.5, lbl1, ha='center', va='top', fontsize=24)
lbl2 = "Section view"
ax2.text(Lx/2, Hz+0.5, lbl2, ha='center', va='top', fontsize=24)
# Linea orizzontale per terreno
ax2.plot([-0.3, 0], [Hz-Elev, Hz-Elev], color='green', linestyle='solid', linewidth=1, label='')
ax2.plot([Lx, Lx+ 0.5], [Hz-Elev, Hz-Elev], color='green', linestyle='solid', linewidth=1, label='')
ax2.text(Lx + 0.25, Hz - Elev + 0.1, 'soil', color='green', fontsize=14)  # Posizionamento manuale

if Lx != 0 and Ly !=0 and Hz !=0:
    col1.pyplot(fig1)
    col2.pyplot(fig2)


