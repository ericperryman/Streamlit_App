# Import python packages
import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from urllib.parse import quote



st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if "current_page" not in st.session_state:
    st.session_state.current_page = "summary"

def switch_page(page: str):
    st.session_state.current_page = page

if "selected_county" not in st.session_state:
    st.session_state.selected_county = None
    
if "selected_taxonomic" not in st.session_state:
    st.session_state.selected_taxonomic = None    
    

#sidebar
st.sidebar.subheader("Navigation")

summary_button = st.sidebar.button(
    "Home".upper(), on_click=switch_page, args=["summary"]
)

data_button = st.sidebar.button(
    "Data Overview".upper(), on_click=switch_page, args=["data"]
)

species_button = st.sidebar.button(
    "Species select".upper(), on_click=switch_page, args=["species_select"]
)
wildlife_df = pd.read_csv('merged-county-files.csv')

def summary():
    st.image('orr_western_nc.jpg')
    st.title('North Carolina Wildlife effected by Hurricane Helene')
    st.write('The purpose of this application is to provide a data driven analysis of the unique ecosystem of North Carolina and the species that may have been impacted by Hurricane Helene. In the Data Overview page, you will be able to view the amount of species that have been catalogued in one of three counties: Buncombe, Yancey, and Rutherford county. While North Carolina has 100 counties, my intended purpose of this application was to identify species within the highest impact zone of Hurricane Helene of October 2024 in Western North Carolina and to view the unique species that call this state their home. This data was accessed by the North Carolina Natural Heritage Program.')
    
    col1,col2,col3 = st.columns(3)
    with col2:
        st.image('NCNHPimage.png')
        ncnhp_url = f"https://NCNHP.org"
        st.markdown((ncnhp_url))

def data():
    
    print(wildlife_df)
    print("-=-----------")
    counties = wildlife_df['County'].unique()
    counties = counties.astype('U')
    taxonomic = wildlife_df['Taxonomic Group'].unique()
    
    features = wildlife_df.columns.tolist()
    print(features)
    print(features)
    st.title("Data Overview")
    selected_county = st.selectbox(
            "What county do you want to filter by?",
            counties,
    )
    
    tab1, tab2 = st.tabs(['Charts', 'Data'])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Count of Taxonomic Group per County')
            bar_df = wildlife_df[wildlife_df['County'] == selected_county]
            bar_chart = alt.Chart(bar_df).mark_bar().encode(
                x="Taxonomic Group", y="count()"
            ).properties(
                height=650,
            )
            bar_chart
        with col2:
            st.subheader('NC Conservatory Status per Taxonomic Group')
            circle_df = wildlife_df[wildlife_df['County'] == selected_county]
            chart1 = alt.Chart(circle_df).mark_circle(size=60).encode(
                x='NC Status',
                y='Taxonomic Group',
                color=alt.Color('Common Name', legend=None),
                tooltip='Common Name'
            ).interactive()
            chart1
        col3,col4,col5 = st.columns(3)
        with col4:
            status_df = pd.read_csv('statuses.csv')
            selected_status = st.selectbox("Which Status do you want to know about?",status_df)
            display = status_df[status_df['CODE'] == selected_status]
            st.write(display)
        
    with tab2:
        selected_taxonomic = st.selectbox(
            "What Taxonomic Group do you want to filter by?",
            taxonomic,
    )
        filtered_df = wildlife_df.loc[(wildlife_df['County'] == selected_county) & (wildlife_df['Taxonomic Group'] == selected_taxonomic)]
        st.dataframe(filtered_df)


def species_select():
    st.title("Pick a Taxonomic group & Species for more information!")
    taxonomic = wildlife_df['Taxonomic Group'].unique()
    filtered_taxonomic = taxonomic[taxonomic != 'Natural Community']
    common_name = wildlife_df['Common Name'].dropna()
    options = [f'Pick one' + i for i in filtered_taxonomic]
    search_tax = st.selectbox(
        "What Taxonomic Group do you want to pick from?",
        filtered_taxonomic,
        index=0,
        )
    if search_tax:
        common_filtered = wildlife_df[wildlife_df['Taxonomic Group'] == search_tax]['Common Name']
        search_spec = st.selectbox(
            "What Species do you want to search for?",
            common_filtered,
            index=0,
        )
        st.title("Habitat Description:")
        habitat= wildlife_df[wildlife_df["Common Name"] == search_spec]["Habitat Comment"].unique()
        st.write(habitat[0])


        col1, col2 = st.columns(2)
        with col1:
            st.title("More information")
            encoded_query = quote(search_spec)
            wikipedia_url = f"https://en.wikipedia.org/wiki/{encoded_query}"
            google_url = f"https://google.com/search?q={encoded_query}"
            st.markdown(f"### [Wikipedia page for '{search_spec}']({wikipedia_url})")
            st.markdown(f"### [Google page for '{search_spec}']({google_url})")
        with col2:
            st.title("Endangered status")
            endangered_df = wildlife_df[wildlife_df["Common Name"] == search_spec][[ "County","County Status", "NC Status", "State Rank", "Federal Status", "Global Rank"]]
            st.dataframe(endangered_df)

fn_map = {
    "summary": summary,
    "data": data,
    "species_select": species_select,
}

main_window = st.container()

main_workflow = fn_map.get(st.session_state.current_page, summary)

main_workflow()