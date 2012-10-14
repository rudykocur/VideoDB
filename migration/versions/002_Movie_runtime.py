from sqlalchemy import *
from migrate import *

metadata = MetaData()

def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    
    tab = Table('imdb_data', metadata, autoload=True)
    
    col = Column('runtime', Unicode)
    col.create(tab)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
