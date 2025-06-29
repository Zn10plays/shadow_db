# export models as a module

from .connector import db, BaseModel, Novel, Chapter, BibleInfo
__all__ = ['db', 'BaseModel', 'Novel', 'Chapter', 'BibleInfo']
