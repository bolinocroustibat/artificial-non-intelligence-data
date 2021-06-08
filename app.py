import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
import seaborn as sns
import streamlit as st


DATABASE_URL = os.environ['DATABASE_URL']

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Artificial Non Intelligence Data Analysis")

st.write("Answers from game's users")

connection = psycopg2.connect(DATABASE_URL, sslmode='require')
with connection:
    query: str = f"SELECT answer FROM answers;"
    cursor = connection.cursor()
    cursor.execute(query)
    answers = cursor.fetchall()
    cursor.close()

df = pd.DataFrame(answers)

sns.displot(data=df)
st.pyplot()

st.write("Test2")
