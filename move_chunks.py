#!/usr/bin/python

from commands import getstatusoutput as gso
import json,time

colname = 'sharded_30nodes_nobalancer'
mongos = open('masters.txt').read().strip().split('\n')[0]
simulate=False
runonce=True

while True:
    countcmd = """cat slaves.txt | xargs -P0 -n1 -I{}     ssh {} 'annotate-output +{} mongo --eval "db.%s.count()" --quiet localhost:27017/test_database' | egrep -v '(Finished|Started)' | awk '{print $3" "$1}' |sort -n"""%(colname)

    st,op = gso(countcmd)
    assert st==0
    sizes = op.split("\n")
    targetshard = sizes[0].split(' ')[1]
    sourceshard = sizes[-1].split(' ')[1]
    print '%s vs %s'%(sizes[0],sizes[-1])
    print 'going to move a chunk %s -> %s'%(sourceshard,targetshard)
    
    findchunk = """db.chunks.find({shard:'\"'%s'\"',ns:'\"'test_database.%s'\"'})"""%(sourceshard,colname)
    findchunkcmd ="""ssh %s 'echo "%s" | mongo --quiet localhost:10000/config'"""%(mongos,findchunk)
    #print findchunkcmd
    st,op = gso(findchunkcmd)
    assert st==0
    chunksop = '['+','.join(op.split('\n')[1:-2])+']'
    #print chunksop
    chunks = json.loads(chunksop)
    print 'loaded %s chunks. moving a random one'%len(chunks)
    movcmd = """db.runCommand({moveChunk:'\"'test_database.%s'\"',find:{indexed_id:'\"'%s'\"'},to:'\"'%s'\"'})"""%(colname,chunks[0]['min']['indexed_id'],targetshard)
    movcmdf = """ssh %s 'echo "%s" | mongo localhost:10000/admin'"""%(mongos,movcmd)
    print movcmdf
    if simulate:
        print 'simulate. sleeping'
        time.sleep(1)
    else:
        #print op
        st,op = gso(movcmdf) ; assert st==0
    if runonce:
        break
