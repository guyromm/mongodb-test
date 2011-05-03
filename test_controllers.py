# -*- coding: utf-8 -*-
"""
    Our main test logic is here. We implement here inserting of chunk of testing data
    and get indexed item function.
"""
from controllers import get_collection
from noodles.http import Response, ajax_response


def get_test_item(uid):
        #print uid
    return {
                'indexed_id': md5.new(str(uid)).hexdigest(),
                'no': 'dftg',
                'such': 'fkidjifx',
                'thing': 'hfsdjfhdjkshsdfkldjsgergdsf',
                'as': 'dsgkljadgndsfhgodfgbdhdfhkghhhhhhtrjioesrgjeronigergioer',
                'free': 'sdgjkdsgn jdsgneropgnmeropgunnodsjsdkgjndsgkdl;krkgnl;sdgkdsfgjjfpirsgkdjsiorogybriougnerpognepr',
                'lunch': 'wgjnsjklsdnflguboerugnjdfklgjsdjkgbdsfkln nasdlfjmasopfeopfuniofu84yt784y30fu 4fnfue9fnu32urfn849yrbydfwe87yrf8y832ry834yr348ty8ty348ty3484y38t349t8y3498yrbyb89ewyrf9yisdbfiu',
    }


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
