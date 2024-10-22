#==========================================================================#
#                          Import Libiraries
#==========================================================================#
# Streamlit
import streamlit as st
import numpy as np
from streamlit_extras.colored_header import colored_header 
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer 
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
)

# supabase
from supabase import create_client, Client

#others
import pandas as pd
from datetime import datetime
import sys
import os
from dotenv import load_dotenv  # pip install python-dotenv
import yaml
from yaml.loader import SafeLoader
import matplotlib.pyplot as plt
import plotly.express as px




#==========================================================================#
#                          Database Environment
#==========================================================================#

# Supabase credentials
# load_dotenv(".env")
# api_key = os.getenv("api_key")

url =  st.secrets['url']
api_key =  st.secrets['api_key']
supabase: Client = create_client(url, api_key)





#==========================================================================#
#                          Database Functions
#==========================================================================#


# Function to fetch data from the database
@st.cache_resource
def fetch_data(table_name):
    response = supabase.table(table_name).select("*").execute()
    return response.data


@st.cache_resource
def fetch_name(id):
    response = supabase.from_("patients").select("name").eq("patient_id", id).execute()
    return response.data[0]["name"]

@st.cache_resource
def fetch_project(project_id):
    response = supabase.table("projects").select("*").eq("id", project_id).execute()
    return response.data


# function to add new project 
def add_project(project_name):
    response = supabase.table("projects").insert({
        "name": project_name,
    }).execute()
    return response.data



# function to update exsiting project 
def update_project(project_name, project_id):
    response = supabase.table('patients').update({'name': project_name}).eq('id', project_id).execute()
    return response.data

# function to Delete exsiting project 
def delete_project(project_id):
    response = supabase.table('projects').delete().eq('id', project_id).execute()
    return response.data




# function to add new Tasks 
def add_patient(name, gender, age, birth_date, primary_phone_number, secondary_phone_number, address, emergency_phone_number,
                emergency_name, email, marital_status , notes
                ):
    response = supabase.table("patients").insert({
        "name": name,
        "gender": gender,
        "age": age,
        "birth_date": birth_date,
        "primary_phone_number": primary_phone_number,
        "secondary_phone_number": secondary_phone_number,
        "address": address,
        "emergency_phone_number": emergency_phone_number,
        "emergency_name": emergency_name,
        "email": email,
        "marital_status": marital_status,
        "notes": notes
    }).execute()
    #return response.data

def add_blood_test(patient_id, test_date,test_name,test_results):
    response = supabase.table("blood_test").insert({
            "patient_id": patient_id,
            "test_date": test_date,
            "test_name": test_name,
            "test_results": test_results
     }).execute()


def add_hormon_test(patient_id, test_date,
                    estrogen_levels, progesterone_levels, luteinizing_hormone,follicle_stimulating_hormone,
                    testosterone_levels, thyroid_tsh, thyroid_t3, thyroid_t4,notes
                    ):
    
    response = supabase.table("hormonal_test").insert({
            "patient_id": patient_id,
            "test_date": test_date,
            "estrogen_levels": estrogen_levels,
            "progesterone_levels": progesterone_levels,
            "luteinizing_hormone": luteinizing_hormone,
            "follicle_stimulating_hormone": follicle_stimulating_hormone,
            "testosterone_levels": testosterone_levels,
            "thyroid_tsh": thyroid_tsh,
            "thyroid_t3": thyroid_t3,
            "thyroid_t4": thyroid_t4,
            "notes": notes
     }).execute()



def add_tumor_marks(patient_id, test_date,
                    ca_15_3, ca_27_29, carcinoembryonic_antigen,her2_neu,
                    muc1
                    ):
    
    response = supabase.table("tumor_marks").insert({
            "patient_id": patient_id,
            "test_date": test_date,
            "ca_15_3": ca_15_3,
            "ca_27_29": ca_27_29,
            "carcinoembryonic_antigen": carcinoembryonic_antigen,
            "her2_neu": her2_neu,
            "muc1": muc1
         }).execute()


def add_mutation_analysis(patient_id, test_date,
                        bcr_abl_fusion_gene, bcr_abl_transcript_levels, t315i_mutation,f317l_mutation,
                        e255k_mutation, g250e_mutation, m351t_mutation, v299l_mutation
                            ):
    response = supabase.table("mutation_analysis").insert({
            "patient_id": patient_id,
            "test_date": test_date,
            "bcr_abl_fusion_gene": bcr_abl_fusion_gene,
            "bcr_abl_transcript_levels": bcr_abl_transcript_levels,
            "t315i_mutation": t315i_mutation,
            "f317l_mutation": f317l_mutation,
            "e255k_mutation": e255k_mutation,
            "g250e_mutation": g250e_mutation,
            "m351t_mutation": m351t_mutation,
            "v299l_mutation": v299l_mutation
         }).execute()

def update_patients(data, patient_id):
    response = supabase.table('patients').update(data).eq('patient_id', patient_id).execute()
    return response.data


def delete_patient(patient_id):
    response = supabase.table('patients').delete().eq('patient_id', patient_id).execute()
    return response.data


def make_states():
    if 'patients_df' not in st.session_state:
        st.session_state["patients_df"] = pd.DataFrame([], columns=[])

    if 'blood_df' not in st.session_state:
        st.session_state["blood_df"] = pd.DataFrame([], columns=[])

    if 'hormonal_df' not in st.session_state:
        st.session_state["hormonal_df"] = pd.DataFrame([], columns=[])

    if 'tumer_marks_df' not in st.session_state:
        st.session_state["tumer_marks_df"] = pd.DataFrame([], columns=[])
    
    if 'mutation_analysis_df' not in st.session_state:
        st.session_state["mutation_analysis_df"] = pd.DataFrame([], columns=[])
    
    if 'clinical_notes_df' not in st.session_state:
        st.session_state["clinical_notes_df"] = pd.DataFrame([], columns=[])





def aggrid_dis(data, label, sublabel, selection="single"):
    colored_header(
    label=label,
    description=sublabel,
    color_name="violet-70")

    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_pagination(enabled=True)
    gd.configure_column(data.columns[0], header_name="id",minWidth=100, cellStyle={'textAlign': 'center'})


    gd.configure_default_column(groupable=False,
                                 filter=True,autoSize=True,
                                 resizable=True,
                                 headerStyle={'textAlign': 'center', 'fontSize': '16px', 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': 'black'},  # Styling for header
                                 cellStyle={'textAlign': 'center'})
    gd.configure_side_bar()
    if selection:
        gd.configure_selection(selection_mode=selection,use_checkbox=True)
    gridoptions = gd.build()


# Display the custom CSS
    grid_table = AgGrid(data,gridOptions=gridoptions,
                            height = 700,
                            allow_unsafe_jscode=True,
                            enable_enterprise_modules = True,
                            theme = 'alpine')

    selected_row = grid_table['selected_rows']
    return selected_row



#==========================================================================#
#                          Other Functions
#==========================================================================#



def convert_to_title(df):
    str_cols = df.select_dtypes(include=['object']).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.title() if isinstance(x, str) else x)
    return df







@st.cache_data(persist=True)
def df_to_dic(df):
    my_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
    return my_dict

def map_df(df, columns, dic):
    for col in columns:
        df[col] = df[col].map(dic)
    return df




@st.cache_data(persist=True)
def get_tasks():
    tasks = fetch_data("tasks")
    global tasks_df
    tasks_df = pd.DataFrame(tasks).sort_values(by="id")
    # st.session_state["tasks_df"] = tasks_df
    return tasks_df

@st.cache_data(persist=True)
def get_employees():
    employees = fetch_data("employees")
    global employees_df
    employees_df = pd.DataFrame(employees).sort_values(by="id")
    # st.session_state["employees_df"] = employees_df
    return employees_df


    

@st.cache_data(persist=True)
def get_projects():
    projects = fetch_data("projects")
    global projects_df
    projects_df = pd.DataFrame(projects).sort_values(by="id")
    # st.session_state["projects_df"] = projects_df
    return projects_df


@st.cache_data(persist=True)
def get_milestones():
    milestones = fetch_data("milestones")
    global milestones_df
    milestones_df = pd.DataFrame(milestones).sort_values(by="id")
    # st.session_state["milestones_df"] = milestones_df
    return milestones_df


@st.cache_data(persist=True)
def get_skills():
    skills = fetch_data("skills")
    global skills_df
    skills_df = pd.DataFrame(skills).sort_values(by="id")
    # st.session_state["skills_df"] = skills_df
    return skills_df


@st.cache_data(persist=True)
def get_employee_skills():
    employee_skills = fetch_data("employeeskills")
    global employee_skills_df
    employee_skills_df = pd.DataFrame(employee_skills).sort_values(by="employee_id")
    # st.session_state["employee_skills_df"] = employee_skills_df
    return employee_skills_df




@st.cache_data(persist=True)
def get_edited_task(emp_df, pro_df, task):

    global employees_dic
    global projects_dic
    employees_dic = df_to_dic(employees_df[["id", "name"]])
    projects_dic = df_to_dic(projects_df)

    edited_tasks_df = tasks_df.copy()
    edited_tasks_df = map_df(edited_tasks_df, ["assigned_to", "employee_to_review", "task_owner", "created_by"], employees_dic)
    edited_tasks_df = map_df(edited_tasks_df, ["project_id"], projects_dic)
    edited_tasks_df.rename(columns={
        'project_id': 'project', 
        'task_name': 'task'
          }, inplace=True)
    
    edited_tasks_df = edited_tasks_df.sort_values(by="id")
    # st.session_state["edited_tasks_df"] = edited_tasks_df
    return edited_tasks_df, 
 



@st.cache_data(persist=True)
def get_edited_task2(emp_df, pro_df, task):

    global employees_dic
    global projects_dic
    employees_dic = df_to_dic(emp_df[["id", "name"]])
    projects_dic = df_to_dic(pro_df)

    edited_tasks_df = task.copy()
    edited_tasks_df = map_df(edited_tasks_df, ["assigned_to", "employee_to_review", "task_owner", "created_by"], employees_dic)
    edited_tasks_df = map_df(edited_tasks_df, ["project_id"], projects_dic)
    edited_tasks_df.rename(columns={
        'project_id': 'project', 
        'task_name': 'task'
          }, inplace=True)
    
    edited_tasks_df = edited_tasks_df.sort_values(by="id")
    # st.session_state["edited_tasks_df"] = edited_tasks_df
    return edited_tasks_df, 
 


normal_ranges = {
    'RBC': {'low': 4.2, 'high': 5.4, 'marginal_low': 4.0, 'marginal_high': 5.6},
    'WBC': {'low': 4.0, 'high': 11.0, 'marginal_low': 3.8, 'marginal_high': 11.2},
    'Platelets': {'low': 150, 'high': 400, 'marginal_low': 140, 'marginal_high': 410},
    'Hemoglobin': {'low': 12.0, 'high': 16.0, 'marginal_low': 11.8, 'marginal_high': 16.2},
    'ALT': {'low': 7, 'high': 56, 'marginal_low': 6, 'marginal_high': 57},  # Updated for ALT
    'AST': {'low': 10, 'high': 40, 'marginal_low': 9, 'marginal_high': 41},  # Updated for AST
    'Bilirubin': {'low': 0.1, 'high': 1.2, 'marginal_low': 0.0, 'marginal_high': 1.3},  # Typical range
    'BUN': {'low': 7, 'high': 20, 'marginal_low': 6, 'marginal_high': 21},  # Typical range
    'Creatinine': {'low': 0.6, 'high': 1.2, 'marginal_low': 0.5, 'marginal_high': 1.3},  # Typical range
    'estrogen_levels': {'low': 30, 'high': 400, 'marginal_low': 20, 'marginal_high': 450},  # Varies by phase
    'progesterone_levels': {'low': 1.0, 'high': 20.0, 'marginal_low': 0.5, 'marginal_high': 22.0},  # Varies by phase
    'luteinizing_hormone (LH)': {'low': 1.9, 'high': 12.0, 'marginal_low': 1.5, 'marginal_high': 13.0},  # Varies by phase
    'follicle_stimulating_hormone': {'low': 1.5, 'high': 10.0, 'marginal_low': 1.0, 'marginal_high': 11.0},  # Varies by phase
    'testosterone_levels': {'low': 300, 'high': 1000, 'marginal_low': 250, 'marginal_high': 1100},  # Varies by age
    'thyroid_tsh': {'low': 0.4, 'high': 4.0, 'marginal_low': 0.3, 'marginal_high': 4.5},  # Typical range
    'thyroid_t3': {'low': 80, 'high': 200, 'marginal_low': 70, 'marginal_high': 210},  # Typical range
    'thyroid_t4': {'low': 4.5, 'high': 12.0, 'marginal_low': 4.0, 'marginal_high': 12.5},  # Typical range
    'ca_15_3': {'low': 0.0, 'high': 30.0, 'marginal_low': 0.0, 'marginal_high': 35.0},
    'ca_27_29': {'low': 0.0, 'high': 38.0, 'marginal_low': 0.0, 'marginal_high': 40.0},
    'carcinoembryonic_antigen': {'low': 0.0, 'high': 5.0, 'marginal_low': 0.0, 'marginal_high': 6.0},
    'her2_neu': {'positive': 1, 'negative': 0},  # Treat as categorical
    'muc1': {'low': 0.0, 'high': 15.0, 'marginal_low': 0.0, 'marginal_high': 20.0},
    'bcr_abl_fusion_gene': {'True': 1, 'False': 0},  # Categorical, presence of the gene
    'bcr_abl_transcript_levels': {'low': 0.0, 'high': 1000.0, 'marginal_high': 1500.0, 'unit': 'copies/mL'},
    't315i_mutation': {'True': 1, 'False': 0},  # Categorical
    'f317l_mutation': {'True': 1, 'False': 0},  # Categorical
    'e255k_mutation': {'True': 1, 'False': 0},  # Categorical
    'g250e_mutation': {'True': 1, 'False': 0},  # Categorical
    'm351t_mutation': {'True': 1, 'False': 0},  # Categorical
    'v299l_mutation': {'True': 1, 'False': 0},  # Categorical
}


# normal_ranges = {
#     'RBC': {'low': 4.2, 'high': 5.4, 'marginal_low': 4.0, 'marginal_high': 5.6},
#     'WBC': {'low': 4.0, 'high': 11.0, 'marginal_low': 3.8, 'marginal_high': 11.2},
#     'Platelets': {'low': 150, 'high': 400, 'marginal_low': 140, 'marginal_high': 410},
#     'Hemoglobin': {'low': 12.0, 'high': 16.0, 'marginal_low': 11.8, 'marginal_high': 16.2},
#     'ALT': {'low': 12.0, 'high': 16.0, 'marginal_low': 11.8, 'marginal_high': 16.2},
#     'AST': {'low': 12.0, 'high': 16.0, 'marginal_low': 11.8, 'marginal_high': 16.2},
#     'Bilirubin': {'low': 12.0, 'high': 16.0, 'marginal_low': 11.8, 'marginal_high': 16.2},
#     'BUN': {'low': 12.0, 'high': 16.0, 'marginal_low': 11.8, 'marginal_high': 16.2},
#     'Creatinine': {'low': 12.0, 'high': 16.0, 'marginal_low': 11.8, 'marginal_high': 16.2},
# }

# Function to apply colors based on the value and normal range
# def color_values(row):
#     lab = row['Lab']
#     value = row['Value']
    
#     # Fetch normal and marginal ranges for the specific lab
#     normal_range = normal_ranges.get(lab, None)
    
#     # If no normal range is found for the lab, return a neutral color (e.g., white)
#     if normal_range is None:
#         return ['', ''] #* 2
    
#     # Normal range conditions
#     try:
#         if normal_range['low'] <= value <= normal_range['high']:
#             return ['','color: green'] #* 2
#         # Marginally low or high
#         elif normal_range['marginal_low'] <= value < normal_range['low'] or normal_range['high'] < value <= normal_range['marginal_high']:
#             return ['','color: orange']# * 2
#         # Outside the normal range
#         else:
#             return ['','color: red']# * 2
#     except KeyError as e:
#         # Handle cases where 'low' or 'high' are missing
#         print(f"Missing key {e} for lab {lab}")
#         return ['','']# * 2


def color_values(row):
    lab = row['Lab']
    value = row['Value']


    # Fetch normal and marginal ranges for the specific lab
    normal_range = normal_ranges.get(lab, None)
    
    # If no normal range is found for the lab, return a neutral color (e.g., white)
    if normal_range is None:
        return ['', '']  # Neutral color for non-existent ranges
    
    # Normal range conditions for numeric values
    if isinstance(value, (int, float)):  # For numeric values
        try:
            if normal_range['low'] <= value <= normal_range['high']:
                return ['', 'color: green']  # Normal value
            # Marginally low or high
            elif (normal_range['marginal_low'] <= value < normal_range['low'] or 
                  normal_range['high'] < value <= normal_range['marginal_high']):
                return ['', 'color: orange']  # Marginal value
            # Outside the normal range
            else:
                return ['', 'color: red']  # Abnormal value
        except KeyError as e:
            # Handle cases where 'low' or 'high' are missing
            print(f"Missing key {e} for lab {lab}")
            return ['', '']  # Default color

    # Handle categorical value for HER2/neu
    elif lab == 'her2_neu':
        if value == 'Positive':
            return ['', '']  # Color for positive result
        elif value == 'Negative':
            return ['', '']  # Color for negative result
        else:
            return ['', '']  # Neutral color for unexpected values
    
    elif (
        lab == 'bcr_abl_fusion_gene' or 
        lab == 't315i_mutation' or 
        lab == 'f317l_mutation' or 
        lab == 'e255k_mutation' or 
        lab == 'g250e_mutation' or 
        lab == 'm351t_mutation' or 
        lab == 'v299l_mutation' 
        ) :
        if value == 'true':
            return ['', 'color: red']  # Color for positive result
        elif value == 'false':
            return ['', 'color: Blue']  # Color for negative result
        else:
            return ['', '']  # Neutral color for unexpected values
        

    return ['', '']  # Default color for other cases






def patient_clincal_notes(id, data):
    if id == "":
        pass
    else:
        name = fetch_name(id)
        st.markdown(f"<h2 style='color: #008080; text-align:center'>{name} Visits history and Clinical notes</h2>", unsafe_allow_html=True)
        for index , row in data.iterrows():
            st.markdown(f'''<h4 style='color: #008080; text-align:left'>{row["date_of_visit"]} Visit </h4>''', unsafe_allow_html=True)
            #d = pd.DataFrame(.T)
            #st.write(row)
            df = pd.DataFrame(row)
            # df.index.name = 'Features'
            df = df.reset_index()
            df.columns = ["Features", "Values"]
            
            def highlight_next_cell(row):
                # Check if the 'Features' column contains 'allergy'
                if row['Features'] == 'allergy':
                    # Return green color for the cell in the next column, empty string for other cells
                    return ['' if col != 'Values' else 'color: red' for col in row.index]
                return ['' for _ in row.index]

            # Apply the function to style the dataframe
            styled_df = st.dataframe(df.style.apply(highlight_next_cell, axis=1),  use_container_width=True)
            styled_df




def patient_blood_lab(id, data, test):
    if id == "":
        pass
    else:
        name = fetch_name(id)
        st.markdown(f"<h2 style='color: #008080; text-align:center'>{test} results for {name}</h2>", unsafe_allow_html=True)
        for index , row in data.iterrows():
            st.markdown(f'''<h4 style='color: #008080; text-align:left'>{row["test_name"]} results on {row["test_date"]}</h4>''', unsafe_allow_html=True)
            c = pd.json_normalize(row['test_results'])
            d = pd.DataFrame(c.T)
            d = d.reset_index()
            d.columns = ["Lab", "Value"]
            # d["Value"] = np.round(d["Value"], 2)
            d = d.style.apply(color_values, axis=1).format({'Value': '{:.2f}'})
            st.dataframe(d)
            st.markdown(f'''<h4 style='color: green; text-align:left'>---------------------------------------------------------------------------------------------- </h4>''', unsafe_allow_html=True)
            

def patient_hormon_lab(id, data, test):
    if id == "":
        pass
    else:
        name = fetch_name(id)
        st.markdown(f"<h2 style='color: #008080; text-align:center'>{test} results for {name}</h2>", unsafe_allow_html=True)
        for index , row in data.iterrows():
            st.markdown(f'''<h4 style='color: #008080; text-align:left'>{row["test_date"]} results </h4>''', unsafe_allow_html=True)
            d = row.iloc[3:-2]
            d = d.reset_index()
            d.columns = ["Lab", "Value"]
            d = d.style.apply(color_values, axis=1).format({'Value': '{:.2f}'})
            st.dataframe(d)
            st.markdown(f'''<h5 style='color: #008080; text-align:left'>Test Notes: {row["notes"]} </h5>''', unsafe_allow_html=True)
            st.markdown(f'''<h4 style='color: green; text-align:left'>---------------------------------------------------------------------------------------------- </h4>''', unsafe_allow_html=True)





def patient_tumer_lab(id, data, test):
    if id == "":
        pass
    else:
        name = fetch_name(id)
        st.markdown(f"<h2 style='color: #008080; text-align:center'>{test} results for {name}</h2>", unsafe_allow_html=True)
        for index , row in data.iterrows():
            st.markdown(f'''<h4 style='color: #008080; text-align:left'>{row["test_date"]} results </h4>''', unsafe_allow_html=True)
            d = row.iloc[3:]
            d = d.reset_index()
            d.columns = ["Lab", "Value"]
            d = d.style.apply(color_values, axis=1)#.format({'Value': format_values})
            st.dataframe(d)
            # st.markdown(f'''<h5 style='color: #008080; text-align:left'>Test Notes: {row["notes"]} </h5>''', unsafe_allow_html=True)
            st.markdown(f'''<h4 style='color: green; text-align:left'>---------------------------------------------------------------------------------------------- </h4>''', unsafe_allow_html=True)
            # st.write(row)



def patient_mutation_lab(id, data, test):
    if id == "":
        pass
    else:
        name = fetch_name(id)
        st.markdown(f"<h2 style='color: #008080; text-align:center'>{test} results for {name}</h2>", unsafe_allow_html=True)
        for index , row in data.iterrows():
            st.markdown(f'''<h4 style='color: #008080; text-align:left'>{row["test_date"]} results </h4>''', unsafe_allow_html=True)
            d = row.iloc[3:]
            d = d.reset_index()
            d.columns = ["Lab", "Value"]
            d = d.style.apply(color_values, axis=1)#.format({'Value': format_values})
            st.dataframe(d)
            # st.markdown(f'''<h5 style='color: #008080; text-align:left'>Test Notes: {row["notes"]} </h5>''', unsafe_allow_html=True)
            st.markdown(f'''<h4 style='color: green; text-align:left'>---------------------------------------------------------------------------------------------- </h4>''', unsafe_allow_html=True)
            # st.write(row)





make_states()









#==========================================================================#
#                          Charts Functions
#==========================================================================#


## Make Charts Functions

def bar_chart(df, xx, yy,  txt="", labls={},hover={}, colors=[], height=600, width=900, ttle="ttle",xtitle="xtitle" , ytitle="ytitle" ,colour=None, bg=0.6, bgg=0.1, leg=None, box=False,yscale=False,yscale_percentage=False, start=-1, end=1, facetrow=None, facetcol=None, group="group", textloc="inside", errory=None, violn=False, showleg=True, legfontsize=16):
    if violn:
        fig = px.violin(df,  x=xx, y=yy, color=colour,
            color_discrete_sequence=colors,height=height, width=width, box=True, points='all',
             facet_col=facetcol, 
             facet_row=facetrow,
             facet_col_spacing=0.15,
             facet_row_spacing=0.15,
            )
    elif box:
        fig = px.box(df,  x=xx, y=yy, color=colour,
            color_discrete_sequence=colors,height=height, width=width,
             facet_col=facetcol, 
             facet_row=facetrow,
             facet_col_spacing=0.20,
             facet_row_spacing=0.25,
            )
    elif colour ==None:
        fig = px.bar(df, x=xx, y=yy, barmode=group,text=txt,
             labels=labls,
             hover_data=hover,
             title=ttle,
             color_discrete_sequence=colors,
             height=height, width=width,
             facet_col=facetcol, 
             facet_row=facetrow,
             facet_col_spacing=0.20,
             facet_row_spacing=0.25,
             error_y=errory,
                    )
    else:
        fig = px.bar(df, x=xx, y=yy, color=colour, barmode=group,text=txt,
                     labels=labls,
                     hover_data=hover,
                     title=ttle,
                     color_discrete_sequence=colors,height=height, width=width,
                     facet_col=facetcol, 
                     facet_row=facetrow,
             facet_col_spacing=0.20,
             facet_row_spacing=0.25,
                      error_y=errory,
                            )


    if box == False and violn == False:
        fig.update_traces(
        textfont_size=15, 
        textposition="outside", 
        texttemplate='<b>%{text}</b>', 
        insidetextanchor='middle', 
        textangle=0, 
        cliponaxis=False
    )

    

    
    if yscale_percentage and yscale:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         zeroline=True,
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)
                        tickfont=dict(
                                    size=12,
                                    family='Arial'
                                ),
                         matches='x'
                         )
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         range=[start, end],
                         tickformat='.0%',
                         zeroline=True,
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=18,  # Set the title font size (optional)
                         titlefont_color="#008080",  # Set the title font color (optional)         )
                         tickfont=dict(
                                        size=12,
                                        family='Arial'
                                    ),
                        matches='y'  # Ensure the y-axis settings apply to all facets
                        )
    elif yscale_percentage:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         zeroline=True,
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=14,  # Set the title font size (optional)
                        titlefont_color="black",  # Set the title font color (optional)
                         tickfont=dict(
                                    size=12,
                                    family='Arial'
                                ),
                         matches='x'
                         )
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         zeroline=True,
                         tickformat='.0%',
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=14,  # Set the title font size (optional)
                        titlefont_color="black",  # Set the title font color (optional)         )
                        tickfont=dict(
                                        size=12,
                                        family='Arial'
                                    ),
                        matches='y'      
                        )
    elif yscale:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         zeroline=True,
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=14,  # Set the title font size (optional)
                        titlefont_color="black",  # Set the title font color (optional)
                         tickfont=dict(
                                    size=12,
                                    family='Arial'
                                ),
                         matches='x'
                         )
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         range=[start, end],
                         zeroline=True,
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=16,  # Set the title font size (optional)
                         titlefont_color="#008080",  # Set the title font color (optional)         )
                         tickfont=dict(
                                        size=12,
                                        family='Arial'
                                    ),
                        matches='y'      
                        )
    else:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)
                         tickfont=dict(
                                        size=12,
                                        family='Arial'
                                    ),
                         matches='x'
                         )
        
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)         )
                         tickfont=dict(
                                        size=12,
                                        family='Arial'
                                    ),
                        matches='y'      
                        )
        
        fig.update_layout(
            legend_title=dict(
                text=leg,  # Legend title text
                font=dict(
                    size=legfontsize,  # Font size of the legend title
                    family='Arial',  # Font family
                    weight='bold'  # Make the font bold
                )
            ),
            plot_bgcolor=None,  #background color
            bargap=bg,  # Gap between bars
            bargroupgap=bgg, 

            title={'text': ttle, 'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}, #title center and size
            title_font_size=20,  # Title font size,
            title_xanchor='center',
            margin=dict(t=100) ,
            showlegend=showleg,
            title_font=dict(
            size=20,  # Font size for title
            family='Arial',  # Font family for title
            color='#008080'  # Font color for title (set to red)
        ),
    
    )
        #  Display the chart in Streamlit

    if facetcol is not None:
        try:
            fig.update_layout(
                # xaxis2_title='',  # Disabling the title for the second x-axis (if present)
                yaxis2_title='',  # Disabling the title for the second y-axis (if present)
            )
        except:
            pass
        for annotation in fig.layout.annotations:
            annotation['font'] = {'size' : 18, 'weight':"bold", "color":"#008080"}
            annotation['y'] = annotation['y'] + .02 
    if facetrow is not None:
        try:
            fig.update_layout(
                xaxis2_title='',  # Disabling the title for the second x-axis (if present)
                # yaxis2_title='',  # Disabling the title for the second y-axis (if present)
            )
        except:
            pass
        for annotation in fig.layout.annotations:
            annotation['font'] = {'size' : 18, 'weight':"bold", "color":"#008080"}
            annotation['x'] = annotation['x'] + .02 

    st.plotly_chart(fig, use_container_width=True)




