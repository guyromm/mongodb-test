# -*- coding: utf-8 -*-

# Here is the code for communicate with MongoDB
from noodles.http import Response, ajax_response
from noodles.templates import render_to
from pymongo import Connection
import pymongo, time, random, string

def get_collection():
    connection = Connection()
    db = connection.test_database
    return db.test_collection
    
def random_str(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))

@render_to('testbench.html')
def index(request):
    return {}

@ajax_response    
def checkMongo(request):
    try:
        connection = Connection()
    except pymongo.errors.AutoReconnect:
        connection = None
    if connection: success = True
    else: success = False
    return {'success': success}

@ajax_response
def create_items(request, amount):
    "Create an amount of test items and insert it to test collection"
    test_collection = get_collection()
    def get_test_item():
        test_item = {
                'no': random_str(4),
                'such': random_str(8),
                'thing': random_str(16),
                'as': random_str(32),
                'free': random_str(64),
                'lunch': random_str(128),
            }
        return test_item
    start = time.time()
    for i in range(int(amount)):
        test_collection.insert(get_test_item())
    delta = time.time() - start
    return {'success': True, 'time': delta, 'count': test_collection.count()}
    
@ajax_response
def get_count(request):
    "Get the count of our test collection"
    start = time.time()
    test_collection = get_collection()
    delta = time.time() - start
    return {'time': delta, 'count': test_collection.count()}
    
@ajax_response
def get_random(request):
    "Get random testing item from test_collection"
    start = time.time()
    test_collection = get_collection()
    randomNum = random.randint(0, test_collection.count())
    item = test_collection.find().limit(-1).skip(randomNum).next()
    delta = time.time() - start
    return {'item': item, 'time': delta}
    
@ajax_response
def insert_marker(request, uid):
    start = time.time()
    test_collection = get_collection()
    marker = {'text': "Hey-hey, i'm a marker", 'marker_id': uid}
    test_collection.insert(marker)
    delta = time.time() - start
    return {'success': True, 'time': delta}
    
@ajax_response
def get_marker(request, uid):
    start = time.time()
    test_collection = get_collection()
    marker = test_collection.find_one({'marker_id': uid})
    delta = time.time() - start
    if marker: success = True
    else: success = False
    return {'success': success, 'time': delta}
    
@ajax_response
def drop_collection(request):
    start = time.time()
    test_collection = get_collection()
    test_collection.drop()
    delta = time.time() - start
    return {'success': True, 'time': delta}
