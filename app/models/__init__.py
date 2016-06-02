from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

class Workspace(Base):
    __tablename__ = 'workspace'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    dataframes = relationship('DataFrame', backref='workspace')

    def __init__(self, name):
        self.name = name


class DataFrame(Base):
    __tablename__ = 'data_frame'

    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspace.id'))
    slug_name = Column(String(120), unique=True, nullable=False)
    data_path = Column(String(120), unique=True)

def init_db(engine):
    Base.metadata.create_all(bind=engine)
