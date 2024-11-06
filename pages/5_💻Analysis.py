import streamlit as st
import pandas as pd
import csv
from math import sqrt, log, pi, exp
from datetime import datetime
import numpy as np

if 'prot' not in st.session_state:
    st.session_state.prot = False

if 'loadsCond' not in st.session_state:
    st.session_state.loadsCond = []

print ('prot analysis', st.session_state.prot)
if st.session_state.prot == False:
    st.info('unauthorized access')
    st.stop()

st.title ('Calculation')

with open('files/DatiGenerali.csv') as file_gen:
    dfgen = pd.read_csv(file_gen, index_col=False)   # lettura file e creazione
    dfgen.drop(dfgen.columns[dfgen.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

#Lettura dati macchina
with open('files/DatiEqp.csv') as file_eqp:
    dfeqp = pd.read_csv(file_eqp)   # lettura file e creazione
    dfeqp.drop(dfeqp.columns[dfeqp.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

somma_weight = dfeqp['weight'].sum()
if somma_weight == 0:
    st.write('machines weights missing')
    st.stop()

dfeqp['prodotto'] = dfeqp['weight']*dfeqp['CoG_X'] 
somma_X = dfeqp['prodotto'].sum()
dfeqp['prodotto'] = dfeqp['weight']*dfeqp['CoG_Y'] 
somma_Y = dfeqp['prodotto'].sum()
dfeqp['prodotto'] = dfeqp['weight']*dfeqp['CoG_Z'] 
somma_Z = dfeqp['prodotto'].sum()
#baricentro masse riferito al vertice skid inferiore-sinistro
XGW = somma_X/somma_weight
YGW = somma_Y/somma_weight
ZGW = somma_Z/somma_weight

#Lettura dati Fondazione
with open('files/DatiFooting.csv') as file_footing:
    dffond = pd.read_csv(file_footing)   # lettura file e creazione
    dffond.drop(dffond.columns[dffond.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

#Lettura Fattori Combinazioni di carico
with open('files/Combs.csv') as file_Combinazioni:
    dfComb = pd.read_csv(file_Combinazioni)   # lettura file e creazione
    dfComb.drop(dfComb.columns[dfComb.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)



st.write(dfgen)
st.write(dfeqp)
st.write(dffond)
st.write(dfComb)
st.write('---')

a = dffond['a'][0]
b = dffond['b'][0]
Lx = dffond['Lx'][0]
Ly = dffond['Ly'][0]
Hz = dffond['Hz'][0]
Elev = dffond['Elev'][0]
allP = dffond['allP'][0]
gcls = dffond['gconc'][0]

dx = (Lx-a)/2
dy = (Ly-b)/2

if a==0.0 or b==0.0 or Lx ==0.0 or Ly ==0.0 or Hz ==0.0:
    st.write('The geometry must be completely defined. In this moment some value are 0.')
    st.stop()

# centro geometrico fondazione (origine vertice inferire sinistro skid)
XCG = Lx*1000/2-dx*1000
YCG = Ly*1000/2-dy*1000
ZCG = 0.00

# Verifiche eccentricità masse < 5% e rapporto PesoFond/PesoMacchina
ecc_X = abs((XGW-XCG)/(Lx*1000))
ecc_Y = abs((YGW-YCG)/(Ly*1000))
PF = Lx*Ly*Hz*gcls*100  # valore in kg
PM = somma_weight
PT = PF+PM
Ratio = PF/PM

st.subheader('Eccentricity Check')
st.write ('**Eccentricity between center of gravity of masses and center of foundation base**')
st.write('')
st.write ('Ecc_X = ', f" {ecc_X:.2%}")
st.write ('Ecc_Y = ', f" {ecc_Y:.2%}")
if (ecc_X<= 0.05 and ecc_Y <= 0.05):
    st.success('👍 Eccentricity < 5% The check is successfull !')
else:
    st.markdown('<p style="color:red;">👎 Eccentricity > 5% The check failed !</p>', unsafe_allow_html=True)
st.write('')
st.subheader('Weight ratio check')
st.write('**Weight of Machine and Footing**')
st.write('Machine Weight [kg]= ', f"{PM:.2f}")
st.write('Footing Weight [kg]= ', f"{PF:.2f}")
st.write('Total Weight [kg]= ', f"{PF+PM:.2f}")

col1,col2 = st.columns(2)
ratio_weights = PF/PM
#st.write("Ratio = ", f"{PF/PM: .2f}" , "> 3 times machine weight")

if ratio_weights >= 3:
    st.write("Ratio of weights = ", f"{PF/PM: .2f}" , "> 3 times the machine weight.")
    st.success('👍 The check is successfull !')
else:
    st.write("Ratio of weights = ", f"{PF/PM: .2f}" , "< 3 times the machine weight. ")
    st.error('<p style="color:red;">👎 The Check failed !</p>', unsafe_allow_html=True)


# Azioni dinamiche
# a partire dal dataframe dfeqp calcolo il valore di e in micrometri come 25.4*radq(12000/N) 
# poi valuto anche omega (vel angolare) come 2*pigreco*N/60 rad/sec


dfeqp['e'] = 25.4*np.sqrt(12000.0/dfeqp['velocity'])

# Applicazione delle condizioni specifiche per 'Motor'
# Seleziona le righe dove 'name' è 'Motor'
mask_motor = dfeqp['name'] == "Motor"
# Applica np.select solo alle righe selezionate
dfeqp.loc[mask_motor, 'e'] = np.select(
    [
        dfeqp.loc[mask_motor, 'velocity'] <= 1000,
        (dfeqp.loc[mask_motor, 'velocity'] > 1000) & (dfeqp.loc[mask_motor, 'velocity'] <= 1500),
        (dfeqp.loc[mask_motor, 'velocity'] > 1500) & (dfeqp.loc[mask_motor, 'velocity'] <= 3000),
        dfeqp.loc[mask_motor, 'velocity'] > 3000
    ],
    [
        38.0,
        32.0,
        25.0,
        13.0
    ],
    default=dfeqp.loc[mask_motor, 'e']
)

dfeqp['omega'] = 2*pi*dfeqp['velocity']/60.0
dfeqp ['Fdyn_Y'] = dfeqp['e']*dfeqp['omega']**2*dfeqp['rot_mass']*1e-9
dfeqp['Mdyn_btm'] = dfeqp['Fdyn_Y']*(dfeqp['CoG_Z']/1000 + Hz - Elev )

# vento
Fw_Y = dfgen['Fwy'][0]
Mw_X = dfgen['Mwx'][0]


# sisma
coefSismico = dfgen['acc'][0]/100
dfeqp ['Fs_Y'] = dfeqp['weight']*coefSismico   # valore in kN
dfeqp['Ms_btm'] = dfeqp['Fs_Y']*(dfeqp['CoG_Z']/1000 + Hz - Elev )

somma_Fdyn = dfeqp['Fdyn_Y'].sum(skipna= True)
somma_Mdyn = dfeqp['Mdyn_btm'].sum(skipna= True)
somma_FsY = dfeqp['Fs_Y'].sum(skipna= True)
somma_MsX = dfeqp['Ms_btm'].sum(skipna= True)

# short circuit
# Verifica che 'Motor' sia presente nella colonna 'Equipment'
if 'Motor' in dfeqp['name'].values:
  
    # Esegui i calcoli
    dfeqp.loc[mask_motor, 'Starting_Torque'] = dfeqp.loc[mask_motor, 'power']/dfeqp.loc[mask_motor, 'omega']
    dfeqp.loc[mask_motor, 'Short_Circuit'] = 7*dfeqp.loc[mask_motor, 'Starting_Torque']
    # Verifica se ci sono risultati e assegna il valore a Msc
    filtered_series = dfeqp.loc[mask_motor, 'Short_Circuit']
    if not filtered_series.empty:
        Msc = filtered_series.iloc[0]
    else:
        Msc = None  # Oppure assegna un valore di default
    
    filtered_series1 = dfeqp.loc[mask_motor, 'Starting_Torque']
    if not filtered_series1.empty:
        StartingTorque = filtered_series1.iloc[0]
    else:
        StartingTorque = None  # Oppure assegna un valore di default
    #Msc = dfeqp.loc[mask_motor, 'Short_Circuit'].iloc[0]

else:
    st.error("Equipment **'Motor'** is not present between the Equipments.")
    Msc = 0.0  # Oppure assegna un valore di default
    StartingTorque = 0.0


st.subheader('Starting torque and locked-rotor torque')
st.write('Starting torque = ',f"{StartingTorque:.3f} kN*m")
st.write('Locked-rotor torque = ', f"{Msc:.3f} kN*m")
st.write('')
st.write(dfeqp)


# Tabella condizioni di carico alla base del blocco

# Aggiungi l'elemento alla lista
st.session_state['LoadsCond'] = {
    'LC_name': ['DL', 'SCT', 'DYN', 'WIND', 'QUAKE'],
    'N': [PT/100,0.0,0.0,0.0,0.0],
    'SHEAR': [0.0,0.0,somma_Fdyn,Fw_Y,somma_FsY],
    'MOMENT': [0.0,Msc,somma_Mdyn,Mw_X,somma_MsX]
}

dfLoads = pd.DataFrame(st.session_state['LoadsCond'])
dfLoads = dfLoads.fillna('')
st.subheader('Summary of Loads Conditions')
st.dataframe(dfLoads, hide_index= True)
dfLoads.to_csv("files/LoadsCond.csv")   # salva dati su LoadsCond  

# Genera Combinazioni di carico


# Carica i DataFrame dai CSV forniti (puoi caricarli con st.file_uploader se i file sono esterni)
with open('files/Combs.csv') as file_comb:
    df_comb = pd.read_csv(file_comb, index_col=False)   # lettura file e creazione
    df_comb.drop(df_comb.columns[df_comb.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

with open('files/LoadsCond.csv') as file_loads:
    df_loads = pd.read_csv(file_loads, index_col=False)   # lettura file e creazione
    df_loads.drop(df_loads.columns[df_loads.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)



# Rimuovi la colonna Comb_name dal primo dataframe per permettere la moltiplicazione
coeff_matrix = df_comb.set_index('Comb_name')

# Associa i carichi elementari ai rispettivi nomi di colonna (DL, SCT, ecc.)
loads_matrix = df_loads.set_index('LC_name')

# Calcola la matrice prodotto
result = coeff_matrix[['DL', 'SCT', 'DYN', 'WIND', 'QUAKE']].dot(loads_matrix)


# Aggiungi i nomi delle combinazioni
#result.insert(0, 'Comb_name', df_comb['Comb_name'])

# Mostra il risultato
st.subheader("Loading Combinations and Checks")
st.write('Forces in kN, Moments in kN*m, Lenght in m, Pressures in kPa')
result['ecc'] = result['MOMENT']/result['N']
#result['A_Mey'] = (Ly-2*result['ecc'])/(Lx)
result['A_Mey'] = ((Ly-result['ecc']*2)*(Lx-2*0.0))
Area = Lx*Ly
result['Pmax']= result['N']/Area * (1+6*result['ecc']/Ly+6*0.0/Lx) # kPa mantenuta formula completa nel caso di eccX !=0
result['PMey']= result['N']/result['A_Mey']
result['Pallow']= allP
result['Mstab']= result['N']*0.5*Ly

result['Ovr@X'] = result['Mstab']/result['MOMENT']
result['Check'] = np.where((result['Ovr@X'] >= 1.1) & (result['Pmax'] <= result['Pallow']), '👍', '👎')

st.dataframe(result)

# Verifica se esistono valori diversi da '👍'
exists_invalid = (result['Check'] != '👍').any()
if exists_invalid == False:
    st.success('The footing is verified !')
elif exists_invalid == True:
    st.error('The footing is not verified !')

