import unittest
from app import app, users


class MassAssignmentTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        # Reset Alice before every test.
        users["alice"] = {
            "username": "alice",
            "email": "alice@example.com",
            "role": "user",
            "is_admin": False
        }

    def test_legitimate_email_update(self):
        response = self.client.patch(
            "/api/profile",
            json={"email": "newalice@example.com"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            users["alice"]["email"],
            "newalice@example.com"
        )

    def test_role_change_rejected(self):
        response = self.client.patch(
            "/api/profile",
            json={"role": "admin"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(users["alice"]["role"], "user")

    def test_admin_privilege_change_rejected(self):
        response = self.client.patch(
            "/api/profile",
            json={"is_admin": True}
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(users["alice"]["is_admin"])

    def test_mixed_request_rejected_entirely(self):
        response = self.client.patch(
            "/api/profile",
            json={
                "email": "attacker@example.com",
                "role": "admin"
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            users["alice"]["email"],
            "alice@example.com"
        )
        self.assertEqual(users["alice"]["role"], "user")

    def test_empty_email_rejected(self):
        response = self.client.patch(
            "/api/profile",
            json={"email": ""}
        )

        self.assertEqual(response.status_code, 400)

    def test_request_without_json_rejected(self):
        response = self.client.patch(
            "/api/profile",
            data="email=new@example.com"
        )
        self.assertEqual(response.status_code, 400)

    def test_malformed_json_rejected(self):
        response = self.client.patch(
            "/api/profile",
            data='{"email":',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_non_string_email_rejected(self):
        response = self.client.patch(
            "/api/profile",
            json={"email": 12345}
        )
        self.assertEqual(response.status_code, 400)

    def test_whitespace_email_rejected(self):
        response = self.client.patch(
            "/api/profile",
            json={"email": "   "}
        )
        self.assertEqual(response.status_code, 400)

    def test_username_change_rejected(self):
        response = self.client.patch(
            "/api/profile",
            json={"username": "attacker"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(users["alice"]["username"], "alice")
if __name__ == "__main__":
    unittest.main()
