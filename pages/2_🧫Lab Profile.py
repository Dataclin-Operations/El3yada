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











########################################################
#                       Data                          #
########################################################
patients_df = pd.DataFrame(fetch_data("patients"))
blood_df = pd.DataFrame(fetch_data("blood_test"))
hormon_df = pd.DataFrame(fetch_data("hormonal_test"))
tumer_marks_df = pd.DataFrame(fetch_data("tumor_marks"))
mutation_analysis_df = pd.DataFrame(fetch_data("mutation_analysis"))


st.session_state["patients_df"] = patients_df
st.session_state["blood_df"] = blood_df
st.session_state["hormonal_df"] = hormon_df
st.session_state["tumer_marks_df"] = tumer_marks_df
st.session_state["mutation_analysis_df"] = mutation_analysis_df






def make_title():
    col1,col2 = st.columns([4, 4])
    with col1:
        colored_header(
    label="Select Patient for test information",
    description="",
    color_name="blue-70")


if 'tests' not in st.session_state:
    st.session_state.tests = ['']

if 'results' not in st.session_state:
    st.session_state.results = ['']




def add_buttons():
    st.session_state.results.append('')
    st.session_state.tests.append('')


def remove_buttons():
    if len(st.session_state.tests) > 1:
        st.session_state.tests.pop()
    if len(st.session_state.results) > 1:
        st.session_state.results.pop()

# Function to add a new language input field
def add_test():
    st.session_state.tests.append('')

    
# Function to add a new language input field
def add_result():
    st.session_state.results.append('')

# Function to remove the last language input field
def remove_test():
    if len(st.session_state.tests) > 1:
        st.session_state.tests.pop()

# Function to remove the last language input field
def remove_result():
    if len(st.session_state.results) > 1:
        st.session_state.results.pop()







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

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⚡"):
                fetch_data.clear()
                st.rerun()

        #----------------------------- Make Tabs--------------------------------------
        maintabs = st.tabs(["Check Lab Results", "Add Lab Results"])

                                #----------------------------------------------------------------#
                                #----------------------------------------------------------------#
                                #                        Check results                           #    
                                #----------------------------------------------------------------#
                                #----------------------------------------------------------------#

        with maintabs[0]:
            results_tabs = st.tabs(["Blood Test", "Hormonal Tests", "Tumor Markers","Mutation Analysis"])
            
    

        #with results_tabs[0]:
            #tabs = st.tabs(["Blood Test", "Hormonal Tests", "Tumor Markers","Mutation Analysis"])
            
            # ----------------------------------Blood Test----------------------------------
            with results_tabs[0]:
                make_title()
                col1, col2, col3 = st.columns([1.3,2,2])
                with col1:
                    
                    blood_patient_id = st.selectbox("Patient Id", [""] + sorted(set([""] + st.session_state["blood_df"]["patient_id"].values)), key="blood")
                with col2:

                    all_blood_dates = ["All"] + [i for i in blood_df[blood_df["patient_id"] == blood_patient_id]["test_date"]]
                    blood_test_date = st.selectbox("Test Date", all_blood_dates, key="blooddate")
                if blood_patient_id == "":
                    test_data_blood = blood_df[blood_df["patient_id"] == ""]
                elif blood_test_date == "All":
                    test_data_blood = blood_df[blood_df["patient_id"] == blood_patient_id]
                else:
                    test_data_blood = blood_df[(blood_df["patient_id"] == blood_patient_id) & (blood_df["test_date"] == blood_test_date)]


                patient_blood_lab(blood_patient_id, test_data_blood, "Blood Test")

            # ----------------------------------Hormon Test----------------------------------
            with results_tabs[1]:
                make_title()
                col1, col2, col3 = st.columns([1.3,2,2])
                with col1:
                    hormon_patient_id = st.selectbox("Patient Id", [""] + sorted(set([""] + st.session_state["hormonal_df"]["patient_id"].values)), key="hormon")
                with col2:
                    all_hormon_dates = ["All"] + [i for i in hormon_df[hormon_df["patient_id"] == hormon_patient_id]["test_date"]]
                    hormon_test_date = st.selectbox("Test Date", all_hormon_dates, key="hormondate")

                if hormon_patient_id == "":
                    test_data_hormon = hormon_df[hormon_df["patient_id"] == ""]

                elif hormon_test_date == "All":
                    test_data_hormon = hormon_df[hormon_df["patient_id"] == hormon_patient_id]
                else:
                    test_data_hormon = hormon_df[(hormon_df["patient_id"] == hormon_patient_id) & (hormon_df["test_date"] == hormon_test_date)]

                patient_hormon_lab(hormon_patient_id, test_data_hormon, "Hormonal Test")


            with results_tabs[2]:
                make_title()
                #tumer_marks_df

                col1, col2, col3 = st.columns([1.3,2,2])
                with col1:
                    tumer_patient_id = st.selectbox("Patient Id", [""] + sorted(set([""] + st.session_state["tumer_marks_df"]["patient_id"].values)), key="tumer_marks")
                with col2:
                    all_tumer_dates = ["All"] + [i for i in tumer_marks_df[tumer_marks_df["patient_id"] == tumer_patient_id]["test_date"]]
                    tumer_test_date = st.selectbox("Test Date", all_tumer_dates, key="tumerdate")

                if tumer_patient_id == "":
                    test_data_tumer = tumer_marks_df[tumer_marks_df["patient_id"] == ""]
                elif tumer_test_date == "All":
                    test_data_tumer = tumer_marks_df[tumer_marks_df["patient_id"] == tumer_patient_id]
                else:
                    test_data_tumer = tumer_marks_df[(tumer_marks_df["patient_id"] == tumer_patient_id) & (tumer_marks_df["test_date"] == tumer_test_date)]

                patient_tumer_lab(tumer_patient_id, test_data_tumer, "Tumer Marks Test")
            with results_tabs[3]:
                make_title()
                #mutation_analysis_df

                col1, col2, col3 = st.columns([1.3,2,2])
                with col1:
                    mutation_patient_id = st.selectbox("Patient Id", [""] + sorted(set([""] + st.session_state["mutation_analysis_df"]["patient_id"].values)), key="mutation_marks")
                with col2:
                    all_mutation_dates = ["All"] + [i for i in mutation_analysis_df[mutation_analysis_df["patient_id"] == mutation_patient_id]["test_date"]]
                    mutation_test_date = st.selectbox("Test Date", all_mutation_dates, key="mutationdate")

                if mutation_patient_id == "":
                    test_data_mutation = mutation_analysis_df[mutation_analysis_df["patient_id"] == ""]
                if mutation_test_date == "All":
                    test_data_mutation = mutation_analysis_df[mutation_analysis_df["patient_id"] == mutation_patient_id]
                else:
                    test_data_mutation = mutation_analysis_df[(mutation_analysis_df["patient_id"] == mutation_patient_id) & (mutation_analysis_df["test_date"] == mutation_test_date)]

                patient_mutation_lab(mutation_patient_id, test_data_mutation, "Mutation Analysis Test")


                                #----------------------------------------------------------------#
                                #----------------------------------------------------------------#
                                #                       Add new results                          #    
                                #----------------------------------------------------------------#
                                #----------------------------------------------------------------#


        with maintabs[1]:
            add_tabs = st.tabs(["Blood Test", "Hormonal Tests", "Tumor Markers","Mutation Analysis"])

            with add_tabs[0]:
                #st.write(st.session_state.tests[0] == "")
                with st.form("add_blood_test"):
                    col1, col2, col3 = st.columns([2,1.5,1.5])
                    with col1:
                        patient_id_blood = st.selectbox("Patient Id", [""] + sorted(set([""] + st.session_state["patients_df"]["patient_id"].values)), key="patients")
                    with col2:
                        test_name_blood = st.text_input("Test Name 💥")
                    with col3:
                        test_date_blood = st.date_input("Test Date 💥", value=None)
                    #st.write("Test Results")
                    col1, col2, col3 = st.columns([2,2,4])
                    with col1:
                        for i, test in enumerate(st.session_state.tests):
                            st.session_state.tests[i] = st.text_input(f"Lab {i + 1}", value=test, key=f"tests_{i}")
                    with col2:
                        for i, result in enumerate(st.session_state.results):
                            st.session_state.results[i] = st.text_input(f"Value {i + 1}", value=result, key=f"results_{i}")
                    col1, col2, col3, col4 = st.columns([1,1.5,3, 2])
                    with col1:
                        st.form_submit_button("Add Test", on_click=add_buttons)
                    with col2:
                        st.form_submit_button("Remove Last Test", on_click=remove_buttons)
                    # with col4:
                    if st.form_submit_button("Submit Results"):
                        
                        if ( 
                            not patient_id_blood or 
                            patient_id_blood == "" or
                            not test_name_blood or 
                            not test_date_blood or 
                            st.session_state.tests[0] == "" or
                            st.session_state.results[0] == ""
                            ):
                            st.error("Please fill all mandatory fields with 💥 sign inside it.")

                        else:
                            lab_values = dict(zip(st.session_state.tests, [int(i) for i in st.session_state.results]))
                            add_blood_test(patient_id_blood, str(test_date_blood),test_name_blood,lab_values)
                            placeholder = st.empty()
                            placeholder.success(f"Lab Results added successfully.")
                            time.sleep(1.5)
                            placeholder.empty()
                            fetch_data.clear()
                            st.session_state["blood_df"] = pd.DataFrame(fetch_data("blood_df"))  
                            st.session_state["patients_df"] = pd.DataFrame(fetch_data("patients")) 
                            st.rerun()



            with add_tabs[1]:
                with st.form("add_hormon_test"):
                    col1, col2, col3 = st.columns([2,1.5,1.5])
                    with col1:
                        patient_id_hormon = st.selectbox("Patient Id 💥", [""] + sorted(set([""] + st.session_state["patients_df"]["patient_id"].values)), key="patients_hormon")
                    with col2:
                        test_date_hormon = st.date_input("Test Date 💥", value=None)
                    # with col3:
                    #     test_name_blood = st.text_input("Test Name 💥")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        estrogen_levels = st.number_input("Estrogen Levels 💥", value = int())
                        progesterone_levels = st.number_input("Progesterone Levels 💥", value= int())
                    with col2:
                        testosterone_levels = st.number_input("Testosterone Levels 💥", value= int())
                        thyroid_tsh = st.number_input("Thyroid TSH", value= int())

                    with col3:
                        luteinizing_hormone = st.number_input("Luteinizing Hormone", value= int())
                        follicle_stimulating_hormone = st.number_input("Follicle Stimulating Hormone", value=int())
                    with col4:
                        thyroid_t3 = st.number_input("Thyroid T3", value= int())
                        thyroid_t4 = st.number_input("Thyroid T4 Levels", value= int())
                    hormons_notes = st.text_input("Notes 💥")

                    
                    if st.form_submit_button("Submit Results"):
                        if ( 
                            not patient_id_hormon or 
                            patient_id_hormon =="" or 
                            not test_date_hormon or
                            estrogen_levels ==0 or
                            testosterone_levels ==0 or
                            progesterone_levels ==0 
                            ):
                            st.error("Please fill all mandatory fields with 💥 sign inside it.")

                        else:
                            add_hormon_test(patient_id_hormon, str(test_date_hormon),
                                            estrogen_levels, progesterone_levels, luteinizing_hormone,follicle_stimulating_hormone,
                                            testosterone_levels, thyroid_tsh, thyroid_t3, thyroid_t4,hormons_notes
                                            )
                            placeholder = st.empty()
                            placeholder.success(f"Lab Results added successfully.")
                            time.sleep(1.5)
                            placeholder.empty()
                            fetch_data.clear()
                            st.session_state["hormonal_df"] = pd.DataFrame(fetch_data("hormonal_test"))  
                            st.session_state["patients_df"] = pd.DataFrame(fetch_data("patients")) 
                            st.rerun()

            
            
            
            with add_tabs[2]:
                with st.form("add_tumor_marks"):
                    col1, col2, col3 = st.columns([5,3, 2])
                    with col1:
                        patient_id_tumor = st.selectbox("Patient Id 💥", [""] + sorted(set([""] + st.session_state["patients_df"]["patient_id"].values)), key="patients_tumor")
                    with col2:
                        test_date_tumor = st.date_input("Test Date 💥", value=None)
                    # with col3:
                    #     test_name_blood = st.text_input("Test Name 💥")
                    col1, col2, col3, col4, col5, col6 = st.columns([2,0.2,2,0.2,2,1.8])
                    with col1:
                        ca_15_3 = st.number_input("ca_15_3 💥", value = int())
                        ca_27_29 = st.number_input("ca_27_29 💥", value= int())
                    with col3:
                        carcinoembryonic_antigen = st.number_input("carcinoembryonic_antigen 💥", value= int())
                        her2_neu = st.selectbox("her2_neu 💥", ["", "Negative", "Positive"])

                    with col5:
                         muc1= st.number_input("muc1 💥", value= int())

                    if st.form_submit_button("Submit Results"):
                        if ( 
                            not patient_id_tumor or 
                            patient_id_tumor == "" or 
                            not test_date_tumor or
                            ca_15_3 ==0 or
                            ca_27_29 ==0 or
                            carcinoembryonic_antigen ==0 or
                            her2_neu =="" or
                            muc1 ==0 
                            ):
                            st.error("Please fill all mandatory fields with 💥 sign inside it.")

                        else:
                            add_tumor_marks(patient_id_tumor, str(test_date_tumor),
                                            ca_15_3, ca_27_29, carcinoembryonic_antigen,her2_neu,
                                            muc1
                                            )
                            placeholder = st.empty()
                            placeholder.success(f"Lab Results added successfully.")
                            time.sleep(1.5)
                            placeholder.empty()
                            fetch_data.clear()
                            st.session_state["tumer_marks_df"] = pd.DataFrame(fetch_data("tumor_marks"))  
                            st.session_state["patients_df"] = pd.DataFrame(fetch_data("patients")) 
                            st.rerun()

            
            with add_tabs[3]:
                with st.form("add_mutation_analysis"):
                    col1, col2, col3 = st.columns([5,3, 2])
                    with col1:
                        patient_id_mutation = st.selectbox("Patient Id 💥", [""] + sorted(set([""] + st.session_state["patients_df"]["patient_id"].values)), key="patients_mutation")
                    with col2:
                        test_date_mutation = st.date_input("Test Date 💥", value=None)
                    # with col3:
                    #     test_name_blood = st.text_input("Test Name 💥")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        bcr_abl_fusion_gene = st.selectbox("BCR ABL Fusion Gene 💥", ["", "true", "false"])
                        bcr_abl_transcript_levels = st.number_input("BCR ABL Transcript Levels 💥", value = float(), format="%.2f")
                    with col2:
                        t315i_mutation = st.selectbox("T315i Mutation 💥", ["", "true", "false"])
                        f317l_mutation = st.selectbox("F317l Mutation 💥", ["", "true", "false"])

                    with col3:
                        e255k_mutation = st.selectbox("E255k Mutation 💥", ["", "true", "false"])
                        g250e_mutation = st.selectbox("G250e Mutation 💥", ["", "true", "false"])
                         

                    with col4:
                        m351t_mutation = st.selectbox("M351t Mutation 💥", ["", "true", "false"])
                        v299l_mutation = st.selectbox("V299l Mutation 💥", ["", "true", "false"])


                    if st.form_submit_button("Submit Results"):
                        if ( 
                            not patient_id_mutation or 
                            patient_id_mutation == "" or 
                            not test_date_mutation  or
                            bcr_abl_fusion_gene == "" or
                            bcr_abl_transcript_levels == 0 or
                            t315i_mutation == "" or
                            f317l_mutation == "" or
                            e255k_mutation == "" or
                            g250e_mutation == "" or
                            m351t_mutation == "" or
                            v299l_mutation == "" 
                            ):
                            st.error("Please fill all mandatory fields with 💥 sign inside it.")

                        else:
                            add_mutation_analysis(patient_id_mutation, str(test_date_mutation),
                                                    bcr_abl_fusion_gene, bcr_abl_transcript_levels, t315i_mutation,f317l_mutation,
                                                    e255k_mutation, g250e_mutation, m351t_mutation, v299l_mutation
                                                        )
                            placeholder = st.empty()
                            placeholder.success(f"Lab Results added successfully.")
                            time.sleep(1.5)
                            placeholder.empty()
                            fetch_data.clear()
                            st.session_state["mutation_analysis_df"] = pd.DataFrame(fetch_data("mutation_analysis"))  
                            st.session_state["patients_df"] = pd.DataFrame(fetch_data("patients"))  
                            st.rerun()














    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
