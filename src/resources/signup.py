from flask_restful import Resource

from src.model.services.shared_server_service import SharedServerService, InvalidDataException, NoServerException, UnexpectedErrorException
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.user import User
from src.utils.logger_config import Logger


class SignUpResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)
        self.shared_server_service = SharedServerService()

    def post(self):
        try:
            # get all data from request
            # TODO: add other user-info fields (obligatory and optional)
            user_data = {}
            user_data['username'] = self._get_username_from_request()
            user_data['password'] = self._get_password_from_request()
            self.logger.info('User data generated. ({})'.format(user_data))

            # validate data received
            # TODO

            # ask shared server for register
            output_dict = self.shared_server_service.create_user(user_data)
            self.logger.info("User {} successfully registered in shared server".format(output_dict['username']))

            # register new user in own DB:
            new_user_id = User.insert_one(user_data)
            self.logger.info('User ({}) added to DB with id {}'.format(user_data, new_user_id))

            # return response
            response = {'username': output_dict['username'], 'password': output_dict['password']}
            return ResponseBuilder.build_response(response)
        except MissingFieldException as mfe:
            return ResponseBuilder.build_error_response(str(mfe), 400)  # check status_code
        except InvalidDataException as ide:
            return ResponseBuilder.build_error_response(str(ide), 400)  # check status_code
        except NoServerException as nse:
            return ResponseBuilder.build_error_response(str(nse), 500)  # check status_code
        except UnexpectedErrorException as uee:
            return ResponseBuilder.build_error_response(str(uee), 500)  # check status_code


    def _get_username_from_request(self):
        return RequestBuilder.get_field_from_request('username')

    def _get_password_from_request(self):
        return RequestBuilder.get_field_from_request('password')
