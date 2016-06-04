import urlparse
import io

import requests
from pandas.compat import cPickle as pkl


class Api(object):
    def __init__(self, root_uri='http://localhost:8080'):
        self.root_uri = root_uri
        self.s = requests.Session()

    def _url(self, url):
        return urlparse.urljoin(self.root_uri, url)

    def get_worskpace(self, name):
        if not name:
            raise ValueError("Specify a name")
        r = self.s.get(self._url('/workspace'), params={'name': name}).json()

        if len(r) == 1:
            w = r[0]
            return Workspace(w['id'], w['name'], api=self)
        elif len(r) > 1:
            raise ValueError('Ooops')
        else:
            r = self.s.post(self._url('/workspace'), data={'name': name}).json()
            return Workspace(r['id'], r['name'], api=self)

class Workspace(object):
    def __init__(self, id, name, api=None):
        self.id = id
        self.name = name
        self.api = api

    def put(self, slug_name, df):
        if not slug_name:
            raise ValueError('Oops')
        data = io.BytesIO()
        pkl.dump(df, data,  protocol=pkl.HIGHEST_PROTOCOL)

        endpoint = '/workspace/%s/dataframe/%s' % (self.id, slug_name)
        url = self.api._url(endpoint)
        self.api.s.post(url, data=data.getvalue())


__all__ = ['Api', 'Workspace']
