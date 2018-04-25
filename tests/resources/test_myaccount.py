import unittest
import unittest.mock as mock

from src.model.token import Token, ExpiredTokenException
from tests.mocks.token_mock import token_mock
from tests.mocks.user_mock import user_mock
from src.resources.myaccount import MyAccountResource,MissingFieldException
from src.utils.response_builder import ResponseBuilder
from src.model.user import User


class MyAccountTestCase(unittest.TestCase):

    def test_get_myaccount(self):
        service = MyAccountResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        User.get_one = mock.MagicMock(return_value=user_mock)
        Token.validate = lambda x: True
        ResponseBuilder.build_response = lambda output, status_code = 200: output
        self.assertEqual(service.get(user_mock['username']), user_mock)

    def test_get_myaccount_myssing_field(self):
        service = MyAccountResource()
        service._get_token_from_header = mock.MagicMock(side_effect=MissingFieldException)
        ResponseBuilder.build_response = lambda output, status_code: status_code
        self.assertEqual(service.get(user_mock['username']), 400)

    def test_get_myaccount_expired_token(self):
        service = MyAccountResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        Token.validate = mock.MagicMock(side_effect=ExpiredTokenException)
        ResponseBuilder.build_response = lambda output, status_code: status_code
        self.assertEqual(service.get(user_mock['username']), 400)
