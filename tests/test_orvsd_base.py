from unittest import TestCase

from manage import setup_app

from orvsd_central.models import User
from orvsd_central.database import create_db_session


class BaseORVSDTest(TestCase):
    """
    Functions useful for testing ORVSD.
    """

    def setUp(self):
        self.app = setup_app()
        self.test_client = self.app.test_client()

    def login(self, username, password):
        """
        Login a user.
        """
        return self.test_client.post('/login', data=dict(
            name=username,
            password=password
        ), follow_redirects=True)

    def register(self, user, password, role, email):
        """
        Regiser a user.
        """
        return self.test_client.post('/register', data=dict(
            user=user,
            password=password,
            confirm_pass=password,
            role=role,
            email=email), follow_redirects=True)

    def delete_user(self, username):
        """
        Delete a user directly from the database.
        """
        with self.app.app_context():
            session = create_db_session()
            admin = session.query(User).filter(User.name == username).first()
            session.delete(admin)
            session.commit()

    def add_user(self, username, email, password, role):
        """
        Add a user directly to the database. Role may be an integer indicating
        the permissions of the user or may be one of the following strings:
        * normal
        * helper
        * admin
        """
        roles = {
            'normail': 1,
            'helper': 2,
            'admin': 3,
        }
        with self.app.app_context():
            session = create_db_session()
            user = User(username, email, password,
                        role if type(role) == int else roles[role])
            session.add(user)
            session.commit()
