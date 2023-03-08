import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
import numpy as np
import time

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ],
)
worksheet_name = 'Sheet1'
client = gspread.authorize(credentials) # login as client
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
