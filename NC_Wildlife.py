#venv\scripts\activate.bat


import altair as alt
import pandas as pd
import streamlit as st
import snowflake as sn

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("NC Wildlife")
st.markdown("Use this Streamlit app to make your own scatterplot about nc wildlife!aaa")

wildlife_df = pd.read_csv('merged-county-files.csv', on_bad_lines='skip')

#sidebar
st.sidebar.subheader("Navigation")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Summary", "Overview", "Param Select", "Data", "wiki", "geo"])
with tab1:
    #def summary():
        st.title('NC Wildlife Application')
        st.write('This app will help you explore attributes about NC Wildlife')

with tab2:
    st.title("This tab will hold overview of the data")
    st.write("mainly showing the breakdown of the taxonomic groups etc")

with tab3:
    st.title("the user will narrow down what they want to see")
    st.write("if they want to get rid of some types or choose specific groups to look at")
with tab4:
    #def data():
        #wildlife_df = pd.read_csv('merged-county-files.csv', on_bad_lines='skip')

        features = wildlife_df.select_dtypes(include=['number']).columns.tolist()
        #features = [col for col in features if col in ['Taxonomic Group', 'County']]
        features = ['Taxonomic Group', 'County']
        selected_x_var = st.selectbox(
            "What do you want the x variable to be?",
            features,
            
        )
        #x = len(selected_x_var)
        selected_y_var = st.selectbox(
            "What about the y?",
            features,
        )

        alt_chart = (
            alt.Chart(wildlife_df, title="Scatterplot of NC's wildlife")
            .mark_circle()
            .encode(
                x=alt.X(selected_x_var, scale=alt.Scale(zero=False)),
                y=alt.Y(selected_y_var, scale=alt.Scale(zero=False)),
            # y=alt.Y(x),

                color="Taxonomic Group",
            )
            .interactive()
        )
        st.altair_chart(alt_chart, use_container_width=True)

with tab5:
      selectbox_species = wildlife_df['Common Name']
      selectbox_species = selectbox_species.dropna()
      val = st.selectbox("choose your species!", selectbox_species).lower().capitalize()

      urlBase = "https://en.wikipedia.org/wiki/"
      urlExt = val
      urlExtEdit = urlExt.replace(" ", "_")
      urlComb = urlBase+urlExtEdit
      st.write("for more info on this species, check out this [link](%s)" % urlComb)

with tab6:
    st.title("Map of interest")
    # gdf = gpd.read_file("map2.geojson")
    # df = pd.DataFrame(gdf)
    # #df = {'lat': [35.7596], 'lon': [-79.0193]}
    # st.map(df)
