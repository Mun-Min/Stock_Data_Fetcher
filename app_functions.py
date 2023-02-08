import streamlit as st
import io
import pandas as pd 

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8'), df.to_json().encode('utf-8')