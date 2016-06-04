import os
import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import pandas as pd

import config


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

    workspace_id = Column(Integer, ForeignKey('workspace.id'), primary_key=True)
    slug_name = Column(String(120), nullable=False, primary_key=True)
    data_path = Column(String(120), unique=True)

    def get_pd_dataframe(self):
        full_path = os.path.join(config.DATA_DIR, self.data_path)
        return pd.read_pickle(full_path)

    @classmethod
    def update_or_create(cls, db, workspace_id, slug_name, df_data):
        data_path = '%s.pickle' % uuid.uuid4()
        full_path = os.path.join(config.DATA_DIR, data_path)

        f = open(full_path, 'w')
        f.write(df_data)
        f.close()

        df = cls(
            workspace_id=workspace_id,
            slug_name=slug_name,
            data_path=data_path)
        df = db.merge(df)
        db.commit()


def init_db(engine):
    Base.metadata.create_all(bind=engine)
