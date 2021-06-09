import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
import seaborn as sns
import streamlit as st


DATABASE_URL = os.environ['DATABASE_URL']

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="Artificial Non Intelligence - Data Analysis", page_icon="http://artificial-non-intelligence.herokuapp.com/style/favicon.ico",
    layout='centered',
    initial_sidebar_state='auto'
)

st.title("Artificial Non Intelligence - Data Analysis")

st.write("Players's answers general trend:")

connection = psycopg2.connect(DATABASE_URL, sslmode='require')
with connection:
    cursor = connection.cursor()
    
    # Get the general answers trend
    query: str = f"SELECT answer, count(*) AS a FROM answers GROUP by answer;"
    cursor.execute(query)
    answers = cursor.fetchall()
    
    # Get the question with most mistakes
    # ??
    
    cursor.close()

# df = pd.DataFrame(answers)
sns.barplot(x=["Think it's AI", "Thinks it's human"], y=[answers[0][1], answers[1][1]])
st.pyplot()
