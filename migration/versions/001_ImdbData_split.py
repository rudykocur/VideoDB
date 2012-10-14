from sqlalchemy import *
from migrate import *

metadata = MetaData()
imdbData_table = Table("imdb_data", metadata,
                    Column("imdbId", Unicode, primary_key=True),
                    Column("name", Unicode),
                    Column("genres", Unicode),
                    Column("coverUrl", Unicode),
                    Column("year", Unicode)
                    )

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    metadata.bind = migrate_engine
    imdbData_table.create()
    
    movieTab = Table('movie', metadata, autoload=True)
    
    movieTab.c.imdbId.drop()
    
    imdbDataId_col = Column('imdbData_id', Unicode, ForeignKey('imdb_data.imdbId'))
    imdbDataId_col.create(movieTab)
    


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
