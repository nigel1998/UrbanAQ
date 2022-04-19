import pandas as pd
import numpy as np
import PIL as pil
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import hydralit as hy

st.set_page_config(page_title="Urban AQ", layout= "wide")
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

#Reading clean dataset
@st.cache
def clean_data():
    df = pd.read_csv('unified_data.csv', encoding='utf-8')
    #df1 = df.iloc[:,1:4].groupby(by=['ID','City','Country']).sum().reset_index()
    df.sort_values(by=['Country','City','ID'], inplace= True)
    return df

df = clean_data()

#compare = df.iloc[:,[1,2,3,6,7,11,12,16,17,21]]
#compare['City_Country'] = [x+", "+y for (x,y) in zip(compare.iloc[:,1], compare.iloc[:,2])]

codebook = pd.read_csv('codebook.csv', encoding='utf-8')

img1 = pil.Image.open('img1.png')



##########################################################################################################################
col01, col02, col03 = st.columns([1,9,1])
#col01.markdown("<h6 style='text-align: center; font-weight: bold; font-size:35pt; color: #033c5a; padding-top: 40px; '>Urban AQ: Air quality and health in 13,000 cities</h1>", unsafe_allow_html=True)
col02.image(img1,use_column_width= True)


st.text("")
st.text("")
st.text("")
over_theme = {'txc_inactive': '#000000'}
app = hy.HydraApp(title='UrbanAQ',
        hide_streamlit_markers=False,
        #add a nice banner, this banner has been defined as 5 sections with spacing defined by the banner_spacing array below.
        use_navbar=True, 
        navbar_sticky=False,
        navbar_theme=over_theme
    )
@app.addapp(is_home=True)
def home():
    my_expander1 = st.expander('Description', expanded=True)  
    col1, col2, col3 = my_expander1.columns([1,7,1])
    #col2.markdown("<h3 style='text-align: left; font-weight: bold '>Description:</h1>", unsafe_allow_html=True)
    col2.markdown("<p style='text-align: justify;'>This website provides estimates of fine particulate matter (PM<sub>2.5</sub>), nitrogen dioxide (NO<sub>2</sub>) and ozone (O<sub>3</sub>) concentrations and associated disease burdens in >13,000 urban areas globally. Estimates for PM<sub>2.5</sub> and NO<sub>2</sub> are available from 2000-2019. Estimates for O<sub>3</sub> are currently available for the year 2019. Methods are consistent with the Global Burden of Disease 2019 study, to the extent possible. Please visit our <b>More Information</b> and <b>Acknowledgements</b> sections by navigating to the 'About' page.</p>", unsafe_allow_html=True)

            
    col2.text("")
    col2.text("")

    select_pollutant_intro= col2.selectbox('Select Pollutant:', ['PM 2.5', 'Ozone', 'NO2'], key='about')
    if (select_pollutant_intro == 'PM 2.5'):    
        world_map = px.scatter_mapbox(df.dropna(axis = 0, subset = ['PM']), lat='Latitude', lon='Longitude',color = 'PM', opacity= 0.9, center={'lat' : 27.0326, 'lon' : 14.436}, zoom = 0.6, title='<b>Annual Average PM<sub>2.5</sub> Concentration (µg/m³)</b>', color_continuous_scale= "Inferno_r", mapbox_style='carto-positron', height = 650, labels = {"PM": "<b>PM<sub>2.5</sub> concentration (µg/m³)</b>", "lat":"Latitude", "lon":"Longitude"}, animation_frame = 'Year', hover_name= 'City')
        world_map.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
        world_map.update_coloraxes(colorbar_outlinecolor="black", colorbar_outlinewidth=0.5, cmin=round(df['PM'].min()), cmax = round(df['PM'].max()))
        world_map.layout['sliders'][0]['active'] = len(world_map.frames) - 1
        world_map = go.Figure(data=world_map['frames'][len(world_map.frames)-1]['data'], frames=world_map['frames'], layout=world_map.layout)
        col2.plotly_chart(world_map, use_container_width=True)
    if (select_pollutant_intro == 'Ozone'):       
        world_map = px.scatter_mapbox(df.dropna(axis = 0, subset = ['O3']), lat='Latitude', lon='Longitude',color = 'O3', opacity= 0.9, center={'lat' : 27.0326, 'lon' : 14.436}, zoom = 0.6, title='<b>6-month Averages of the Daily Maximum 8-hour Mixing Ratio Ozone Concentration (ppb)</b>', color_continuous_scale= "Inferno_r", mapbox_style='carto-positron', height = 650, labels = {"O3": "<b>O3 concentration (ppb)</b>", "lat":"Latitude", "lon":"Longitude"}, animation_frame = 'Year', hover_name= 'City')
        world_map.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
        world_map.update_coloraxes(colorbar_outlinecolor="black", colorbar_outlinewidth=0.5, cmin=round(df['PM'].min()), cmax = 80)
        #world_map.layout['sliders'][0]['active'] = len(world_map.frames) - 1
        #world_map = go.Figure(data=world_map['frames'][len(world_map.frames)-1]['data'], frames=world_map['frames'], layout=world_map.layout)
        col2.plotly_chart(world_map, use_container_width=True)
    if (select_pollutant_intro == 'NO2'):
        world_map = px.scatter_mapbox(df.dropna(axis = 0, subset = ['NO2']), lat='Latitude', lon='Longitude',color = 'NO2', opacity= 0.9, center={'lat' : 27.0326, 'lon' : 14.436}, zoom = 0.6, title='<b>Annual Average NO<sub>2</sub> Concentration (ppb)</b>', color_continuous_scale= "Inferno_r", mapbox_style='carto-positron', height = 650, labels = {"NO2": "<b>NO<sub>2</sub> concentration (ppb)</b>", "lat":"Latitude", "lon":"Longitude"}, animation_frame = 'Year', hover_name= 'City')
        world_map.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
        world_map.update_coloraxes(colorbar_outlinecolor="black", colorbar_outlinewidth=0.5, cmin=round(df['PM'].min()), cmax = 30)
        world_map.layout['sliders'][0]['active'] = len(world_map.frames) - 1
        world_map = go.Figure(data=world_map['frames'][len(world_map.frames)-1]['data'], frames=world_map['frames'], layout=world_map.layout)
        col2.plotly_chart(world_map, use_container_width=True)


##########################################################################################################################
# Initial plots (Set 1)
@app.addapp(title='Data Visualizations')
def DataVisualization():

    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    my_expander2 = st.expander("Data Visualizations", expanded=True)   
    st.sidebar.title("Select Options to Visualize Data:")
    countries = list(df['Country'].unique())
    countries.remove('United States')
    countries.remove('India')
    countries.remove('China')
    select_country = st.sidebar.selectbox('Select Country:',['<select>','United States', 'India', 'China'] + countries, help="Filter data by Country, which will be displayed under the 'Data Visualizations' expander on button click.", key='sel_con')
    select_city = st.sidebar.selectbox('Select City:',list(df[df['Country'] == select_country]['City'].unique()), help="Filter data by City, which will be displayed under the 'Data Visualizations' expander on button click.", key='sel_cit')
    select_id = st.sidebar.selectbox('Select City ID:',list(df[df['Country'] == select_country][df[df['Country'] == select_country]['City'] == select_city]['ID'].unique()), help="Filter data by City ID (if there are Cities with identical names), which will be displayed under the 'Data Visualizations' expander on button click.",key='sel_id')
    select_pollutant = st.sidebar.selectbox('Select Pollutant:', ['<select>','PM 2.5', 'Ozone', 'NO2'], help="Filter data by Pollutant, which will be displayed under the 'Data Visualizations' expander on button click.", key='sel_pol')
    
    
    
    if st.sidebar.button('Visualize Data'):
        if (select_id != '<select>'): 
            if (select_pollutant == 'PM 2.5'):

                try:
                    map = px.scatter_mapbox(df[df['Country'] == select_country].dropna(axis = 0, subset = ['PM']), lat='Latitude', lon='Longitude',color = 'PM', opacity= 0.9, zoom = 2,  title='<b>Annual Average PM<sub>2.5</sub> Concentration (µg/m³)</b>', color_continuous_scale= "Inferno_r", mapbox_style='carto-positron', height = 650, labels = {"PM": "<b>PM<sub>2.5</sub> concentration (µg/m³)</b>", "lat":"Latitude", "lon":"Longitude"}, animation_frame = 'Year', hover_name= 'City')
                    map.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    map.update_coloraxes(colorbar_outlinecolor="black", colorbar_outlinewidth=0.5, cmin=round(df[df['Country'] == select_country]['PM'].min()), cmax = round(df[df['Country'] == select_country]['PM'].max()))
                    my_expander2.plotly_chart(map, use_container_width=True)

                    fig = px.line(df[df['ID'] == select_id], x="Year", y="PM", hover_name = 'City', template="simple_white", title= '<b>' + select_city.upper() + ' - Annual Average PM<sub>2.5</sub> Concentration (µg/m³)</b>', labels = {'PM':'<b>PM<sub>2.5</sub> Concentration (µg/m³)</b>', 'Year' : '<b>Year</b>'})
                    fig.data[0].update(mode='markers+lines')
                    fig.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig.update_traces(line=dict(color="#F26572", width=2))
                    fig.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig, use_container_width=True)

                    fig1 = px.bar(df[df['ID'] == select_id], x="Year", y="Cases_PM", template="simple_white", hover_name = 'City', color= 'Population', color_continuous_scale= "teal", title= '<b>' + select_city.upper() + ' - PM<sub>2.5</sub> - Attributable Premature Deaths</b>', labels = {'Cases_PM':'<b>Attributable Premature Deaths</b>', 'Year' : '<b>Year</b>', 'Population' : '<b>Population</b>'})
                    fig1.update_traces(marker=dict(line=dict(width=0.5,color='Black')))
                    fig1.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig1.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig1.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig1, use_container_width=True)

                    fig2 = px.line(df[df['ID'] == select_id], x="Year", y="Rates_PM", hover_name = 'City', template="simple_white", title= '<b>' + select_city.upper() + ' - PM<sub>2.5</sub> - Attributable Premature Deaths (per 100,000)</b>', labels = {'Rates_PM':'<b>Attributable Premature Deaths (per 100,000)</b>', 'Year' : '<b>Year</b>'})
                    fig2.data[0].update(mode='markers+lines')
                    fig2.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig2.update_traces(line=dict(color="#008080", width=2))
                    fig2.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig2.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig2, use_container_width=True)

                    my_expander2.markdown("<p style='text-align: justify;'><b>PM<sub>2.5</sub> health impacts include mortality from stroke, ischemic heart disease, chronic obstructive pulmonary disease, lung cancer, lower respiratory infections, and diabetes mellitus type 2.</b>", unsafe_allow_html=True)

                except:
                    my_expander2.text("")
                    my_expander2.markdown("<ul style='text-align: justify; font-size:30px'>Data not available. Select a different pollutant.", unsafe_allow_html=True)
        
            if (select_pollutant == 'Ozone'):
                
                try:
                    map = px.scatter_mapbox(df[df['Country'] == select_country].dropna(axis = 0, subset = ['O3']), lat='Latitude', lon='Longitude',color = 'O3', opacity= 0.9, zoom = 2,  title='<b>6-month Averages of the Daily Maximum 8-hour Mixing Ratio Ozone Concentration (ppb)</b>', color_continuous_scale= "Inferno_r", mapbox_style='carto-positron', height = 650, labels = {"O3": "<b>O3 concentration (ppb)</b>", "lat":"Latitude", "lon":"Longitude"}, animation_frame = 'Year', hover_name= 'City')
                    map.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    map.update_coloraxes(colorbar_outlinecolor="black", colorbar_outlinewidth=0.5, cmin=round(df[df['Country'] == select_country]['O3'].min()), cmax = 80)
                    my_expander2.plotly_chart(map, use_container_width=True)
                    
                    fig = px.line(df[df['ID'] == select_id], x="Year", y="O3", hover_name = 'City', template="simple_white", title= '<b>' + select_city.upper() + ' - 6-month Averages of the Daily Maximum 8-hour Mixing Ratio Ozone Concentration (ppb)</b>', labels = {'O3':'<b>O3 Concentration (ppb)</b>', 'Year' : '<b>Year</b>'})
                    fig.data[0].update(mode='markers+lines')
                    fig.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig.update_traces(line=dict(color="#F26572", width=2))
                    fig.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig, use_container_width=True)

                    fig1 = px.bar(df[df['ID'] == select_id], x="Year", y="Cases_O3", hover_name = 'City', template="simple_white", color= 'Population', color_continuous_scale= "teal", title= '<b>' + select_city.upper() + ' - Ozone - Attributable Premature Deaths</b>', labels = {'Cases_O3':'<b>Attributable Premature Deaths</b>', 'Year' : '<b>Year</b>', 'Population' : '<b>Population</b>'})
                    fig1.update_traces(marker=dict(line=dict(width=0.5,color='Black')))
                    fig1.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig1.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig1.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig1, use_container_width=True)

                    fig2 = px.line(df[df['ID'] == select_id], x="Year", y="Rates_O3", hover_name = 'City', template="simple_white", title= '<b>' + select_city.upper() + ' - Ozone - Attributable Premature Deaths (per 100,000)</b>', labels = {'Rates_O3':'<b>Attributable Premature Deaths (per 100,000)</b>', 'Year' : '<b>Year</b>'})
                    fig2.data[0].update(mode='markers+lines')
                    fig2.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig2.update_traces(line=dict(color="#008080", width=2))
                    fig2.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig2.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig2, use_container_width=True)

                    my_expander2.markdown("<p style='text-align: justify;'><b>Ozone health impacts include only chronic respiratory mortality.</b>", unsafe_allow_html=True)
                except:
                    my_expander2.text("")
                    my_expander2.markdown("<ul style='text-align: justify; font-size:30px'>Data not available. Select a different pollutant.", unsafe_allow_html=True)

            if (select_pollutant == 'NO2'):
                try:
                    my_expander2.markdown("<p style='text-align: justify;'><b>NOTE:-</b> For NO<sub>2</sub>, values between Years 2000-2005 and Years 2005-2010 are linearly interpolated.</p>", unsafe_allow_html=True)

                    map = px.scatter_mapbox(df[df['Country'] == select_country].dropna(axis = 0, subset = ['NO2']), lat='Latitude', lon='Longitude',color = 'NO2', opacity= 0.9, zoom = 2,  title='<b>Annual Average NO<sub>2</sub> Concentration (ppb)</b>', color_continuous_scale= "Inferno_r", mapbox_style='carto-positron', height = 650, labels = {"NO2": "<b>NO<sub>2</sub> concentration (ppb)</b>", "lat":"Latitude", "lon":"Longitude"}, animation_frame = 'Year', hover_name= 'City')
                    map.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    map.update_coloraxes(colorbar_outlinecolor="black", colorbar_outlinewidth=0.5, cmin=round(df[df['Country'] == select_country]['NO2'].min()), cmax = 30)
                    my_expander2.plotly_chart(map, use_container_width=True)

                    fig = px.line(df[df['ID'] == select_id], x="Year", y="NO2", hover_name = 'City', template="simple_white", title= '<b>' + select_city.upper() + ' - Annual Average NO<sub>2</sub> Concentration (ppb)</b>', labels = {'NO2':'<b>NO<sub>2</sub> Concentration (ppb)</b>', 'Year' : '<b>Year</b>'})
                    fig.data[0].update(mode='markers+lines')
                    fig.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig.update_traces(line=dict(color="#F26572", width=2))
                    fig.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig, use_container_width=True)

                    fig1 = px.bar(df[df['ID'] == select_id], x="Year", y="Cases_NO2", hover_name = 'City', template="simple_white", color= 'Population', color_continuous_scale= "teal", title= '<b>' + select_city.upper() + ' - NO<sub>2</sub> - Attributable Pediatric Asthma Incidence</b>', labels = {'Cases_NO2':'<b>Attributable Pediatric Asthma Incidence</b>', 'Year' : '<b>Year</b>', 'Population' : '<b>Population</b>'})
                    fig1.update_traces(marker=dict(line=dict(width=0.5,color='Black')))
                    fig1.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig1.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig1.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig1, use_container_width=True)

                    fig2 = px.line(df[df['ID'] == select_id], x="Year", y="Rates_NO2", hover_name = 'City', template="simple_white", title= '<b>' + select_city.upper() + ' - NO<sub>2</sub> - Attributable Pediatric Asthma Incidence (per 100,000)</b>', labels = {'Rates_NO2':'<b>Attributable Pediatric Asthma Incidence (per 100,000)</b>', 'Year' : '<b>Year</b>'})
                    fig2.data[0].update(mode='markers+lines')
                    fig2.update_layout(title_xanchor='left', title_yanchor='top', title_pad_t=100, title_pad_l= 50, plot_bgcolor='#EAECFB')
                    fig2.update_traces(line=dict(color="#008080", width=2))
                    fig2.update_xaxes(title_font=dict(size=14), tickvals=[2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020])
                    fig2.update_yaxes(title_font=dict(size=14))
                    my_expander2.plotly_chart(fig2, use_container_width=True)

                    my_expander2.markdown("<p style='text-align: justify;'><b>NO<sub>2</sub> health impacts include only pediatric asthma incidence.</b>", unsafe_allow_html=True)
                except:
                    my_expander2.text("")
                    my_expander2.markdown("<ul style='text-align: justify; font-size:30px'>Data not available. Select a different pollutant.", unsafe_allow_html=True)
    my_expander2.text("")
    my_expander2.text("")



##########################################################################################################################

@app.addapp(title='Data Download')
def DataDownload():
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    my_expander3 = st.expander("Data Download", expanded=True)
    st.sidebar.title("Select Options to Download Data:")

    df1 = df
    container_select_pollutant1 = st.sidebar.container()
    all_select_pollutant1 = st.sidebar.checkbox("Select all",key="all_select_pollutant1")
    if all_select_pollutant1:
        select_pollutant1 = container_select_pollutant1.multiselect('Select Pollutant:', ['PM 2.5', 'Ozone', 'NO2'], ['PM 2.5', 'Ozone', 'NO2'], help="Filter data by Pollutant, which will be displayed under the 'Data Download' expander on button click.")
    else:
        select_pollutant1 = container_select_pollutant1.multiselect('Select Pollutant:', ['PM 2.5', 'Ozone', 'NO2'], help="Filter data by Pollutant, which will be displayed under the 'Data Download' expander on button click.")


    if (select_pollutant1 == ['PM 2.5', 'Ozone', 'NO2']):
        df1 = df1
    elif (select_pollutant1 ==['PM 2.5']):
        df1 = df1.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,23,24,25,26,27,28]]
    elif (select_pollutant1 ==['Ozone']):
        df1 = df1.iloc[:,[0,1,2,3,4,5,6,12,13,14,15,16,23,24,25,26,27,28]]
    elif (select_pollutant1 ==['NO2']):
        df1 = df1.iloc[:,[0,1,2,3,4,5,6,17,18,19,20,21,22,23,24,25,26,27,28]]
    elif (select_pollutant1 ==[]):
        df1 = df1.iloc[:,[0,1,2,3,4,5,6,23,24,25,26,27,28]]
    elif (select_pollutant1 ==['PM 2.5','Ozone']):
        df1 = df1.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,23,24,25,26,27,28]]
    elif (select_pollutant1 ==['NO2','Ozone']):
        df1 = df1.iloc[:,[0,1,2,3,4,5,6,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]]
    elif (select_pollutant1 ==['PM 2.5','NO2']):
        df1 = df1.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,17,18,19,20,21,22,23,24,25,26,27,28]]





    container_select_year1 = st.sidebar.container()
    all_select_year1 = st.sidebar.checkbox("Select all",key="all_select_year1")
    if all_select_year1:
        select_year = container_select_year1.multiselect('Select Year:',list(df1['Year'].unique()),list(df1['Year'].unique()), help="Filter data by Year, which will be displayed under the 'Data Download' expander on button click.")
        df1 = df1
    else:
        select_year = container_select_year1.multiselect('Select Year:',list(df1['Year'].unique()), help="Filter data by Year, which will be displayed under the 'Data Download' expander on button click.")
        df1 = df1[df1['Year'].isin(select_year)]


    select_country1 = st.sidebar.selectbox('Select Country:',['All'] + list(df1['Country'].unique()), help="Filter data by Country, which will be displayed under the 'Data Download' expander on button click.")
    if (select_country1!='All'):
        df1 = df1[df1['Country'] == select_country1]

        container_select_city1 = st.sidebar.container()
        all_select_city1 = st.sidebar.checkbox("Select all",key="all_select_city1")
        if all_select_city1:
            select_city1 = container_select_city1.multiselect('Select City:', list(df1['City'].unique()), list(df1['City'].unique()), help="Filter data by City, which will be displayed under the 'Data Download' expander on button click.")
            df1=df1
        else:
            select_city1 = container_select_city1.multiselect('Select City:', list(df1['City'].unique()), help="Filter data by City, which will be displayed under the 'Data Download' expander on button click.")
            df1 = df1[df1['City'].isin(select_city1)]
    

    elif (select_country1=='All'):
        df1 = df1



    df1 = df1.reset_index(drop=True)
    
 


    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')


    if st.sidebar.button('Preview Data'):
        my_expander3.subheader("Data head preview:")
        my_expander3.dataframe(df1.head(20))
        my_expander3.subheader("Data tail preview:")
        my_expander3.dataframe(df1.tail(20))

        st.sidebar.download_button(label="Download Data as .csv", data=convert_df(df1), file_name='Data.csv', mime='text/csv')
        st.sidebar.download_button(label="Download Codebook as .csv", data=convert_df(codebook), file_name='Codebook.csv', mime='text/csv')

    
    my_expander3.subheader("Data Codebook:")
    my_expander3.table(codebook)
    my_expander3.text("")


    



##########################################################################################################################
@app.addapp(title='About')
def About():
    my_expander4 = st.expander('About', expanded=True)  
    col11, col12, col13 = my_expander4.columns([1,7,1])

    col12.markdown("<h3 style='text-align: left; font-weight: bold '>More Information:</h1>", unsafe_allow_html=True)
    col12.markdown("<ul style='text-align: justify;'><li>PM<sub>2.5</sub> urban concentrations and disease burdens are from <a href= 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3871717', target='_blank'>Southerland et al. (2021)</a>. PM<sub>2.5</sub> concentrations are not from the GBD 2019, but are from a higher spatial resolution dataset (1km x 1km) developed by <a href= 'https://pubs.acs.org/doi/full/10.1021/acs.est.0c01764', target='_blank'>Hammer et al. (2020)</a>. The dataset integrates information from satellite-retrieved aerosol optical depth, chemical transport modeling, and ground monitor data. Briefly, multiple AOD retrievals from three satellite instruments (the Moderate Resolution Imaging Spectroradiometer (MODIS), SeaWiFs, and the Multiangle Imaging Spectroradiometer (MISR)) were combined and related to near-surface PM<sub>2.5</sub> concentrations using the GEOS-Chem chemical transport model. Ground-based observations of PM<sub>2.5</sub> were then incorporated using a geographically weighted regression. PM<sub>2.5</sub> concentrations and disease burdens are year-specific.</li><li>Ozone urban concentrations and disease burdens are from Malashock et al. (2022). Estimates of ozone season daily maximum 8 h mixing ratio (OSDMA8) concentrations are from the GBD 2019 (0.1 x 0.1 degree), originally developed by <a href= 'https://pubs.acs.org/doi/abs/10.1021/acs.est.0c07742', target='_blank'>DeLang et al. (2021)</a>. OSDMA8 is calculated as the annual maximum of the six-month running mean of the monthly average daily maximum 8 hour mixing ratio, including through March of the following year to contain the Southern Hemisphere summer. DeLang et al (2021) combined ozone ground measurement data with chemical transport model estimates. Output was subsequently downscaled to create fine (0.1 degree) resolution estimates of global surface ozone concentrations from 1990-2017. For the GBD 2019 study, the Institute for Health Metrics and Evaluation (IHME) extrapolated the available estimates for 1990–2017 to 2019 using log-linear trends based on 2008−2017 estimates. We re-gridded ozone data to 1 km (0.0083 degree) resolution to match the spatial resolution of the population estimates. Ozone concentrations and disease burdens are year-specific.</li><li>NO<sub>2</sub> urban concentrations and disease burdens are from <a href= 'https://www.essoar.org/doi/10.1002/essoar.10506660.2', target='_blank'>Anenberg et al. (2021)</a>. NO<sub>2</sub> concentrations (1km x 1km) are those used by the GBD 2020, as NO<sub>2</sub> is a new pollutant included in the GBD after GBD 2019. The dataset was originally developed by <a href= 'https://www.essoar.org/doi/10.1002/essoar.10506660.2', target='_blank'>Anenberg et al. (2021)</a> and combines surface NO<sub>2</sub> concentrations for 2010-2012 from a land use regression model with Ozone Monitoring Instrument (OMI) satellite NO<sub>2</sub> columns to scale to different years. NO<sub>2</sub> concentrations and disease burdens are year-specific and were interpolated for the years between 2000 and 2005 and between 2005 and 2010.</li><li>Urban built-up area is from the <a href= 'https://ghsl.jrc.ec.europa.eu/ghs_smod2019.php', target='_blank'>GHS-SMOD</a> dataset. Urban boundaries don’t follow administrative boundaries and include surrounding built-up areas. <a href= 'https://chemrxiv.org/engage/chemrxiv/article-details/60c75932702a9baa0818ce61', target='_blank'>Apte et al. (2021)</a> show that the urban boundary definition doesn’t influence concentration estimates much.</li><li>Population is from the <a href= 'https://www.worldpop.org/', target='_blank'>Worldpop</a> dataset at ~1km resolution. There’s quite a bit of difference between globally gridded population datasets, and it’s not clear which is the “best” source. A good resource to see how different population datasets compare in different areas of the world is <a href ='https://sedac.ciesin.columbia.edu/mapping/popgrid/', target='_blank'>https://sedac.ciesin.columbia.edu/mapping/popgrid/</a>.</li><li>Disease burdens (national and, in some cases, subnational) and epidemiologically-derived concentration-response relationships are from the <a href= 'http://www.healthdata.org/gbd/2019', target='_blank'>GBD 2019</a>. We could not find urban disease rates for cities globally, so we don’t account for differences in urban disease rates compared with the national (or sub-national, in some places) average rates that we applied. We used the same concentration-response relationships everywhere in the world.</li><li>Uncertainty has been excluded in this data visualization to display temporal trends more clearly. For more information on source and magnitude of uncertainty, see the journal articles linked above. We believe the greatest source of uncertainty is the concentration-response factor, and less uncertainty (though likely still substantial) comes from the concentration estimates, disease rates, and population distribution.</li></ul> ", unsafe_allow_html=True)


    col12.markdown("<h3 style='text-align: left; font-weight: bold '>Acknowledgements:</h1>", unsafe_allow_html=True)
    col12.markdown("<p style='text-align: justify;'>This project was led by the George Washington University Milken Institute School of Public Health with support from NASA, Health Effects Institute, and the Wellcome Trust. Susan Anenberg led the project. Veronica Southerland produced the PM<sub>2.5</sub> estimates, Danny Malashock produced the ozone estimates, and Arash Mohegh produced the NO<sub>2</sub> estimates. The website was developed by Nigel Martis. Additional contributors include Josh Apte, Jacob Becker, Michael Brauer, Katrin Burkart, Kai-Lan Chang, Owen Cooper, Marissa DeLang, Dan Goldberg, Melanie Hammer, Daven Henze, Perry Hystad, Gaige Kerr, Pat Kinney, Andy Larkin, Randall Martin, Omar Nawaz, Marc Serre, Aaron Van Donkelaar, Jason West and Sarah Wozniak. We also gratefully acknowledge the developers of the input datasets, including satellite observations, pollution concentration, GHS-SMOD urban area, Worldpop population, and GBD disease rates and concentration-response functions. The contents of this website do not necessarily reflect the views of NASA, the Health Effects Institute, or Wellcome Trust.</p>", unsafe_allow_html=True)

        
    col12.text("")
    col12.text("")
    col12.markdown('<h3 style="text-align: center; font-weight: bold"><a href="mailto:nigelmartis0@gmail.com">CONTACT US</a></h3>', unsafe_allow_html=True)


app.run()