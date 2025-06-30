from peewee import *
from datetime import datetime
import os 

import dotenv
dotenv.load_dotenv()

db_port = os.getenv('SQL_SERVER_PORT', '3306')
db_host = os.getenv('SQL_SERVER_HOST', 'localhost')
db_name = os.getenv('SQL_DB_NAME', 'shadowdb')
db_password = os.getenv('SQL_ROOT_PASSWORD', 'password')

# SQLite DB initialization
db = MySQLDatabase('shadow', host=db_host, port=int(db_port), user='root', password=db_password)

# Base model
class BaseModel(Model):
    class Meta:
        database = db

# Novel model
class Novel(BaseModel):
    title = CharField(500)
    url = CharField(500, unique=True)
    last_updated = DateTimeField(default=datetime.now)

class BibleInfo(BaseModel):
    """
    Model to represent character or place information.
    """
    name = CharField(max_length=255)
    raw_name = CharField(max_length=255)
    description = TextField()
    novel = ForeignKeyField(Novel, backref='bible_info', on_delete='CASCADE')

# Chapter model
class Chapter(BaseModel):
    novel = ForeignKeyField(Novel, backref='chapters', on_delete='CASCADE')
    content = TextField()
    accessed_at = DateTimeField(default=datetime.now)
    title = CharField(500)
    url = CharField(500)
    chapter_number = IntegerField()
    is_filled = BooleanField(default=False)
    is_translated = BooleanField(default=False)
    translated_content = TextField(null=True)
    translated_title = CharField(null=True)
    summary = TextField(null=True)
    notes_for_next_chapter = TextField(null=True)

    class Meta:
        indexes = (
            (('novel', 'chapter_number'), True),  # Unique per novel
        )

db.connect()
db.create_tables([Novel, Chapter, BibleInfo], safe=True)