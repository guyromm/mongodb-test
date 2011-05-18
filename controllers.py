# -*- coding: utf-8 -*-

# mongoimport -h localhost -d test_database -c test_collection --type json testdumps.log
# Here is the code for communicate with MongoDB
from noodles.http import Response, ajax_response
from noodles.templates import render_to
from pymongo import Connection
import pymongo, time, random, string, gevent
from pymongo import ASCENDING, DESCENDING
import subprocess, json

connection = None

def get_collection():
    global connection
    if not connection:
        connection = Connection(host='localhost',port=10000)
    else:
        pass
    db = connection.test_database
    collection = db.test_collection
    #collection.ensure_index('indexed_id', unique = True)
    return collection
    
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
    
        return {
                'no': 'dftg',
                'such': 'fkidjifx',
                'thing': 'hfsdjfhdjkshsdfkldjsgergdsf',
                'as': 'dsgkljadgndsfhgodfgbdhdfhkghhhhhhtrjioesrgjeronigergioer',
                'free': 'sdgjkdsgn jdsgneropgnmeropgunnodsjsdkgjndsgkdl;krkgnl;sdgkdsfgjjfpirsgkdjsiorogybriougnerpognepr',
                'lunch': 'wgjnsjklsdnflguboerugnjdfklgjsdjkgbdsfkln nasdlfjmasopfeopfuniofu84yt784y30fu 4fnfue9fnu32urfn849yrbydfwe87yrf8y832ry834yr348ty8ty348ty3484y38t349t8y3498yrbyb89ewyrf9yisdbfiu',
            }
    
    #docs = [get_test_item() for i in range(int(amount))]
    #test_collection.insert(docs) 
    start = time.time()
    #amount_per_greenlet = int(int(amount) / GREENLETS)
    #for i in range(int(amount)):
    #    test_collection.insert(get_test_item()) 
    
    """ Insert by series (20 per time) """
    records_per_iter = 20
    count_of_iter = int(amount)/records_per_iter
    
    for i in range(count_of_iter):
        docs = [get_test_item() for e in range(records_per_iter)]
        test_collection.insert(docs) 
    
    delta = time.time() - start
    return {'success': True, 'time': delta, 'count': test_collection.count()}
    
@ajax_response
def get_count(request):
    "Get the count of our test collection"
    start = time.time()
    test_collection = get_collection()
    delta = time.time() - start
    return {'time': delta, 'count': test_collection.count(), 'success': True}
    
@ajax_response
def get_random(request):
    "Get random testing item from test_collection"
    start = time.time()
    test_collection = get_collection()
    randomNum = random.randint(0, test_collection.count())
    item = test_collection.find().limit(-1).skip(randomNum).next()
    delta = time.time() - start
    return {'item': item, 'time': delta, 'success': True}
    
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
def insert_indexed_marker(request, uid):
    start = time.time()
    test_collection = get_collection()
    marker = {'text': "Hey-hey, i'm an indexed marker", 'indexed_id': uid}
    test_collection.insert(marker)
    delta = time.time() - start
    return {'success': True, 'time': delta}
    
@ajax_response
def get_indexed_marker(request, uid):
    start = time.time() 
    test_collection = get_collection()
    marker = test_collection.find_one({'indexed_id': uid})
    delta = time.time() - start
    if marker: success = True
    else: success = False
    return {'success': success, 'time': delta}    

@ajax_response
def create_index(request):
    "Create index for marker"
    start = time.time() 
    test_collection = get_collection()
    test_collection.create_index('marker_id')
    delta = time.time() - start
    return {'success': True, 'time': delta}

@ajax_response
def drop_index(request):
    "Drop index for the marker"
    start = time.time() 
    test_collection = get_collection()
    try:
        test_collection.drop_index('marker_id_1')
    except pymongo.errors.OperationFailure:
        pass
    delta = time.time() - start
    return {'success': True, 'time': delta}

@ajax_response
def drop_collection(request):
    start = time.time()
    test_collection = get_collection()
    test_collection.drop()
    delta = time.time() - start
    return {'success': True, 'time': delta}
