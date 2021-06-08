import datetime
from peewee import *


db = SqliteDatabase('../data/db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db

class Website(BaseModel):
    name = CharField(max_length=40)
    short_name = CharField(max_length=20, unique=True)
    language = CharField(max_length=2, default="EN")
    # url = URLField(null=True, unique=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.short_name

    class Meta:
        table_name = "websites"


class Article(BaseModel):
    url = CharField(max_length=200, null=True, unique=True)  # The URL
    url_from = CharField(max_length=200, null=True)  # The source URL
    website = ForeignKeyField(
        model=Website,
        column_name="website_id",
        related_name="website_article",
        on_delete="SET NULL",
    )
    created = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.url

    class Meta:
        table_name = "articles"


class Comment(BaseModel):
    author = CharField(max_length=80, null=True)
    message = TextField()
    article = ForeignKeyField(
        model=Article,
        column_name="article_id",
        related_name="article_comment",
        on_delete="SET NULL",
    )
    created = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.message[:100]

    class Meta:
        table_name = "comments"
        unique_together = ["message"]
