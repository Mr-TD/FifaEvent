import unittest

from app import create_app


class ChatRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"StadiumIQ", response.data)

    def test_chat_rejects_blank_messages(self):
        response = self.client.post("/api/chat", json={"message": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.get_json()["error"].lower())

    def test_chat_accepts_valid_message(self):
        response = self.client.post("/api/chat", json={"message": "Where is the nearest restroom?"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.get_json())


if __name__ == "__main__":
    unittest.main()
