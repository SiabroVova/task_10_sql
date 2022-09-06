from app import app
import unittest


class FlaskTest(unittest.TestCase):

    # Check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check if contect return is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/students")
        self.assertEqual(response.content_type, "application/json")

    # Check for returned data
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/all_groups_less_stud")
        self.assertTrue(b"['LG-06']" in response.data)


if __name__ == "__main__":
    unittest.main()
