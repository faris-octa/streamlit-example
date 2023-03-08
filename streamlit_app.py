import streamlit as st
# from streamlit_modal import Modal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from st_aggrid import AgGrid
from datetime import date
import pandas as pd
import numpy as np
import time

# define variable for json and sheet name
json_file = {
  "type": "service_account",
  "project_id": "booming-triode-305701",
  "private_key_id": "7b37e82be7a3561581af53847cc46c87a4cf732b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7XqhgFL8zutBP\nXfcZD3woDxEBaQZebk6bAY1ZXHO/0iM3dhHiC8bLBHyW8/dnj6IX1EzkFmmdl+M+\nEn8Kd1pqkDYdmwEa4R0tYjJ0xS81A3OhtdCIBAuJ1gtU4OuEqNOA/A5uMBXiE1/E\nEvGA23cM/aY0SMCQlP7sg7F0jySQAwWm8eXCkeGdBn6zTyXqzUu2/emTFRLa5YTQ\nyn4Jo4O2U5yvtD789yBrMf+FgoT1pHTWSnTGiwbpqGS91xhegS4Hx6oSEn2Hx3xh\n2LkbrbdSeyGTiK93yWO29GxnCJgeIcTQ3YhUVyrjuMkr+IqVnMDg6fGVMyTe2vkT\nkCYl0Fn3AgMBAAECggEARa9gw8sziVOzYbE60zE1JdjkpDehTMGNroyXO2LtEaxf\nuKLK590lZCAZDjNSEkwTJvWoWzQSt6/jrhRG92eIUxWrartZX9vVdCmPRmqHshnE\niaILGmsWt37J3BmCvmXjs5cK7uQnX1uBRHUfKKN21XgItm1QYPVpEiGwf/80w/IY\npWT86ghkTsHjO3m5M2/4lNGyqFVRf8UmztcIUxq3rmA/2VSrI/zSOfgaMAzctXw9\nomThZSuQMRPCCexLpcMwXqnj7XT1u0ngOAmLwkBeC3U51PlZ57uBQHLnHzMW7Jne\n2UNVnuqrr924yY3sekO2PiDf6yYCfFOrCS6sLnkWQQKBgQDnD1xorwZtVQr8X138\n+YUFj4u6vodmbTvkqyXGtSjL7tHnHrcJW6cTa1NuavnhV2DQ1t5DYlg6I9wCj8W3\nvSQX26D6tscAks5Euc9lmKrHplykPJ7dbgSh/BRccfdVt1mO920v1vylWMzaGpP/\n75WWp2ztZGZqWtaP4J+rXiAWBwKBgQDPmAzHQj+Ttw9hgJHZQS1CmISx2CVL6ljq\nG/YaJAdS4EYCAvZQiCs+/EYf6/kzx1eK45AzDOMxov3yKIov+tchSUM/NmYnOpdr\nL1wHaMCuIq8/1PU3rL0/TeUA1PfR4CrW2S9Spblbe6gOgCD8aj4x/5roS1+AU1hA\npgNkRUUgkQKBgQCjWLWwgAOgKV3x2o28eL20l61loKpiG9kaqG+1UX785OHZbVpi\nsDumO9qoldH/n2EfYreQlabfu1gfK3rQkVNB1o+wjqSS4DYYWe+n2Ezrhc26geyh\nh9SYm3fdfugm3c7fhkXXazoCvotbqSx14+8xqT0VekP47iz/XAIlCQ7P4wKBgFw/\nEp6Qn7PCCsGm4iiKP9Rx9bUZeSlMz4noNunSzLZVFobaTh3nBGCOtZKFx0zs7ce3\n62Hj/ikWZoXu4ckETAhsh8dVIvuXm6VzfA+GyugWXY2d0gGVbtrsgDBocl7+n8qs\n48xz+/Pc9QbMhNvlUhHhpTJIG/3oCzVfD+7EoT0hAoGAUXeHlfDU6oxzuqy5RSFS\nvM6D3MOc9aSuLp7WO+eAr4/MgTvsPidch0iLUBa6n9kptlrFGTF+VTSkhSSJJXsx\nrAzRhDeistaoOEuGMjPewCtc5zRGgykY7h9m93pchwK95zJNS2XPFBwNiVHRORAW\n3KzG6qH3s0fzQaJGl68dymo=\n-----END PRIVATE KEY-----\n",
  "client_email": "streamlit@booming-triode-305701.iam.gserviceaccount.com",
  "client_id": "117098514051524851403",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlit%40booming-triode-305701.iam.gserviceaccount.com"
}
worksheet_name = 'Sheet1'

# Credentials making
creds = ServiceAccountCredentials.from_json_keyfile_name(json_file)
client = gspread.authorize(creds) # login as client
spreadsheet = client.open('OVEN') # open spreadsheet
worksheet = spreadsheet.worksheet(worksheet_name) # choose worksheet

# Mengambil semua data pada worksheet dan buat menjadi dataframe
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])
df.index = np.arange(0, len(df))

# web panel
st.set_page_config(page_title="Faris' Webpage", page_icon=":tada:", layout="wide")

# Header
with st.container():
    st.header("Oven 45\xb0C")
    st.subheader("Realtime Sample Tracking")

# session state
# "st.session_state object:", st.session_state  

# Menampilkan data sebagai tabel menggunakan Streamlit
st.dataframe(df[1:], use_container_width=True)
# AgGrid(df, editable=True)


# Fitur tambah dan hapus baris
col1, col2 = st.columns(2)

with col1:
    with st.expander("Tambah sampel baru"):
        with st.form("add_sample", clear_on_submit=True):
            nama_sampel = st.text_input('Nama Sampel')
            pic = st.text_input('PIC')
            input_date = st.date_input("Tanggal Masuk")
            output_date = st.date_input("Tanggal Keluar")

            submitted = st.form_submit_button("Submit")
        if submitted:
            worksheet.append_row([nama_sampel, pic.title(), input_date.isoformat(), output_date.isoformat()])
            st.success('Data berhasil ditambahkan')
            time.sleep(2)
            st.experimental_rerun()

with col2:
    with st.expander("Keluarkan sampel"):
        col_1, col_2 = st.columns([1,2])
        with col_1:
            pic = st.selectbox('choose PIC',
                               options = df['PIC'].unique(),
                               format_func=lambda x: 'Select...' if x == ' ' else x,
                               key='pic_to_remove')
            
        with col_2:
            sampel = st.selectbox('choose sample',
                                  options=df[df['PIC']==pic].index.to_list(),
                                  format_func=lambda x: '' if x == 0 else x,
                                  disabled = st.session_state.pic_to_remove == ' ',
                                  key='sample_to_remove')
        
        submitted = st.button("Submit")
        if submitted:
            if pic != ' ':
                worksheet.delete_row(sampel+2)
                st.success(f'berhasil mengeluarkan {sampel} milik {pic}')
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error('silahkan isi form di atas terlebih dahulu')
