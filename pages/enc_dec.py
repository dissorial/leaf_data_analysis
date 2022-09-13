from io import BytesIO
from cryptography.fernet import Fernet
import streamlit as st
import pandas as pd
import io

# #encryption
# key = st.secrets['key']

# fernet = Fernet(key)

# with open('../data/exports/test.csv', 'rb') as file:
#     original = file.read()

# encrypted = fernet.encrypt(original)

# with open('../data/exports/test.csv', 'wb') as encrypted_file:
#     encrypted_file.write(encrypted)


# #decryption
# dkey = st.secrets['key']

# dkey_fernet = Fernet(dkey)

# with open('../data/exports/test.csv', 'rb') as enc_file:
#     enc = enc_file.read()

# dec = dkey_fernet.decrypt(enc)

# df = pd.read_csv(io.StringIO(dec.decode('utf-8')))

# st.dataframe(df.head())