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


if __name__ == "__main__":
    unittest.main()
