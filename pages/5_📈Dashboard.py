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



def box(count):
     # Add custom CSS for the box with green borders and professional font
        st.markdown("""
            <style>
            .box {
                border: 6px solid #008294;
                border-radius: 25px;
                padding: 20px;
                text-align: center;
                font-size: 24px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                display: inline-block;
            }
            .centered-box {
                display: flex;
                justify-content: center;
            }
            </style>
            """, unsafe_allow_html=True)

        # Display the box in the top center of the dashboard
        st.markdown(f'<div class="centered-box"><div class="box">Total Patients: {count}</div></div>', unsafe_allow_html=True)



def box2(count):
     # Add custom CSS for the box with green borders and professional font
        st.markdown("""
            <style>
            .box {
                border: 6px solid #008294;
                border-radius: 25px;
                padding: 20px;
                text-align: center;
                font-size: 24px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                display: inline-block;
            }
            .centered-box {
                display: flex;
                justify-content: center;
            }
            </style>
            """, unsafe_allow_html=True)

        # Display the box in the top center of the dashboard
        st.markdown(f'<div class="centered-box"><div class="box">Total Visits: {count}</div></div>', unsafe_allow_html=True)



def bar_chart_dissease(df):
    clinic_c = clinical_notes_df.groupby("disease_type", as_index=False)["has_disease"].value_counts()
    clinic_p = clinical_notes_df.groupby("disease_type", as_index=False)["has_disease"].value_counts(normalize=True)
    values_df = clinic_c.merge(clinic_p, how="left", on=["disease_type", "has_disease"])
    values_df.columns = ["Disease_type", "Has_disease", "Count", "Percentage"]
    values_df["Percentage"] = np.round((values_df["Percentage"] * 100) , 2)
    values_df["Percentage"] = values_df["Percentage"].apply(lambda x: str(x) + " %")
    bar_chart(
    values_df,
    "Disease_type",
    "Percentage",
    "Percentage",
    colors =['#008294','#4D4D4D'],
    height=500,
    width=1100,
    ttle="Disease Prevalence Percentage by Patient Group",
    xtitle="Disease" ,
    ytitle="Percentage" ,
    colour='Has_disease', 
    bg=0.5, 
    bgg=0.08,
    leg="Has_disease" ,
    group="group" 
)

def pie_chart_gender(df):
    vc = df.gender.value_counts().to_frame()
    vcp = df.gender.value_counts(normalize=True).to_frame()
    values_df = vc.merge(vcp, how="left", on="gender")
    values_df = values_df.reset_index()
    values_df.columns = ["Gender", "Count", "Percentage"]
    values_df["Percentage"] = np.round((values_df["Percentage"] * 100) , 2)


    fig = px.pie(values_df, values='Percentage',names=values_df["Gender"],
                custom_data=['Count'],
                labels={"Gender": "Gender"},
                color_discrete_sequence=['#008294', '#4b4b4c', '#bdbdbd'],
                height=450)
    
    fig.update_traces(
    marker_line_color='white',
    marker_line_width=0.5,
    opacity=1,
    hoverinfo='label+value',
    texttemplate='<b>%{value:.2f} %</b>',
    textinfo='percent',
    textfont_size=16,
    hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}<extra></extra>'
)

    fig.update_layout(
        legend_title=dict(
                text="Gender",  # Legend title text
                font=dict(
                    size=16,  # Font size of the legend title
                    family='Arial',  # Font family
                    color='black',  # Font color
                    weight='bold'  # Make the font bold
                )
            ),
        title={'text': f'Gender Percentages Composition', 'y': 0.95, 'x': 0.45, 'xanchor': 'center', 'yanchor': 'top'},
        title_font_size=20,
        title_xanchor='center',
        margin=dict(t=140),
        font=dict(family='Arial', size=16),
        title_font=dict(
        size=20,  # Font size for title
        family='Arial',  # Font family for title
        color='#008080'  # Font color for title (set to red)
    ),
    )

    # for annotation in fig.layout.annotations:
    #     annotation['font'] = {'size' : 18, 'weight':"bold", "color":"#008080"}
    #     annotation['y'] = annotation['y'] + .16 
    st.plotly_chart(fig)




def line_chart(df):
    # df["date_of_visitr"]
    df['date_of_visit'] = pd.to_datetime(df['date_of_visit'])
    # df['month_year'] = df['date_of_visit'].dt.strftime('%m %Y')
    # df['month_name_year'] = df['date_of_visit'].dt.strftime('%B %Y')
    # df['year'] = df['date_of_visit'].dt.year
    # df = df.sort_values(by=['year','date_of_visit'])
    # df.groupby("month_year").visit_id.count()

    df.index = df.date_of_visit
    # g =  df.groupby(pd.Grouper(freq='M'), "disease_type")
    # grouped_data = g.disease_type.count().to_frame()
    grouped_data = df.groupby([pd.Grouper(freq='QE'), 'disease_type'], as_index=False).size()
    # grouped_data["Date"] = grouped_data.date_of_visit.dt.strftime('%B %Y')
    grouped_data["Date"] = pd.to_datetime(grouped_data['date_of_visit']).dt.strftime('%B %Y')
    grouped_data.columns = ["Date_of_visit", "Disease", "Count", "Date"]
    #st.write(grouped_data)
    # grouped_dates = df.groupby(["month_name_year", "disease_type"], as_index=False).visit_id.count()
    # grouped_dates["month_year"] = grouped_dates["month_year"].astype("str")
    # grouped_dates['Date'] = pd.to_datetime(grouped_dates['Date'], format='%d %Y')#.dt.strftime('%B %Y')
    # grouped_dates = grouped_dates.sort_values("Date")
    # st.write(grouped_dates)

    fig = px.line(grouped_data, x='Date', y='Count',color="Disease", markers=True,color_discrete_sequence =['#008294','#4D4D4D'] )#, labels={'value': 'Value'})
    
    
#     fig.update_traces(
#     marker_line_color='white',
#     marker_line_width=0.5,
#     opacity=1,
#     hoverinfo='label+value',
#     texttemplate='<b>%{value:.2f} %</b>',
#     textinfo='percent',
#     textfont_size=16,
#     hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}<extra></extra>'
# )

    fig.update_layout(
        legend_title=dict(
                text="Gender",  # Legend title text
                font=dict(
                    size=16,  # Font size of the legend title
                    family='Arial',  # Font family
                    color='#008080',  # Font color
                    weight='bold'  # Make the font bold
                )
            ),
        title={'text': f'Quarterly Visits Frequency', 'y': 0.95, 'x': 0.45, 'xanchor': 'center', 'yanchor': 'top'},
        title_font_size=20,
        title_xanchor='center',
        margin=dict(t=60),
        font=dict(family='Arial', size=16, color="red",), 
        title_font=dict(
        size=20,  # Font size for title
        family='Arial',  # Font family for title
        color='#008080'  # Font color for title (set to red)
    ),
    )
    
    
    fig.update_yaxes(title_text="Count", # Y axisTitle
                        #  range=[start, end],
                        #  tickformat='.0%',
                        #  zeroline=True,
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
    fig.update_xaxes(title_text="Date", # Y axisTitle
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

    
    
    st.plotly_chart(fig)

patients_df = pd.DataFrame(fetch_data("patients"))
st.session_state["patients_df"] = patients_df

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

        col1 , col2 = st.columns(2)
        with col1:
            box(st.session_state["patients_df"].patient_id.count())
        with col2:
            box2(st.session_state["clinical_notes_df"].visit_id.count())

        st.write('###')

        col1, col2 = st.columns([2, 1.5])

        with col1:
            bar_chart_dissease(st.session_state["clinical_notes_df"])
        with col2:
            # st.write("######")
            pie_chart_gender(st.session_state["patients_df"])
        line_chart(st.session_state["clinical_notes_df"])

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
