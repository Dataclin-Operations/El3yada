#==========================================================================#
#                          Import Libiraries
#==========================================================================#
import sys
from datetime import datetime
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


#==========================================================================#
#                          1. Add New Patient
#==========================================================================#


@st.fragment(run_every="10m")
def add_new_patient():
    colored_header(
        label="Add New Patient",
        description="Fill New Patient information then press the Add Patient button",
        color_name="blue-70")

    with st.form("patient_form"):
        min_date = datetime(1960, 1, 1)
        col1, col2, col3, col4, col5 = st.columns([2, 1,0.5,1, 1])
        with col1:
            patient_name = st.text_input("Patient Name 💥")
            
            #st.write(prim_phone["number"])
        with col2:
            patient_gender = st.selectbox("Gender", ["", "Male", "Female"])
        
        with col3:
            patient_age = st.number_input("Age 💥", value=int(), )
            
        with col4:
            birth_date = st.date_input("Birth Date 💥", value=None, min_value=min_date)
        with col5:
            marital_status = st.selectbox("Marital Status 💥", ["", "Married", "Single"])

        col1, col2, col3 = st.columns(3)
        with col1:
            address = st.text_input("Adress 💥", )
            email = st.text_input("Email")
        with col2:
            prim_phone = st_phone_number("Primary Number 💥", placeholder="xxxxxx", default_country="EG")
            emerg_name = st.text_input("Emergency Name")
        with col3:
            secon_phone = st_phone_number("Secondry Number", placeholder="xxxxxxxxxx", default_country="EG")
            emerg_phone = st_phone_number("Emergency Number", placeholder="xxxxxxxxxx", default_country="EG")
        notes = st.text_input("Notes", "")
        
        if st.form_submit_button("Add Patient"):
            #st.write(st.session_state["patients_df"]["primary_phone_number"].values)
            # st.write( prim_phone)
            # st.write(str(birth_date))
            if ( 
                not patient_name or 
                not patient_age or 
                not address or 
                not prim_phone or
                not birth_date or
                not marital_status in ["Married", "Single"] or 
                not patient_gender in ["Male", "Female"]):
                st.error("Please fill all mandatory fields with 💥 sign inside it.")
                

            elif "nationalNumber" not in prim_phone:
                st.error("Primary Number is not correct")
            
            elif ( 
                    prim_phone["nationalNumber"] in st.session_state["patients_df"]["primary_phone_number"].values or 
                    prim_phone["nationalNumber"] in st.session_state["patients_df"]["secondary_phone_number"].values):
                st.warning("Patient already exsits.")

            # elif secon_phone:
            #     if "nationalNumber" not in secon_phone:
            #         st.error("Secondry Number is not correct")

            #     elif (
            #             secon_phone["nationalNumber"] in st.session_state["patients_df"]["primary_phone_number"].values or 
            #             secon_phone["nationalNumber"] in st.session_state["patients_df"]["secondary_phone_number"].values):
            #         st.warning("Patient already exsits.")
                
            else:
                if secon_phone == None:
                    secondry = ""
                else:
                    if "nationalNumber" not in secon_phone:
                        secondry = secon_phone["number"]
                    else:
                        secondry = secon_phone["nationalNumber"]

                add_patient(patient_name, patient_gender, patient_age, str(birth_date), prim_phone["nationalNumber"], secondry, address,
                            emerg_phone,emerg_name, email, marital_status , notes
                        )
                placeholder = st.empty()
                placeholder.success(f"{patient_name} Patient added successfully.")
                time.sleep(1.5)
                placeholder.empty()
                fetch_data.clear()
                st.session_state["patients_df"] = pd.DataFrame(fetch_data("patients"))  
                st.rerun()



#==========================================================================#
#                          2. Edit Exsiting Patient
#==========================================================================#

# Example CSS styles for header


@st.fragment(run_every="10m")
def edit_patient():
    
    colored_header(
    label="Edit Existing Patients",
    description="Select All Patients that you want to edit then edit information and press the submit button",
    color_name="blue-70")
     
    ######## Session state for reset selected rows ##########
    if 'selected_rows' not in st.session_state:
        st.session_state['selected_rows'] = []
    if 'reset' not in st.session_state:
        st.session_state['reset'] = False
    ##########################################################
    gd = GridOptionsBuilder.from_dataframe(st.session_state["patients_df"])
    gd.configure_pagination(enabled=True)
    gd.configure_column("patient_id", header_name="patient_id",minWidth=100, cellStyle={'textAlign': 'center'})
    gd.configure_column("age", header_name="age",maxWidth=75, cellStyle={'textAlign': 'right'})
    gd.configure_column("gender", header_name="gender",maxWidth=110, cellStyle={'textAlign': 'center'})
    gd.configure_column("primary_phone_number", header_name="primary_phone_number",minWidth=120, cellStyle={'textAlign': 'center'})
    gd.configure_column("secondary_phone_number", header_name="secondary_phone_number",minWidth=120, cellStyle={'textAlign': 'center'})
    gd.configure_column("emergency_phone_number", header_name="emergency_phone_number",minWidth=120, cellStyle={'textAlign': 'center'})
    gd.configure_default_column(editable=False,groupable=False,
                                minWidth=200,
                                 filter=True,autoSize=True,
                                 resizable=True,
                                 headerStyle={'width':'20000px','textAlign': 'center', 'fontSize': '56px', 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': 'red'},  # Styling for header
                                 cellStyle={'textAlign': 'left'}
                                )
   
    gd.configure_side_bar()





    gd.configure_pagination(enabled=True)
    
    

    gd.configure_selection(selection_mode='multiple',use_checkbox=True)
    gd.configure_side_bar()
    gridoptions = gd.build()

    ######## Session state for reset selected rows ##########
    if st.session_state['reset'] == True:
        st.session_state['selected_rows'] = []  # Clear the selection
        st.session_state['reset'] = False
        st.rerun()
    #################################################################
# Display the custom CSS
    grid_table = AgGrid(st.session_state["patients_df"],gridOptions=gridoptions,
                            update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
                            height = 400,
                            allow_unsafe_jscode=True,
                            enable_enterprise_modules = True,
                            theme = 'alpine', key="first")
    


    if pd.DataFrame(grid_table["selected_rows"]).empty:
        st.warning("Please Select Patients to edit their information")
    else:
        colored_header(
        label="Edit patient information",
        description="Edit information then press the submit button",
        color_name="blue-70")

        selected_data1 = pd.DataFrame(grid_table["selected_rows"])

        
        # selected_data table
        gd2 = GridOptionsBuilder.from_dataframe(grid_table["selected_rows"])
        gd2.configure_pagination(enabled=True)
        gd2.configure_column("patient_id", editable=False,minWidth=100, cellStyle={'textAlign': 'center'})
        gd2.configure_default_column(groupable=False,editable=True,
                                    autoSize=True,
                                    resizable=True,
                                    cellStyle={'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'color': '#008294'}
                                   )
        gridoptions2 = gd2.build()

         ######## Session state for reset selected rows ##########
        if st.session_state['reset'] == True:
            st.session_state['selected_rows'] = []  # Clear the selection
            st.session_state['reset'] = False
            st.rerun()
    #################################################################
    # Display the custom CSS
        grid_table2 = AgGrid(grid_table["selected_rows"],gridOptions=gridoptions2,
                                update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
                                height = 250,
                                allow_unsafe_jscode=True,
                                enable_enterprise_modules = True,
                                theme = 'alpine', key="second")

        
        
        selected_data2 = grid_table2["data"]

        if grid_table2["data"].equals(grid_table["selected_rows"]):
                st.warning("Please edit Patients before submit")
        else:
            selected_data2["name"] = selected_data2["name"].apply(lambda x:x.title())
            selected_data2["gender"] = selected_data2["gender"].apply(lambda x:x.title())
            selected_data2["address"] = selected_data2["address"].apply(lambda x:x.title())
            selected_data2["emergency_name"] = selected_data2["emergency_name"].apply(lambda x:x.title())
            selected_data2["email"] = selected_data2["email"].apply(lambda x:x.lower())
            selected_data2["marital_status"] = selected_data2["marital_status"].apply(lambda x:x.title())
            # selected_data2
            if st.button("Submit"):
                # tasks_str = ""
                for index, row in selected_data2.iterrows():
                    # tasks_str += f"{row['task']},"  
                    data = {
                        'name': row['name'],
                        'gender': row['gender'],
                        'age': row['age'],
                        'birth_date': str(row['birth_date']),
                        'primary_phone_number': row['primary_phone_number'],
                        'secondary_phone_number': row['secondary_phone_number'],
                        'address': row['address'],
                        'emergency_phone_number': row['emergency_phone_number'],
                        'emergency_name': row['emergency_name'],
                        'email': row['email'],
                        'marital_status': row['marital_status'],
                        'notes': row['notes'],
                    }
                    update_patients(data, row["patient_id"])
                    # supabase.table('tasks').update(data).eq('id', id).execute()
                placeholder2 = st.empty()
                placeholder2.success("Patients information Updated successfully")
                time.sleep(2)
                placeholder2.empty()
                st.session_state["patients_df"] = pd.DataFrame(fetch_data("patients"))  
                st.session_state['reset'] = True
                st.rerun()









@st.fragment(run_every="10m")
def delete_patients():
    colored_header(
        label="Delete Existing Patients",
        description="Select Existing Patients then press the Delete button.",
        color_name="blue-70")
        ######## Session state for reset selected rows ##########
    if 'selected_rows' not in st.session_state:
        st.session_state['selected_rows'] = []
    if 'reset' not in st.session_state:
        st.session_state['reset'] = False
    ##########################################################


    gd6 = GridOptionsBuilder.from_dataframe(st.session_state["patients_df"])

    gd6.configure_pagination(enabled=True)

    gd6.configure_column("patient_id", header_name="patient_id",minWidth=200, cellStyle={'textAlign': 'center'})
    gd6.configure_column("age", header_name="age",maxWidth=75, cellStyle={'textAlign': 'right'})
    gd6.configure_column("gender", header_name="gender",maxWidth=110, cellStyle={'textAlign': 'center'})
    gd6.configure_column("primary_phone_number", header_name="primary_phone_number",minWidth=120, cellStyle={'textAlign': 'center'})
    gd6.configure_column("secondary_phone_number", header_name="secondary_phone_number",minWidth=120, cellStyle={'textAlign': 'center'})
    gd6.configure_column("emergency_phone_number", header_name="emergency_phone_number",minWidth=120, cellStyle={'textAlign': 'center'})
    gd6.configure_default_column(editable=False,groupable=False,
                                minWidth=200,
                                 filter=True,autoSize=True,
                                 resizable=True,
                                 headerStyle={'width':'20000px','textAlign': 'center', 'fontSize': '56px', 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': 'red'},  # Styling for header
                                 cellStyle={'textAlign': 'left'}
                                )


    gd6.configure_selection(selection_mode='multiple',use_checkbox=True)
    gd6.configure_side_bar()

    

    gridoptions = gd6.build()


      ######## Session state for reset selected rows ##########
    if st.session_state['reset'] == True:
        st.session_state['selected_rows'] = []  # Clear the selection
        st.session_state['reset'] = False
        st.rerun()
    #################################################################

# Display the custom CSS
    grid_table = AgGrid(st.session_state["patients_df"],gridOptions=gridoptions,
                            update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
                            height = 500,
                            allow_unsafe_jscode=True,
                            enable_enterprise_modules = True,
                            theme = 'alpine', key="third")
    




    if pd.DataFrame(grid_table["selected_rows"]).empty:
        st.warning("Please Select Patients for Delete")
    else:
        selected_data = pd.DataFrame(grid_table["selected_rows"])
        projs = ""
        if st.button("Delete Patient"):
            for index, row in selected_data.iterrows():
                    delete_patient(row["patient_id"])
            placeholder8 = st.empty()
            # placeholder8.success(f"{row['task']} Task successfully Deleted")
            placeholder8.success('The selected patients successfully deleted')
            time.sleep(2)
            placeholder8.empty()
            fetch_data.clear()
            st.session_state["patients_df"] = pd.DataFrame(fetch_data("patients"))  
            st.session_state['reset'] = True
            st.rerun()







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

        df = pd.DataFrame(fetch_data("patients"))
        st.session_state["patients_df"] = df

        tabs = st.tabs(["Patient Summary","Add New Patient", "Edit Patient", "Delete Patient"])

        with tabs[0]:
            st.markdown(f"<h2 style='color: #008080; text-align:center'>This Feature will come soon</h2>", unsafe_allow_html=True)
        with tabs[1]:
            add_new_patient()
        with tabs[2]:
            edit_patient()
        with tabs[3]:
            delete_patients()

  

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
