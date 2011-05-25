#!/usr/bin/python
"""this parses the output of python-cloudservers' cloudservers boot command which creates a new machine"""

fp = open('installs.txt','r')
ip = None;  name=None
while True:
    line = fp.readline()
    if not line: break
    vals = line.split('|')
    if len(vals)<2:  continue
    vals = [val.strip() for val in vals]
    if vals[1]=='Property': continue
    if vals[1]=='addresses':
        ips = eval(vals[2])
        ip = ips['public'][0]
    elif vals[1]=='name':
        name = vals[2]
    else:
        pass #raise Exception(vals)
    if ip and name:
        pat="""Host %s
     HostName %s
     User %s
     ForwardAgent yes
     IdentityFile ~/.ssh/id_rsa
"""%(name,ip,'root')
        print pat
        ip = None ; name=None
fp.close()
