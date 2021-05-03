import sys
import os
import subprocess as sp
import shlex

read1 = sys.argv[1]
read2 = sys.argv[2]

data = '/home/springer/data_release/umgc/novaseq/210329_A00223_0519_BHW3NGDSXY/Springer_Project_080/'
#work = '/scratch.global/liang795/Heatpanel-RNAseq/'
work = '/scratch.global/liang795/Heatpanel-RNAseq-SNP'
'''
trim_command = 'trim_galore --paired --fastqc --gzip {0} {1} --output_dir {2}'.format(read1, read2, work)
trim_args = shlex.split(trim_command)
trim = sp.Popen(trim_args)
trim.wait()
'''
last1 = read1.split('/')[-1] # SRR1238715_1.fq.gz
last2 = read2.split('/')[-1] # SRR1238715_2.fq.gz
newread1 = last1.split('.')[0]+'_val_1.fq.gz' # SRR1238715_1_val_1.fq.gz
newread2 = last2.split('.')[0]+'_val_2.fq.gz'
prefix = newread1.split('_')[0] # SRR1238715
#samfile = open('{0}/{1}.bam'.format(work, prefix),'w')

#hisat2_command1 = 'hisat2 -x /home/springer/zhoux379/projects/genome/data/Zmays_B73/21_dbs/hisat2/B73_vt01/db -1 {2}/{0} -2 {2}/{1} --rna-strandness R -p 8 -k 20 --no-mixed --no-discordant --met-stderr --new-summary'.format(newread1, newread2, work)
#hisat2_command1 = 'hisat2 -x /home/springer/liang795/genomeinfo/Mo17-hisat2/Mo17-hisat2 -1 {2}/{0} -2 {2}/{1} --rna-strandness R -p 8 -k 20 --no-mixed --no-discordant --met-stderr --new-summary'.format(newread1, newread2, work)
#hisat2_command1 = 'hisat2 -x /home/springer/liang795/genomeinfo/B73v4-Mo17SNP-Lai-Hisat2-Nmasked/B73v4-Mo17SNPLai-Nmasked-hisat2 -1 {2}/{0} -2 {2}/{1} --rna-strandness R -p 8 -k 20 --no-softclip --no-mixed --no-discordant --met-stderr --new-summary'.format(newread1, newread2, work)
'''
hisat2_command1 = 'hisat2 -x /home/springer/liang795/genomeinfo/B73v4-Hisat2/B73v4-Hisat2 -1 {2}/{0} -2 {2}/{1} --rna-strandness R -p 10 --no-softclip --no-mixed --no-discordant --met-stderr --new-summary'.format(newread1, newread2, work)
hisat2_args1 = shlex.split(hisat2_command1)
hisat2_command2 = 'samtools view -bS -F 8'
hisat2_args2 = shlex.split(hisat2_command2)
hisat2_1 = sp.Popen(hisat2_args1, stdout=sp.PIPE)
hisat2_2 = sp.Popen(hisat2_args2, stdin=hisat2_1.stdout, stdout=samfile)
hisat2_2.wait()

samtools_command = 'samtools sort {0}/{1}.bam -o {0}/{1}.sort.bam'.format(work, prefix)
samtools_args = shlex.split(samtools_command)
samtools = sp.Popen(samtools_args)
samtools.wait()
samtools_command = 'samtools index {0}/{1}.sort.bam'.format(work, prefix)
samtools_args = shlex.split(samtools_command)
samtools = sp.Popen(samtools_args)
samtools.wait()
'''
ref = '/home/springer/liang795/genomeinfo/genome-fasta/Zm-B73-REFERENCE-GRAMENE-4.0.fa'
variant = '/home/springer/liang795/projects-in-nathan-lab/heatstress-panel/Selected-Widiv-SNPs/Selected-110genos-Widiv-filtered-chr.vcf'
#variant = '/home/springer/liang795/projects-in-nathan-lab/heatstress-panel/Selected-Widiv-SNPs/Selected-110genos-Widiv-filtered-chr.vcf'
#newsortedbam = work + '/' + prefix + '.sorted.bam'
'''
pc_command = 'picard MarkDuplicates -I {0}/{1}.sort.bam -M {0}/{1}_report.txt -O {0}/{1}.rmdups.bam --VALIDATION_STRINGENCY SILENT --ASSUME_SORTED true --REMOVE_DUPLICATES true'.format(work, prefix)
pc_command_args = shlex.split(pc_command)
pc = sp.Popen(pc_command_args)
pc.wait()

splitnc_command = 'gatk SplitNCigarReads -R {0} -I {1}/{2}.rmdups.bam -O {1}/{2}.splitnc.bam'.format(ref, work, prefix)
splitnc_command_args = shlex.split(splitnc_command)
splitnc = sp.Popen(splitnc_command_args)
splitnc.wait()

group_command = 'picard AddOrReplaceReadGroups -I {0}/{1}.splitnc.bam -O {0}/{1}.splitnc.group.bam -RGID 1 -RGLB lib2 -RGPL illumina -RGPU unit1 -RGSM 3'.format(work, prefix)
group_command_args = shlex.split(group_command)
group = sp.Popen(group_command_args)
group.wait()

base_command = 'gatk BaseRecalibrator -I {0}/{1}.splitnc.group.bam -R {2} --known-sites {3} -O {0}/{1}.recal_data.table'.format(work, prefix, ref, variant)
base_command_args = shlex.split(base_command)
base = sp.Popen(base_command_args)
base.wait()
'''
recap_command = 'gatk ApplyBQSR -I {0}/{1}.splitnc.group.bam -R {2} --bqsr-recal-file {0}/{1}.recal_data.table -O {0}/{1}.bqsr.bam'.format(work, prefix, ref)
recap_command_args = shlex.split(recap_command)
recap = sp.Popen(recap_command_args)
recap.wait()

snp_command = 'gatk --java-options "-Xmx20g" HaplotypeCaller -R {0} -I {1}/{2}.bqsr.bam -O {1}/{2}.vcf'.format(ref, work, prefix)
snp_command_args = shlex.split(snp_command)
snp = sp.Popen(snp_command_args)
snp.wait()
'''
teexp_command = 'python /home/springer/liang795/scripts/TE-expression/TEexpression-pip.py {0}/{1}.sort /home/springer/liang795/genomeinfo/B73.v4.41.pengformat.structuralTEv2.2020.02.03.filteredTE.disjoined.gff3'.format(work, prefix)
teexp_args = shlex.split(teexp_command)
teexp = sp.Popen(teexp_args)
teexp.wait()
os.system('rm -rf {0}/{1} {0}/{2} {0}/{3}.bam {0}/{3}.sort.converted.bam'.format(work, newread1, newread2, prefix))
'''
