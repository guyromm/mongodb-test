# -*- coding: utf-8 -*-

# Start testing application here
import urllib2
from datetime import datetime
import json
import random

PORT = 8090
HOST = 'localhost'
base_url = 'http://%s:%i' % (HOST, PORT)
MARKERS_COUNT = 0

def send_request(url):
    return urllib2.urlopen(base_url + url).read()

if __name__ == '__main__':
    print "Hello, let's crash Mongo DB ))"
    
    # Output csv file
    csv_outf = open('metrics_%s.csv' % datetime.now().strftime('%d.%m_%H:%M:%S'), 'wb')
    
    try:
        resp = send_request('/check/mongo/connect')
    except urllib2.URLError:
        print "Server is down"
        exit(0)
    send_request('/drop/index')
    # Insert at first 50 markers
    for i in range(50): send_request('/insert/marker/%i' % i)
    MARKERS_COUNT += 50
    
    csv_outf.write('iteration;count;average_not_indexed;create_index_time;average_indexed;drop_index;\n')
    
    for i1 in range(100):
        for i2 in range(10):
            print send_request('/create/docs/10000')
            send_request('/insert/marker/%i' % (MARKERS_COUNT + i2))
        MARKERS_COUNT += 10
        resp = send_request('/get/count')
        resp = json.loads(resp)
        count_of_records = resp['count']
        print "Iteration is ready. Count of records is %s" % count_of_records
        print 'Perform reading'
        # Unindexed reading
        for i3 in range(50):
            resp_times = []
            resp = send_request('/get/marker/%i' % random.randint(0, MARKERS_COUNT))
            resp = json.loads(resp)
            resp_times.append(float(resp['time']))
        average_resp_time = sum(resp_times, 0.0) /  len(resp_times)
        average_resp_time = str(average_resp_time).replace('.', ',')
        print "Average response time is %s s." % average_resp_time
        
        
        # Create index for markers
        creat_index_time = json.loads(send_request('/create/index'))['time']
        creat_index_time = str(creat_index_time).replace('.', ',')
        # Indexed read
        for i4 in range(50):
            resp_times = []
            resp = send_request('/get/marker/%i' % random.randint(0, MARKERS_COUNT))
            resp = json.loads(resp)
            resp_times.append(float(resp['time']))
        average_indexed = sum(resp_times, 0.0) /  len(resp_times)
        average_indexed = str(average_indexed).replace('.', ',')
        print "Average response time after indexing is %s s." % average_indexed
        
        drop_index_time = json.loads(send_request('/drop/index'))['time']
        drop_index_time = str(drop_index_time).replace('.', ',')
        
        csv_outf.write('%i;%i;%s;%s;%s;%s;\n' % 
            (i1, count_of_records, average_resp_time, creat_index_time, average_indexed, drop_index_time))

    print send_request('/get/count')
    print send_request('/drop/collection')
    
