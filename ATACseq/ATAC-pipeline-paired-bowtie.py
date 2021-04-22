import sys
import subprocess as sp
import shlex
import os
import atac_toolkits as at


def selectindex(args="B73"):
    if args == "B73":
        myindex = "/home/springer/liang795/genomeinfo/B73v4-bowtie/B73v4-bowtie"
    elif args == "Mo17":
        myindex = "/home/springer/liang795/genomeinfo/Mo17-bowtie/Mo17-bowtie"
    elif args == "W22":
        myindex = "/home/springer/liang795/genomeinfo/W22-bowtie/W22-bowtie"
    elif args == "Oh43":
        myindex = "/home/springer/liang795/genomeinfo/Oh43-bowtie/Oh43-bowtie"
    return myindex


def selectgenome(args="B73"):
    if args == "B73":
        mygenome = "/home/springer/liang795/genomeinfo/genome-fasta/Zm-B73-REFERENCE-GRAMENE-4.0.fa"
    elif args == "Mo17":
        mygenome = "/home/springer/liang795/genomeinfo/genome-fasta/Zm-Mo17-REFERENCE-CAU-1.0.fa"
    elif args == "W22":
        mygenome = "/home/springer/liang795/genomeinfo/genome-fasta/Zm-W22-REFERENCE-NRGENE-2.0.fa"
    elif args == "Oh43":
        mygenome = "/home/springer/liang795/genomeinfo/genome-fasta/Zm-Oh43-REFERENCE-NAM-1.0.fa"
    return mygenome


def selectinput(args="B73"):
    if args == "B73":
        input_path = "/home/springer/liang795/ATAC-data/ATAC-Input1-B73.rmdups.bed"
    elif args == "Mo17":
        input_path = "/home/springer/liang795/ATAC-data/ATAC-Input1-Mo17.rmdups.bed"
    elif args == "W22":
        input_path = "/home/springer/liang795/ATAC-data/ATAC-Input1-W22.rmdups.bed"
    elif args == "Oh43":
        input_path = "/home/springer/liang795/ATAC-data/ATAC-Input1-Oh43.rmdups.bed"
    return input_path


read1 = sys.argv[1]  # absolute path for paired reads: ../ATAC-data/BC4A_S12_R1_001.fastq.gz
read2 = sys.argv[2]

work = sys.argv[3]  # work directory that put temp files in; please give absolute path
mygeno = sys.argv[4]
myindex = selectindex(mygeno)
mygenome = selectgenome(mygeno)
input_path = selectinput(mygeno)

print ("=============Preprocessing reads=====================")
trim_command = 'trim_galore --paired --fastqc --gzip {0} {1} --output_dir {2}'.format(read1, read2, work)
trim_args = shlex.split(trim_command)
trim = sp.Popen(trim_args)
trim.wait()

print ("=============Alignment and sorting=====================")
mread1 = read1.split('/')[-1]  # BC4A_S12_R1_001.fastq.gz
mread2 = read2.split('/')[-1]

newread1 = work + '/' + mread1.split('.')[0] + '_val_1.fq.gz'  # BC4A_S12_R1_001_1_val_1.fq.gz
newread2 = work + '/' + mread2.split('.')[0] + '_val_2.fq.gz'

prefix = mread1.split('_')[0]  # BC4A

newsam = work + '/' + prefix + '.sam'
newbam = work + '/' + prefix + '.bam'
print (newbam)
newsortedbam = work + '/' + prefix + '.sorted.bam'

hisat2_command1 = 'bowtie {3} -1 {0} -2 {1} -X 1000 -m 1 -v 2 --best --strata -S {2}'.format(newread1, newread2, newsam, myindex)
hisat2_args1 = shlex.split(hisat2_command1)
hisat2_1 = sp.Popen(hisat2_args1)
hisat2_1.wait()

bamfile = open(newbam, 'w')
stb_command = 'samtools view -bS {0}'.format(newsam)
stb_args = shlex.split(stb_command)
stb = sp.Popen(stb_args, stdout=bamfile)
stb.wait()
bamfile.close()

samtools_command = 'samtools sort {0} -o {1}'.format(newbam, newsortedbam)
samtools_args = shlex.split(samtools_command)
samtools = sp.Popen(samtools_args)
samtools.wait()

index_command = 'samtools index {0}'.format(newsortedbam)
index_args = shlex.split(index_command)
index = sp.Popen(index_args)
index.wait()

print ("=============Removing duplicates=====================")
rmdupsbam = work + '/' + prefix + '.rmdups.bam'

pc_command = 'picard MarkDuplicates -I {0} -M {1}_report.txt -O {2} --VALIDATION_STRINGENCY SILENT --ASSUME_SORTED true --REMOVE_DUPLICATES true'.format(newsortedbam, prefix, rmdupsbam)
pc_command_args = shlex.split(pc_command)
pc = sp.Popen(pc_command_args)
pc.wait()

rmdupsbed = work + '/' + prefix + '.rmdups.bed'
os.system("bam2bed < {0} > {1}".format(rmdupsbam, rmdupsbed))

print ("=============Call peaks and split original peaks=====================")
b2b_command = 'macs2 callpeak -t {0} -c {1} -g 2.1e9 --keep-dup all --nomodel --extsize 147 -n {2}'.format(rmdupsbed, input_path, prefix)
b2b_command_args = shlex.split(b2b_command)
b2b = sp.Popen(b2b_command_args)
b2b.wait()

try:
    print ("=============Postprocessing peaks=====================")
    peaks = work + '/' + prefix + '_peaks.narrowPeak'
    windowbed = '{0}/{1}.windows.bed'.format(work, prefix)
    at.split_window(peaks, windowbed, work, prefix)
    print ("=============Calculating tn5 integration frequency=====================")
    # calculating tn5 integration frequency
    rmdupsbed = work + '/' + prefix + '.rmdups.bed'
    tn5_read = "{0}/{1}_read.tn5.bed".format(work, prefix)
    count = at.tn5(rmdupsbed, tn5_read)
    print ("=============Determing coverage per window size=====================")
    # determing coverage per window size
    os.system('bedtools coverage -a {0}/{1}.windows.bed -b {0}/{1}_read.tn5.bed -counts > {0}/{1}_tmp.counts.txt'.format(work, prefix))

    tmp = work + '/' + '{0}_tmp.counts.txt'.format(prefix)
    split_coverage_bed = work + '/' + "{0}_relativetn5.split.coverage.bed".format(prefix)
    at.coverage_norm(tmp, split_coverage_bed, count)
    os.remove(tmp)

    print ("=============Merging bin sizes=====================")
    at.merge_bed(split_coverage_bed, work, prefix)

    print ("=============Extracting sequences and removing organelle sequences=====================")
    merged_bed = "{0}/{1}_relativetn5.merge.coverage.bed".format(work, prefix)
    merged_fa = work + '/' + "{0}_relativetn5.merge.coverage.fa".format(prefix)
    # filtering out organelle genome
    dat = "/home/springer/liang795/genomeinfo/OrganelleGenome/MP"
    os.system('bedtools getfasta -fi {0} -bed {1} -fo {2}'.format(mygenome, merged_bed, merged_fa))
    blast_out = work + '/' + "{0}-peak-organelle.fmt".format(prefix)
    os.system('blastn -query {0} -out {1} -db {2} -outfmt 7'.format(merged_fa, blast_out, dat))

    blackfile = "{0}/{1}_peak_organelle.black".format(work, prefix)
    at.ext_black(blast_out, blackfile)

    rmblack = "{0}/{1}_rmblack.bed".format(work, prefix)
    os.system('bedtools intersect -a {0} -b {1} -v | cut -f1-3 > {2}'.format(merged_bed, blackfile, rmblack))

    print ("===============Determining Final Summit for ACR========================================")
    final_file = work + '/' + "{0}_final.merge.coverage.bed".format(prefix)
    at.determine_summit(tn5_read, rmblack, final_file)
    #os.mkdir("{0}/Results-{1}".format(work, prefix))
    #os.move("{1}* {0}/Results-{1}".format(work, prefix))
except Exception as e:
    print(e)
