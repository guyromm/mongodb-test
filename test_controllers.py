# -*- coding: utf-8 -*-
"""
    Our main test logic is here. We implement here inserting of chunk of testing data
    and get indexed item function.
"""
from controllers import get_collection
from noodles.http import Response, ajax_response
import time, md5,random
import logging
log = logging.getLogger(__name__)
letters = 'abcdefghijklmopqrstuvwxyz'
testfields={}

def get_test_item(uid):
    global letters,testfields
        #print uid
    rt= {
                'indexed_id': md5.new(str(uid)).hexdigest(),
    }
    #we try to come up with a sort-of random item
    for i in range(10):
        if i not in testfields:
            nstr=''
            strlen = (i+1)*4
            for si in range(strlen):
                nstr+=random.choice(letters)
            testfields[i]=nstr
        else:
            testfields[i] = ''.join(list(testfields[i])[1:])
            testfields[i]+=random.choice(letters)
            nstr = testfields[i]
        rt['field_%s'%((i+1)*4)]=nstr
    return rt


@ajax_response
def insert_100k(request, count):
    "Insert 100k records from dumps"
    # Mongo insert command
    #mongoimport -h localhost -d test_database -c test_collection --type csv -f no,such,thing,as,free,lunch testdumps.csv --upsert
    # mongoimport -h localhost -d test_database -c test_collection --type json -f no,such,thing,as,free,lunch dumps.son --upsert
    #cmd ='mongoimport -h localhost -d test_database -c test_collection --type json -f indexed_id,no,such,thing,as,free,lunch dump.son --upsert'
    #cmd = 'mongoimport -h localhost -d test_database -c test_collection --type csv -f indexed_id,no,such,thing,as,free,lunch testdumps.csv --upsert'

    
    def perform_dump(count):
        count = int(count)
        dump_json = open('dump.son', 'wb')
        for i in range(100000*count, 100000*(count+1)):
            dump_json.write(json.dumps(get_test_item(i)) + '\n')
        dump_json.close()
        
    records_per_iter = 20
    count_of_iter = 5000
    start = time.time()
    test_collection = get_collection()
    for i in range(count_of_iter):
        docs = [get_test_item(100000*int(count) + i*20 + e) for e in range(records_per_iter)]
        test_collection.insert(docs)
#    perform_dump(count)
#    res = subprocess.call(cmd, shell=True)
    delta = time.time() - start
    return {'success': True, 'time': delta, 'count': test_collection.count()}

import pymongo

@ajax_response
def insert_1m(request,amt, count):
    count = int(count)
    if amt=='1m':
        amt=1000000
    elif amt=='100k':
        amt=100000
    elif amt=='10k':
        amt=10000
    else:
        amt = int(amt)

    noindex = bool(request.params.get('noindex',False))
    log.info('starting off with a count of %s'%count)
    records_per_iter = 100
    count_of_iter = amt / records_per_iter
    log.info('running %s iterations of %s records each. noindex=%s'%(count_of_iter,records_per_iter,noindex))
    start = time.time()
    log.info('getting collection')
    test_collection = get_collection()
    if not noindex:
        try:
            log.info('dropping index (if exists)')
            test_collection.drop_index('indexed_id_1')
        except pymongo.errors.OperationFailure:
            log.info('index did not exist previously, lols')
    #get the current amount of items
    curitems = test_collection.count()
    log.info('currently have %s items'%curitems)
    log.info('starting off insert')
    inserts=[]
    
    for cnt in range(count):
        start_ins = time.time()
        log.info('starting ins %s'%cnt)
        for i in range(count_of_iter):
            ins_start = time.time()
            if i % 1000 ==0: 
                log.info('batch %s, generating %s docs'%(i,records_per_iter))
            #docs = [get_test_item(1000000*int(count) + i*records_per_iter + e) for e in range(records_per_iter)]
            docs = []
            for e in range(records_per_iter):
                curitems+=1
                docs.append((get_test_item(curitems)))
            test_collection.insert(docs)
            if i % 1000==0:
                log.info('inserted, curitems = %s'%curitems)
        ins_delta = time.time() - start_ins
        ins = {'amt':amt,'count':cnt,'time':ins_delta,'curitems':curitems}
        log.info('insert %s done in %s: %s'%(cnt,ins_delta,ins))
        inserts.append(ins)
    log.info('insert phase done')
#    perform_dump(count)
#    res = subprocess.call(cmd, shell=True)
    if not noindex:
        try:
            log.info('creating index')
            test_collection.ensure_index('indexed_id', unique = True)
        except pymongo.errors.DuplicateKeyError:
            log.error('FAILURE TO CREATE UNIQUE INDEX')
            return {'success':False,'message':'unique index could not be created'}
    delta = time.time() - start
    log.info('took us %s'%delta)
    return {'success': True, 'time': delta, 'count': test_collection.count(),'inserts':inserts}

@ajax_response
def get_item(request, uid):
    start = time.time()
    test_collection = get_collection()
    marker = test_collection.find_one({'indexed_id': md5.new(uid).hexdigest()})
    print marker
    if marker:
        success = True
    else:
        success = False
    delta = time.time() - start
    return {'success': success, 'time': delta}
