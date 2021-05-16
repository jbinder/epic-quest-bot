import os
import unittest
from unittest import mock

from components.response.response_service import ResponseService


class TestResponseService(unittest.TestCase):
    user1_id: int

    @mock.patch.dict(os.environ, {'DFM_ENV': 'Test'})
    def setUp(self):
        self.user1_id = 1
        self.service = ResponseService()
        self.service.init(ResponseService.get_absolute_file_name("tests/messages.txt"))

    def tearDown(self):
        pass

    def test_get_random_message(self):
        message = self.service.get_random_message()
        self.assertIsNotNone(message)


if __name__ == '__main__':
    unittest.main()
