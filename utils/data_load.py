import pandas as pd
import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
import io


def decrypt_data(filepath):
    key = st.secrets['key']

    fernet = Fernet(key)
    with open(filepath, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)
    df = pd.read_csv(io.StringIO(decrypted.decode('utf-8')))
    return df
    # return decrypted


def get_classdata(df, input_class, input_terms):
    classdata = df[(df['Class'] == input_class)
                   & (df['Term'].isin(input_terms))]
    return classdata


def get_filtered_assignment_classdata(df, chosenclass, years,
                                      completion_status, display_status):
    return df[(df['Class'] == chosenclass) & (df['Year'].isin(years)) &
              (df['Completion Status'].isin(completion_status)) &
              (df['Display Status'].isin(display_status))]
