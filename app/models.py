from app import db

class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    dataframes = db.relationship('DataFrame', backref='workspace')

    def __init__(self, name):
        self.name = name


class DataFrame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    slug_name = db.Column(db.String(120), unique=True, nullable=False)
    data_path = db.Column(db.String(120), unique=True)
