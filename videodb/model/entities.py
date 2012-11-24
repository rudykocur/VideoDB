
from sqlalchemy import Column, Integer, Unicode, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from videodb.model import DeclarativeBase

class Library(DeclarativeBase):
    __tablename__ = "library"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode)
    root = Column(Unicode, nullable=False)
    type = Column(Unicode)

class Movie(DeclarativeBase):
    __tablename__ = 'movie'
    
    id = Column(Integer, primary_key=True)
    library_id = Column(Integer, ForeignKey('library.id'), nullable=False)
    path = Column(Unicode, nullable=False)
    imdbData_id = Column(Unicode, ForeignKey('imdb_data.imdbId'), nullable=True)
    disabled = Column(Boolean, default=False)
    
    library = relationship("Library")
    imdbData = relationship("ImdbData")
    
    
class ImdbData(DeclarativeBase):
    __tablename__ = 'imdb_data'
    
    imdbId = Column(Unicode, primary_key=True)
    name = Column(Unicode)
    genres = Column(Unicode)
    coverUrl = Column(Unicode)
    year = Column(Unicode)
    runtime = Column(Unicode)
    
