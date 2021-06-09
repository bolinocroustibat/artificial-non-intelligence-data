import json
import re
import os
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']


def load_real_comments_into_db(filename: str, real: int = 1) -> None:
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    with connection:
        with open (filename, "r") as file:
            data: list = json.loads(file.read())
            print("Excluded since it's too long:")
            print(data.pop(15312))
            for line in data:
                try:
                    aggressive: int = int(line["annotation"]["label"][0])
                    raw_content: str = line["content"].strip().replace('\"', '”')
                    content: str = '\"' + raw_content + '\"'
                    pattern = r'((?:#|http)\S+)'
                    if not len(re.findall(pattern, content)) and len(list(content.split(" "))) > 1:
                        query: str = f"""INSERT INTO comments(content,real,aggressive) VALUES({content},{real},{aggressive})"""
                        cursor = connection.cursor()
                        cursor.execute(query)
                        connection.commit()
                except Exception as e:
                    print(e)
                    continue


def load_fake_comments_into_db(
    filename: str,
    aggressive: int,
    real: int = 0) -> None:
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    with connection:
        with open (filename, "r") as file:
            data: dict = json.loads(file.read())
            for line in data["content"].values():
                try:
                    raw_content: str = line.strip().replace('\"', '”')
                    content: str = '\"' + raw_content + '\"'
                    query: str = f"""INSERT INTO comments(content,real,aggressive) VALUES({content},{real},{aggressive})"""
                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                except Exception as e:
                    print(e)
                    continue


if __name__ == "__main__":
    load_real_comments_into_db(filename="../data/kaggle-cyber-trolls.json")

    load_fake_comments_into_db(
        filename="../data/500_fake_tweets_aggressive_1.json",
        aggressive=1
    )

    load_fake_comments_into_db(
        filename="../data/500_fake_tweets_nonaggressive_1.json",
        aggressive=0
    )
