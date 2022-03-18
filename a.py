import pandas as pd
import numpy as np
import PIL as pil
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Urban AQ", layout= "wide")


img1 = pil.Image.open('img1.png')
img2 = pil.Image.open('img2.png')


##########################################################################################################################
col01, col02, col03 = st.columns([6,2,0.90])
col01.markdown("<h6 style='text-align: center; font-weight: bold; font-size:35pt; color: #033c5a; padding-top: 35px; '>Urban AQ: Air quality and health in 13,000 cities</h1>", unsafe_allow_html=True)
col02.image(img1,use_column_width= True)
col03.image(img2,use_column_width= True)

st.text("")
st.text("")
st.text("")
