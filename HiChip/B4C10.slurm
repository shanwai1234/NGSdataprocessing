#!/bin/bash -l
#SBATCH --partition=amdsmall
#SBATCH --time=30:00:00
#SBATCH --ntasks=4
#SBATCH --mem=20g
#SBATCH --job-name=B4C10
#SBATCH --error=B4C10.err
#SBATCH --output=B4C10.out

module load java
cd /scratch.global/liang795/4C-seq/4Cfastq
bowtie2 -p 12 -N 0 -5 25 --un B4C10_unaligned.sam -x /home/springer/liang795/genomeinfo/4Cker-index/B73v4-MaskedMo17SNP/B73v4-MaskedMo17SNP_dpnii_flanking_sequences_125_unique -U B4C10_L3_A002.R1.fastq.gz -S B4C10_aligned.sam 
