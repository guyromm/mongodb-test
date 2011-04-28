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
    map.connect(None, '/check/mongo/connect', controller="controllers", action="checkMongo")
    map.connect(None, '/create/docs/{amount:\d+}', controller="controllers", action="create_items")
    map.connect(None, '/drop/collection', controller="controllers", action="drop_collection")
    map.connect(None, '/get/random', controller="controllers", action="get_random")
    map.connect(None, '/get/count', controller="controllers", action="get_count")
    map.connect(None, '/insert/marker/{uid:\d+}', controller="controllers", action="insert_marker")
    map.connect(None, '/get/marker/{uid:\d+}', controller="controllers", action="get_marker")
    map.connect(None, '/insert/indexed/{uid:\d+}', controller="controllers", action="insert_indexed_marker")
    map.connect(None, '/get/indexed/{uid:\d+}', controller="controllers", action="get_indexed_marker")
    map.connect(None, '/create/index', controller="controllers", action="create_index")
    map.connect(None, '/drop/index', controller="controllers", action="drop_index")
    map.connect(None, '/insert/100k', controller="controllers", action="insert_100k")
    
    if DEBUG:
        map.connect(None, '/static/{path_info:.*}', controller="static", action="index") #Handling static files

    return map
