import sys
import pybedtools
import pandas as pd
import os
from bx.intervals.intersection import Intersecter, Interval
import operator


def tn5(file1, file2):
    # determining tn5 integration sites
    count = 0
    with open(file1, 'r') as fh, open(file2, 'w') as out:
        for line in fh:
            new = line.strip().split('\t')
            if new[5] == "+":
                out.write(new[0] + '\t' + str(int(new[1]) + 4) + '\t' + str(int(new[1]) + 5) + '\n')
            else:
                out.write(new[0] + '\t' + str(int(new[2]) - 6) + '\t' + str(int(new[2]) - 5) + '\n')
            count += 1
    return count


def coverage_norm(file1, file2, total, size=2.1e9):
    # determining normalized coverage
    with open(file1, 'r') as fh, open(file2, 'w') as out:
        for line in fh:
            new = line.strip().split('\t')
            last = (size * int(new[4])) / (int(total) * (int(new[2]) - int(new[1])))
            out.write('\t'.join(new[:4]) + '\t' + str(last) + '\n')


def split_window(file1, output, work, prefix):
    # spliting original ATAC regions into several pieces
    x = pybedtools.BedTool(file1)
    y = pybedtools.BedTool().window_maker(w=50, s=25, b=x) # window as 50bp, and stepping as 25bp
    y1 = y.sort()
    y1.saveas("{0}/{1}_sortmerge.bed".format(work, prefix))
    with open("{0}/{1}_sortmerge.bed".format(work, prefix), 'r') as fh, open(output, 'w') as out:
        b = 0
        for line in fh:
            new = line.strip().split('\t')
            mybin = 'bin_' + str(b)
            out.write('\t'.join(new[:3]) + '\t' + mybin + '\n')
            b += 1
    os.remove("{0}/{1}_sortmerge.bed".format(work, prefix))


def merge_bed(file1, work, prefix):
    '''
    B73V4_ctg10  48746  48796  bin_1  23.31300
    '''
    print ("starting")
    x = pd.read_table(file1, header=None)
    x.columns = ['Chr', 'Start', 'Stop', 'Bin', 'Coverage']
    print (x.head())
    y = x[x['Coverage'] > 25] # filtering bins with coverage > 25
    y.columns = range(y.shape[1])
    print (y.head())
    y.to_csv("{0}/{1}_tmp.bed".format(work, prefix), index=False, sep='\t')
    os.system("sed -i 1d {0}/{1}_tmp.bed".format(work, prefix))
    a = pybedtools.BedTool("{0}/{1}_tmp.bed".format(work, prefix))
    b1 = a.sort()  # sort bed files
    b2 = b1.merge(d=150)  # merge bed files allowing 150bp gap
    b2.saveas("{0}/{1}_tmp_regions.bed".format(work, prefix))
    x1 = pd.read_table("{0}/{1}_tmp_regions.bed".format(work, prefix), header=None)
    x1.columns = ['Chr', 'Start', 'Stop']
    x1['Diff'] = x1['Stop'].sub(x1['Start'], axis=0)
    print (x1.head())
    y1 = x1[x1['Diff'] > 50]  # filter ACR with length > 50
    y2 = y1.iloc[1:, :3]
    y2.to_csv("{0}/{1}_relativetn5.merge.coverage.bed".format(work, prefix), index=False, sep='\t')
    os.system("sed -i 1d {0}/{1}_relativetn5.merge.coverage.bed".format(work, prefix))
    os.remove("{0}/{1}_tmp_regions.bed".format(work, prefix))
    os.remove("{0}/{1}_tmp.bed".format(work, prefix))


def ext_black(file1, file2):
    # removing organelle genome
    pos = set([])
    with open(file1, 'r') as fh, open(file2, 'w') as out:
        for line in fh:
            if line.startswith('#'):
                continue
            new = line.strip().split('\t')
            pos.add(new[0])

        for x in sorted(list(pos)):
            y = x.split(':')
            chrom = y[0]
            p = y[1].split('-')
            mypos = chrom + '\t' + p[0] + '\t' + p[1] + '\n'
            out.write(mypos)


def determine_summit(tfile, file1, file2):
    # tfile is calculated tn5 bed file
    mdict = {}  # storing tn5 density information
    with open(tfile, 'r') as fh:
        for line in fh:
            new = line.strip().split('\t')
            if new[0] not in mdict:
                mdict[new[0]] = {}
            if new[1] not in mdict[new[0]]:
                mdict[new[0]][new[1]] = 0
            mdict[new[0]][new[1]] += 1

    intersect_dict = {}

    for x in mdict:
        mychr = x
        if mychr not in intersect_dict:
            intersect_dict[mychr] = Intersecter()
        for y in mdict[x]:
            st = int(y)
            sp = int(y)
            den = mdict[x][y]
            name = str(st) + '_' + str(den)
            intersect_dict[mychr].add_interval(Interval(st, sp, value=name))

    with open(file1, 'r') as t, open(file2, 'w') as out:
        for line in t:
            y = line.strip().split('\t')
            mychr = y[0]
            start = int(y[1])
            stop = int(y[2])
            a = intersect_dict[mychr].find(start, stop)
            if len(a) > 0:
                mdict = {}
                for b in a:
                    if b.value not in mdict:
                        mdict[b.value] = float(b.value.split('_')[1])
                sorted_x = sorted(mdict.items(), key=operator.itemgetter(1), reverse=True)
                m = 'Summit=' + sorted_x[0][0].split('_')[0]
                out.write(line.strip() + '\t' + m + '\n')
