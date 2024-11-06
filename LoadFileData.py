import streamlit as st
import pandas as pd
import io

# Routine per caricare file dati unico e separare le due sezioni "General Data" e
# "Piping Data" generando i rispettivi CSV sotto files.
def loadData():

    # Funzione per verificare se il file è stato generato da "HeatLoss4"
    def verifica_file(df):

        if 'DatiCaricati' not in st.session_state:
            st.session_state.DatiCaricati = False
            
        # Trova la colonna che contiene "VibratingMachines1"
        colonna_vibMac = [col for col in df.columns if "VibratingMachines1" in col]
        
        if len(colonna_vibMac) == 0:
            # Se non trova la colonna, significa che il file non è stato generato correttamente
            st.warning("File not generated by vibratingMachines1.")
            return None
        else:
            # Estrarre la data e l'ora dalla colonna
            colonna_info = colonna_vibMac[0]
            st.success(f"File correctly generated by vibratingMachines1.")
            
            # Estrai la data e l'ora dal nome della colonna
            data_ora = colonna_info.split(' - ')[1]
            st.write(f"Creation Date & Time: {data_ora}")
            return data_ora

    # Funzione per separare i dati in base alla colonna che contiene "HeatLoss4"
    def separa_dati(df):
        # Trova l'indice della colonna che contiene i separatori
        colonna_s0 = [col for col in df.columns if "VibratingMachines1" in col]
        colonna_s1 = [col for col in df.columns if "separator_1" in col]
        colonna_s2 = [col for col in df.columns if "separator_2" in col]
        colonna_s3 = [col for col in df.columns if "separator_3" in col]
        colonna_s4 = [col for col in df.columns if "separator_4" in col]

        if len(colonna_s1) == 0:
            st.error("No reference to colonna_vuota1 has been found.")
            return None, None
        
        colonnaApp_idx = colonna_s0[0]
        idx0 = df.columns.get_loc(colonnaApp_idx)
        colonna1_idx = colonna_s1[0]  # Nome della colonna "separator_1"
        idx1 = df.columns.get_loc(colonna1_idx)  # Ottieni l'indice numerico della colonna
        colonna2_idx = colonna_s2[0]  # Nome della colonna "separator_2"
        idx2 = df.columns.get_loc(colonna2_idx)  # Ottieni l'indice numerico della colonna
        colonna3_idx = colonna_s3[0]  # Nome della colonna "separator_3"
        idx3 = df.columns.get_loc(colonna3_idx)  # Ottieni l'indice numerico della colonna
        colonna4_idx = colonna_s4[0]  # Nome della colonna "separator_4"
        idx4 = df.columns.get_loc(colonna4_idx)  # Ottieni l'indice numerico della colonna
      
        # Separa i due set di dati
        dati_generali = df.iloc[:, idx0+1: idx1].dropna(how='all')  # Dati fino alla colonna separator_1
        dati_eqp = df.iloc[:, idx1+1: idx2].dropna(how='all')  # Dati dopo separator_1 fino a colonna separator_2
        dati_fond = df.iloc[:, idx2+1: idx3].dropna(how='all')  # Dati dopo separator_2 fino a colonna separator_3
        dati_loads = df.iloc[:, idx3+1: idx4].dropna(how='all')  # Dati dopo separator_3 fino a colonna separator_4
        dati_combs = df.iloc[:, idx4+1:].dropna(how='all')  # Dati dopo la colonna separator_4

        return dati_generali, dati_eqp, dati_fond, dati_loads, dati_combs

    # Carica il file unito tramite uploader
    uploaded_file = st.file_uploader("Select a valid HeatLoss4 data file", type="csv")

    if uploaded_file is not None:
        # Leggi il file caricato in un DataFrame
        df_unito = pd.read_csv(uploaded_file)
        
        # Verifica se il file è stato generato da HeatLoss4
    
        data_ora = verifica_file(df_unito)
    
        if data_ora:
            # Mostra un'anteprima del file solo se la verifica è andata a buon fine
            #st.write("Single File:")
            #st.dataframe(df_unito)

            # Separa i dati
            dati_generali, dati_eqp, dati_fond, dati_loads, dati_combs = separa_dati(df_unito)
            
            if dati_generali is not None and dati_eqp is not None and dati_fond is not None and dati_loads is not None and dati_combs is not None:
                st.session_state.DatiCaricati = True
                dati_generali_vis = dati_generali.loc[:, ~dati_generali.columns.str.contains('^Unnamed')]
                dati_eqp_vis = dati_eqp.loc[:, ~dati_eqp.columns.str.contains('^Unnamed')]
                dati_fond_vis = dati_fond.loc[:, ~dati_fond.columns.str.contains('^Unnamed')]
                dati_loads_vis = dati_loads.loc[:, ~dati_loads.columns.str.contains('^Unnamed')]
                dati_combs_vis = dati_combs.loc[:, ~dati_combs.columns.str.contains('^Unnamed')]
                # Mostra un'anteprima dei dati separati
                st.write("General Data:")
                st.dataframe(dati_generali_vis)
                
                st.write("Equipment Data:")
                st.dataframe(dati_eqp_vis)

                st.write("Footing Data:")
                st.dataframe(dati_fond_vis)  
                
                st.write("Loading Data:")
                st.dataframe(dati_loads_vis)  

                st.write("Combination Factors Data:")
                st.dataframe(dati_combs_vis)  


                # Salva i file CSV localmente o su un percorso remoto
                # In questo esempio, i file vengono salvati localmente
                dati_generali.reset_index(drop=True, inplace=True)
                dati_generali.index = dati_generali.index.astype(int)

                dati_eqp.reset_index(drop=True, inplace=True)
                dati_eqp.index = dati_eqp.index.astype(int)

                dati_fond.reset_index(drop=True, inplace=True)
                dati_fond.index = dati_fond.index.astype(int)

                dati_loads.reset_index(drop=True, inplace=True)
                dati_loads.index = dati_loads.index.astype(int)

                dati_combs.reset_index(drop=True, inplace=True)
                dati_combs.index = dati_combs.index.astype(int)
                
                dati_generali.to_csv("files/DatiGenerali.csv", index=False)
                dati_eqp.to_csv("files/DatiEqp.csv", index=False)
                dati_fond.to_csv("files/DatiFooting.csv", index=False)
                dati_loads.to_csv("files/LoadsCond.csv", index=False)
                dati_combs.to_csv("files/Combs.csv", index=False)
                
                st.success("General & Other Data loaded successfully!")


