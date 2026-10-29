"""
Account API Service Test Suite
"""
import unittest
from service import app
from service.models import db, Account
from service.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

DATABASE_URI = "sqlite:///test.db"

ACCOUNT_DATA = {
    "name": "Roopali Sen",
    "email": "roopali@example.com",
    "address": "452 Industrial Area, Phase II",
    "phone_number": "9876543210"
}


class TestAccountService(unittest.TestCase):
    """Account Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Runs after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, HTTP_200_OK)

    def test_health(self):
        """It should return health status OK"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should create a new Account"""
        resp = self.client.post("/accounts", json=ACCOUNT_DATA)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        new_account = resp.get_json()
        self.assertEqual(new_account["name"], ACCOUNT_DATA["name"])
        self.assertEqual(new_account["email"], ACCOUNT_DATA["email"])

    def test_get_account(self):
        """It should read an Account"""
        resp = self.client.post("/accounts", json=ACCOUNT_DATA)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        account_id = resp.get_json()["id"]

        resp = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], ACCOUNT_DATA["name"])

    def test_get_account_not_found(self):
        """It should return 404 for an Account not found"""
        resp = self.client.get("/accounts/0")
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_update_account(self):
        """It should update an existing Account"""
        resp = self.client.post("/accounts", json=ACCOUNT_DATA)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        account_id = resp.get_json()["id"]

        updated_data = dict(ACCOUNT_DATA)
        updated_data["name"] = "Roopali Updated"
        resp = self.client.put(f"/accounts/{account_id}", json=updated_data)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Roopali Updated")

    def test_delete_account(self):
        """It should delete an Account"""
        resp = self.client.post("/accounts", json=ACCOUNT_DATA)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        account_id = resp.get_json()["id"]

        resp = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)

        resp = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_delete_account_payload(self):
        """It should delete an Account via payload at /accounts"""
        resp = self.client.delete("/accounts", json=ACCOUNT_DATA)
        self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)

    def test_list_accounts(self):
        """It should list all Accounts"""
        self.client.post("/accounts", json=ACCOUNT_DATA)
        resp = self.client.get("/accounts")
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 1)

    def test_security_headers(self):
        """It should return security headers"""
        resp = self.client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(resp.status_code, HTTP_200_OK)
        headers = {
            'X-Frame-Options': 'SAMEORIGIN',
            'X-Content-Type-Options': 'nosniff',
            'Content-Security-Policy': 'default-src \'self\'; object-src \'none\'',
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
        for key, value in headers.items():
            self.assertEqual(resp.headers.get(key), value)

    def test_cors_security(self):
        """It should return a CORS header"""
        resp = self.client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertEqual(resp.headers.get('Access-Control-Allow-Origin'), '*')
