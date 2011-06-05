#!/usr/bin/python

fp = open('installed.txt','r')
ip = None;  name=None
while True:
    line = fp.readline().strip()
    if not line: break
    vals = [val.strip() for val in line.split('|')]
    if len(vals)==1: continue
    if vals[1]=='ID': continue
    hn = vals[2]
    pip = vals[4]
    sip = vals[5]
    pat="""Host %s
     HostName %s
     User %s
     ForwardAgent yes
     IdentityFile ~/.ssh/id_rsa
"""%(hn,pip,'root')
    print pat
    

