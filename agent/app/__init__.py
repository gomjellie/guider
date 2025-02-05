from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from app.config import config_dict

from monitoring.controllers import Main
from monitoring.services import communicate_with_guider, disconnect_with_guider


def create_app(config_name):
    f_config = config_dict[config_name]
    app = Flask(__name__,
                template_folder=f_config.STATIC_FOLDER,
                static_url_path='',
                static_folder=f_config.STATIC_FOLDER)
    app.config.from_object(f_config)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    socket = SocketIO(app)
    socket.init_app(app, cors_allowed_origins="*")

    api = Api(app)
    api.add_resource(Main, '/')

    socket.on_event('request_start', communicate_with_guider)
    socket.on_event('request_stop', disconnect_with_guider)
    
    return app, socket
