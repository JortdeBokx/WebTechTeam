import os
import tempfile
import unittest

import Markis


#TODO: after databases have been created we can make tests
class MarkisTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, Markis.app.config['DATABASE'] = tempfile.mkstemp()
        Markis.app.testing = True
        self.app = Markis.app.test_client()
        with Markis.app.app_context():
            Markis.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(Markis.app.config['DATABASE'])

    def client(request, app):
        client = app.test_client()

        def teardown():
            os.close(app.config['DB_FD'])
            os.unlink(app.config['DATABASE'])

        request.addfinalizer(teardown)

        return client

    def login(client, username, password):
        return client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(client):
        return client.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()