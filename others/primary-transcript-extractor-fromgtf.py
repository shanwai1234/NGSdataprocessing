#python ~/scripts/primary-transcript-extractor-fromgtf.py Zea_mays.B73_RefGen_v4.41.gtf > Zea_mays.B73_RefGen_v4.41.primary.gtf
import sys
import operator

fh = open(sys.argv[1],'r')

flist = []

for line in fh:
    flist.append(line)

fh.close()

mdict = {}

for line in flist:
    if line.startswith('#'):continue
    new = line.strip().split('\t')
    if new[2] == 'gene':
        gene = new[-1].split(';')[0].split(' ')[1].replace('"','')
        if gene not in mdict:
            mdict[gene] = {}
    if new[2] == 'transcript':
        trans = new[-1].split(';')[1].split(' ')[-1].replace('"','')
        region = abs(int(new[3])-int(new[4]))
        if trans not in mdict[gene]:
            mdict[gene][trans] = region

sdict = {}
for x in mdict:
    sorted_x = sorted(mdict[x].items(), key=operator.itemgetter(1), reverse=True)
    if x not in sdict:
        sdict[x] = sorted_x[0][0]

for line in flist:
    if line.startswith('#'):
        print (line.strip())
    else:
        new = line.strip().split('\t')
        if new[2] == 'gene':
            gene = new[-1].split(';')[0].split(' ')[1].replace('"','')
            print (line.strip())
        else:
            gene = new[-1].split(';')[0].split(' ')[1].replace('"','')
            trans = new[-1].split(';')[1].split(' ')[-1].replace('"','')
            if trans != sdict[gene]:continue
            print (line.strip())

fh.close()
