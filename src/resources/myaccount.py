from flask_restful import Resource

from src.security.token import Token, ExpiredTokenException, InvalidTokenException
from src.model.user import User
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.utils.response_builder import ResponseBuilder
from src.utils.logger_config import Logger
from src.model.exceptions.response_exceptions import *
from src.model.exceptions.request_exceptions import *
from src.model.services.shared_server_service import SharedServerService


class MyAccountResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)
        self.shared_server_service = SharedServerService()

    def get(self, username):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            caller_user = Token.identify(token)

            if caller_user != username:
                return ResponseBuilder.build_error_response("Username is not own", 403)

            # get user data
            account_info = User.get_account_info(username)

            # generate response
            output = account_info
            self.logger.info('User account retrieved. ({})'.format(output))

            # return response
            return ResponseBuilder.build_response(output)

        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except ExpiredTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except InvalidTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def delete(self, username):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            caller_user = Token.identify(token)

            if caller_user != username:
                return ResponseBuilder.build_error_response("Username is not own", 403)

            # ask shared server for account deletion service
            result = self.shared_server_service.delete_user(username)

            assert result == username

            # delete user data at app server
            User.delete_user(username)

            # log him/her out
            Token.log_out(username)
            # generate response
            output = {'username': username}
            self.logger.info('{}\'s account deleted.'.format(username))

            # return response
            return ResponseBuilder.build_response(output)

        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except ExpiredTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except InvalidTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except InvalidDataException as ide:
            return ResponseBuilder.build_error_response(str(ide), 400)  # check status_code
        except NoServerException as nse:
            return ResponseBuilder.build_error_response(str(nse), 500)  # check status_code
        except UnexpectedErrorException as uee:
            return ResponseBuilder.build_error_response(str(uee), 500)  # check status_code
        except ConnectionFailException as cfe:
            return ResponseBuilder.build_error_response(str(cfe), 500)  # check status_code
