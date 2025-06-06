import os

import matplotlib.pyplot as plt
import pandas as pd
import psycopg
import seaborn as sns
import sentry_sdk
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "unknown")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB")
SENTRY_DSN = os.getenv("SENTRY_DSN")

if ENVIRONMENT != "local":
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        # release=f"{APP_NAME}@{VERSION}",
        traces_sample_rate=1.0,
        # Experimental profiling
        _experiments={
            "profiles_sample_rate": 1.0,
        },
        
    )

st.set_page_config(
    page_title="Artificial Non Intelligence - Live Data Analysis",
    page_icon="https://artificial-non-intelligence.herokuapp.com/style/favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Artificial Non Intelligence - Live Data Analysis")

connection = psycopg.connect(
    host=POSTGRES_HOST if POSTGRES_HOST else None,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER if POSTGRES_USER else None,
    password=POSTGRES_PASSWORD if POSTGRES_PASSWORD else None,
)

with connection:
    cursor = connection.cursor()

    # Get the number of scores and the max
    query: str = "SELECT MAX(score), count(*) AS s FROM sessions;"
    cursor.execute(query)
    sessions_count = cursor.fetchone()

    # Get the number of questions
    query: str = "SELECT real, count(*) AS a FROM questions GROUP by real;"
    cursor.execute(query)
    comments_count = cursor.fetchall()

    # Get the general answers trend
    query: str = "SELECT answer, count(*) AS a FROM answers GROUP by answer;"
    cursor.execute(query)
    answers_count = cursor.fetchall()

    # Count number of different answers for each question
    query: str = """
    SELECT
        questions.id,
        questions.content,
        questions.real,
        answers.answer,
        count(*) AS count
    FROM
        questions
        INNER JOIN answers ON questions.id = answers.question_id
    GROUP BY
        questions.id,
        questions.content,
        questions.real,
        answers.answer;
    """
    cursor.execute(query)
    answers = cursor.fetchall()
    cursor.close()

st.markdown("<h2>Number of games played (sessions)</h2>", unsafe_allow_html=True)
st.write(sessions_count[1])

st.markdown("<h2>Number of answers</h2>", unsafe_allow_html=True)
total_answers_count: int = sum(row[1] for row in answers_count)
st.write(total_answers_count)

df = pd.DataFrame(answers, columns=["id", "content", "real", "answer", "count"])

# Verify consistency of total number of answers
# st.write("Sanity check:")
# st.write("Sum of df['count']: ", df['count'].sum())
# st.write("total_answers_count: ", total_answers_count)
# st.write("answers_count: ", answers_count)
assert df['count'].sum(axis = 0, skipna = True) == total_answers_count

# Count total number of human right guesses
right_guesses: int = 0
wrong_guesses: int = 0
biggest_good_guesses: int = 0
biggest_wrong_guesses: int = 0
for i in df.index:
    if df["real"][i] == df["answer"][i]:
        right_guesses += df["count"][i]
    else:
        wrong_guesses += df["count"][i]

accuracy: float = round(right_guesses / total_answers_count, 4)

st.markdown("<h2>Current players accuracy</h2>", unsafe_allow_html=True)
st.write(accuracy)

fig, ax = plt.subplots()
sns.barplot(x=["Right guesses", "Wrong guesses"], y=[right_guesses, wrong_guesses], ax=ax)
st.pyplot(fig)

# st.markdown("<h2>Easiest question</h2>", unsafe_allow_html=True)
# st.write(
#     f'{best_comment[0]}: "{best_comment[1]}" ({best_comment[2]} right answers, real={best_comment[3]})'
# )

# st.markdown("<h2>Most difficult question</h2>", unsafe_allow_html=True)
# st.write(
#     f'{worst_comment[0]}: "{worst_comment[1]}" ({worst_comment[2]} wrong answers, real={worst_comment[3]})'
# )

st.markdown("<h2>Best score</h2>", unsafe_allow_html=True)
st.write(sessions_count[0])

st.markdown("<h2>Current dataset</h2>", unsafe_allow_html=True)
total_comments_count: int = sum(row[1] for row in comments_count)
st.write(f"Number of questions in the database: {total_comments_count}")
fig2, ax2 = plt.subplots()
sns.barplot(x=["AI", "Real"], y=[comments_count[0][1], comments_count[1][1]], ax=ax2)
st.pyplot(fig2)
