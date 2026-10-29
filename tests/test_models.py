"""
Test cases for Account Model
"""
import unittest
from datetime import date
from service.models import Account, db
from service import app

DATABASE_URI = "sqlite:///test.db"


class TestAccountModel(unittest.TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """This runs after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_an_account(self):
        """It should create an Account and assert that it exists"""
        with app.app_context():
            fake_account = Account(
                name="John Doe",
                email="john@example.com",
                address="123 Main Street",
                phone_number="555-1234",
                date_joined=date.today()
            )
            fake_account.create()
            self.assertIsNotNone(fake_account.id)
            found = Account.all()
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].name, "John Doe")

    def test_read_an_account(self):
        """It should read an Account"""
        with app.app_context():
            account = Account(
                name="Jane Doe",
                email="jane@example.com",
                address="456 Elm Street",
                phone_number="555-5678",
                date_joined=date.today()
            )
            account.create()
            found = Account.find(account.id)
            self.assertEqual(found.id, account.id)
            self.assertEqual(found.name, "Jane Doe")

    def test_update_an_account(self):
        """It should update an Account"""
        with app.app_context():
            account = Account(
                name="Alice",
                email="alice@example.com",
                address="789 Pine Street",
                phone_number="555-9012",
                date_joined=date.today()
            )
            account.create()
            account.name = "Alice Wonder"
            account.update()
            found = Account.find(account.id)
            self.assertEqual(found.name, "Alice Wonder")

    def test_delete_an_account(self):
        """It should delete an Account"""
        with app.app_context():
            account = Account(
                name="Bob",
                email="bob@example.com",
                address="321 Oak Street",
                phone_number="555-3456",
                date_joined=date.today()
            )
            account.create()
            self.assertEqual(len(Account.all()), 1)
            account.delete()
            self.assertEqual(len(Account.all()), 0)
