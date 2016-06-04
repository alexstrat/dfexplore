import tornado.web

from base import BaseHandler
from ..models import Workspace

class WorkspaceHandler(BaseHandler):
    def get(self):
        workspaces = self.db.query(Workspace)

        query_name = self.get_query_argument('name', False)
        if query_name:
            workspaces = workspaces.filter(Workspace.name == query_name)

        response = [{
            'id': ws.id,
            'name': ws.name
        } for ws in workspaces]

        self.write_json(response)

    def post(self):
        name = self.get_body_argument('name', False)
        if not name:
            raise tornado.web.HTTPError(400, 'missing name in body')

        ws = Workspace(name=name)
        self.db.add(ws)
        self.db.commit()

        self.write_json({'id': ws.id, 'name': ws.name})

default_handlers = [
    (r"/workspace/?", WorkspaceHandler),
]
