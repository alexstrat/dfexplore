from base import BaseHandler
from ..models import DataFrame

class DataframeHandler(BaseHandler):
    def get(self, workspace_id, slug_name):
        dataframe = self.db.query(DataFrame) \
            .filter(DataFrame.workspace_id == workspace_id) \
            .filter(DataFrame.slug_name == slug_name) \
            .first()
        df = dataframe.get_pd_dataframe()
        self.set_header('Content-Type', 'text/csv')
        self.write(df.to_csv())

    def post(self, workspace_id, slug_name):
        DataFrame.update_or_create(self.db,
            workspace_id,
            slug_name,
            self.request.body)
        #self.write()

class WorspaceDataframeHandler(BaseHandler):
    def get(self, workspace_id):
        dataframes = self.db.query(DataFrame).filter(DataFrame.workspace_id==workspace_id).all()

        response = [{"slug_name": d.slug_name} for d in dataframes]
        self.write_json(response)

default_handlers = [
    (r"/workspace/([0-9]+)/dataframe", WorspaceDataframeHandler),
    (r"/workspace/([0-9]+)/dataframe/([a-zA-Z_][a-zA-Z0-9_]*)", DataframeHandler)
]
