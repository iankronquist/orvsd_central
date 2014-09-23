from test_orvsd_base import BaseORVSDTest


class TestRegistration(BaseORVSDTest):

    def setUp(self):
        super(TestRegistration, self).setUp()
        self.add_user('testeradmin', 'testeradmin@exapmle.com', 'password',
                      'admin')
        self.login('testeradmin', 'password')

    def tearDown(self):
        self.delete_user('testeradmin')

    def test_duplicate_emails(self):
        self.login('testeradmin', 'password')
        password = 'password'
        user = 'test1'
        email = 'test@test.test'
        role = 1
        response1 = self.register(user, password, role, email)
        self.assertTrue('test1 has been added successfully!\n' in
                        response1.data)
        user = 'test2'
        response2 = self.register(user, password, role, email)
        self.assertTrue('test2 has been added successfully!\n' in
                        response2.data)
        self.delete_user('test1')
        self.delete_user('test2')

