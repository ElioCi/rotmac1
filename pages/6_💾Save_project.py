import streamlit as st
from generaFileUnito import SalvaDati

# save data in local drive
st.title('Save Project')

fileName = st.text_input('File name', value= 'vm1_data')
fileNamePath = fileName + '.csv'

if st.button('Save'):
    SalvaDati(fileNamePath)



