from flask import Flask
from flask_restful import Api
from src.utils.logger_config import Logger
from src.model.database import mongo
from src.resources.user import UserResource
from src.resources.profile import ProfileResource
from src.resources.ping import PingResource
from src.resources.login import LoginResource
from src.resources.myaccount import MyAccountResource

LOCAL_MONGO = 'mongodb://localhost:27017/restdb'
CLOUD_MONGO = 'mongodb://heroku_lw3s78tf:dhk2glio3fs16ket6aapjc2867@ds229549.mlab.com:29549/heroku_lw3s78tf'
app = Flask(__name__)
api = Api(app)
logger = Logger(__name__)

app.config['MONGO_DBNAME'] = 'restdb'


api.add_resource(UserResource, "/users")
api.add_resource(ProfileResource, "/users/<username>")
api.add_resource(PingResource, "/ping")
api.add_resource(LoginResource,"/users/login")
api.add_resource(MyAccountResource,"/users/<username>/myaccount")


def run_app(local=True):
    if local:
        app.config['MONGO_URI'] = LOCAL_MONGO
        logger.info('Starting app with local database.')
    else:
        app.config['MONGO_URI'] = CLOUD_MONGO
        logger.info('Starting app with remote database')
    mongo.init_app(app)
    logger.info('Database initialized.')
    return app


if __name__ == '__main__':
    app.config['MONGO_URI'] = LOCAL_MONGO
    app.run(host='0.0.0.0', port=8080, threaded=True)
