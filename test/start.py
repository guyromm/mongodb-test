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
    csvav_outf = open('average_%s.csv' % datetime.now().strftime('%d.%m_%H:%M:%S'), 'wb')
    
    try:
        resp = send_request('/check/mongo/connect')
    except urllib2.URLError:
        print "Server is down"
        exit(0)
    # Insert at first 50 indexed markers
    for i in range(50): send_request('/insert/indexed/%i' % i)
    MARKERS_COUNT += 50
    
    csv_outf.write('iteration;count;get_time;\n')
    
    for i1 in range(1000):

        print send_request('/create/docs/100000')
        resp = send_request('/get/count')
        resp = json.loads(resp)
        count_of_records = resp['count']
        print "Iteration is ready. Count of records is %s" % count_of_records
        print 'Perform reading'
        
        for i2 in range(50):
            resp_times = []
            resp = send_request('/get/indexed/%i' % i2)
            resp = json.loads(resp)
            resp_times.append(resp['time'])
            csv_outf.write('%i;%i;%s;\n' % (i1, count_of_records, str(resp['time']).replace('.', ',')))
        average_resp_time = sum(resp_times, 0.0) /  len(resp_times)
        print "Average response time is %f s." % average_resp_time
        csvav_outf.write('%i;%i;%s;\n' % (i1, count_of_records, str(average_resp_time).replace('.', ',')))
        
    print send_request('/get/count')
    print send_request('/drop/collection')
    
