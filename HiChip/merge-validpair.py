import sys
import os

name = sys.argv[1] # hicpro-B73-rep1-H3K27ac

#out = open(sys.argv[2],'w')

for i in range(1,11):
    mydata = "hicpro-"+name + '-part' + str(i) + '/hic_results/data/part' + str(i)
    x = os.listdir(mydata)
    for y in x:
        if 'bam' in y:continue
        if '_' in y:
            z = y.split('_')
            last = z[-1]
        else:
            z = y.split('.')
            last = z[-1]
        nfile = name + '.' + last
        out = open(nfile,'a')
        myfile = mydata + '/' + y
        fh = open(myfile,'r')
        for line in fh:
            out.write(line)
        fh.close()
        out.close()
    # hicpro-B73-rep2-H3K27ac-part1/bowtie_results/bwt2/part1
    bwdata = "hicpro-"+name + '-part' + str(i) + '/bowtie_results/bwt2/part' + str(i)
    x1 = os.listdir(bwdata)
    for y1 in x1:
    # B73-H3K27ac-rep2-part1_B73v4-bowtie2.bwt2pairs.pairstat
        if 'bam' in y1:continue
        if 'pairstat' in y1:
            print (y1)
            z1 = y1.split('.')
            last = z1[-1]
            nfile = name+'.'+z1[1]+'.'+z1[2]
            out = open(nfile,'a')
            myfile = bwdata + '/' + y1
            fh = open(myfile,'r')
            for line in fh:
                out.write(line)
            fh.close()
            out.close()
