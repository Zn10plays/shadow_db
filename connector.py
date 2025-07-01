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

# character bible info
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
    """
    Model to represent a chapter in a novel.
    """
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

# General logs for app
class Logs(BaseModel):
    """
    Model to store logs for all the applications application.
    """
    service = CharField(max_length=255)
    message = TextField()
    message_type = CharField(max_length=50)  # e.g., 'info', 'error', 'debug'
    time= DateTimeField(default=datetime.now)
    instance_id = CharField(max_length=255, null=True)

# user class
class User(BaseModel):
    """
    Model to represent a user in the system.
    """
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.now)
    
# keep all books currently being read in a place
class BookShelf(BaseModel):
    """
    Model to represent a library of novels.
    """
    novel = ForeignKeyField(Novel, backref='bookshelves', on_delete='CASCADE')
    user = ForeignKeyField(User, backref='bookshelves', on_delete='CASCADE')

    class Meta:
        primary_key = CompositeKey('novel', 'user')
        indexes = (
            (('novel', 'user'), True),  # Unique per user
        )
    
# keep track of what chapers a user had read
class ChaptersRead(BaseModel):
    """
    Model to track chapters read by a user.
    """
    chapter = ForeignKeyField(Chapter, backref='read_by', on_delete='CASCADE')
    user = ForeignKeyField(User, backref='chapters_read', on_delete='CASCADE')
    read_at = DateTimeField(default=datetime.now)

    class Meta:
        primary_key = CompositeKey('chapter', 'user')


class Bookmarks(BaseModel):
    """
    Model to represent bookmarks for chapters.
    """
    chapter = ForeignKeyField(Chapter, backref='bookmarks', on_delete='CASCADE')
    novel = ForeignKeyField(Novel, backref='bookmarks', on_delete='CASCADE')
    position = IntegerField(default=0)
    content = TextField(null=True)
    bookmark_filled = BooleanField(default=False)
    user = ForeignKeyField(User, backref='bookmarks', on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        primary_key = CompositeKey('chapter', 'user')

        indexes = (
            (('chapter', 'user', 'position'), True),  # Unique per user
        )

db.connect()
db.create_tables([
    Novel, 
    Chapter, 
    BibleInfo, 
    Logs,
    User,
    BookShelf,
    ChaptersRead,
    Bookmarks
    ], safe=True)