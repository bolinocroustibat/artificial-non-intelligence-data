import streamlit as st

import pandas as pd
import seaborn as sns

st.title("Artificial Intelligence Data Analysis")

st.write("Test")

df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 30, 70]})
sns.lineplot(x='x', y='y', data=df)
st.pyplot()
