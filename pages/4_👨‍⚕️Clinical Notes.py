#==========================================================================#
#                          Import Libiraries
#==========================================================================#
import sys
from streamlit_extras.colored_header import colored_header 
from streamlit_option_menu import option_menu
import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode
import os
from dotenv import load_dotenv  # pip install python-dotenv
import yaml
from yaml.loader import SafeLoader
from streamlit_phone_number import st_phone_number
import time
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
)






from db_functions import *




#==========================================================================#
#                          Authenticator
#==========================================================================#
# with open('./config.yaml', 'r', encoding='utf-8') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    st.secrets['credentials'].to_dict(),
    # st.secrets['credentials'],
    st.secrets['cookie']['name'],
    st.secrets['cookie']['key'],
    st.secrets['cookie']['expiry_days'],
    st.secrets['pre-authorized'],
)






clinical_notes_df = pd.DataFrame(fetch_data("clinical_notes"))
st.session_state["clinical_notes_df"] = clinical_notes_df




#==========================================================================#
#                          Main Application
#==========================================================================#


if __name__ == "__main__":
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)

    if st.session_state["authentication_status"]:
        #make_states()
        logo_path = "./Thelogo.png"  # Replace with the path to your logo image
        st.sidebar.image(logo_path, use_column_width=True)
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col6:
            authenticator.logout()
            # authenticator.logout()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⚡"):
                fetch_data.clear()
                st.rerun()
        df = pd.DataFrame(fetch_data("patients"))
        # st.session_state["patients_df"] = df
        # selected_rows = aggrid_dis(df, "All Patients Information", "", "single")

        col1,col2 = st.columns([4, 3.2])
        with col1:
            colored_header(
        label="Select Patient for clinical information",
        description="",
        color_name="blue-70")
        col1, col2, col3 = st.columns([1.3,2,2])
        with col1:
            clinc_patient_id = st.selectbox("Patient Id", [""] + sorted(set([""] + st.session_state["clinical_notes_df"]["patient_id"].values)), key="clinic")
        with col2:
            all_clinic_dates = ["All"] + [i for i in clinical_notes_df[clinical_notes_df["patient_id"] == clinc_patient_id]["date_of_visit"]]
            clinic_visit_date = st.selectbox("Test Date", all_clinic_dates, key="clinicdate")

        if clinc_patient_id == "":
            test_data_clinical = clinical_notes_df[clinical_notes_df["patient_id"] == ""]
        elif clinic_visit_date == "All":
            test_data_clinical = clinical_notes_df[clinical_notes_df["patient_id"] == clinc_patient_id]
        else:
           test_data_clinical = clinical_notes_df[(clinical_notes_df["patient_id"] == clinc_patient_id) & (clinical_notes_df["date_of_visit"] == clinic_visit_date)]


        patient_clincal_notes(clinc_patient_id, test_data_clinical)#, "Blood Test")

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
