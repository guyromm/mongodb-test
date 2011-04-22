# -*- coding: utf-8 -*-
'''
This module create mapper for using in server application
'''

from routes import Mapper
from config import DEBUG

def get_map():
    " This function returns mapper object for dispatcher "
    map = Mapper()
    # Add routes here
    map.connect("index", '/', controller="controllers", action="index")
    #map.connect(None, '/api/start/game', controller="controllers", action="startgame")
    #map.connect(None, '/api/user/choice/{choice}', controller="controllers", action="handle_user_choice")
    #map.connect(None, '/chat/{channel_id:\d+}', controller="controllers", action="openchat")
    #map.connect(None, '/socket.io/channel{channel_id:\d+}', controller="controllers", action="handle_connect")
    # Connect static path to static content controller
    # You may specify here a static url or something like that

    if DEBUG:
        map.connect(None, '/static/{path_info:.*}', controller="static", action="index") #Handling static files

    return map