#!/bin/bash
#SBATCH --partition=amdsmall
#SBATCH --time=20:00:00
#SBATCH --mem-per-cpu=20g
#SBATCH --job-name=B73v4
#SBATCH --error=B73v4.err
#SBATCH --output=B73v4.out
# sbatch reduced_genome_modified.sh dpnii B73v4 100
enzyme=$1
genome=$2
fl=$3 # 150-50 = 100

#get coordinates for all RE sites in the genome
oligoMatch ${enzyme}.fa ${genome}.fa ${genome}_${enzyme}_restriction_sites_oligomatch.bed
#get coordinates of upstream fragments
awk -v fl=$fl1 '{print $1"\t"$2-fl"\t"$2}' ${genome}_${enzyme}_restriction_sites_oligomatch.bed >up.txt
#get coordinates of downstream fragments
awk -v fl=$fl2 '{print $1"\t"$3"\t"$3+fl}' ${genome}_${enzyme}_restriction_sites_oligomatch.bed > down.txt
#combine up and downstream fragments
cat up.txt down.txt > ${genome}_${enzyme}_flanking_sites_${fl}_2.bed
#remove any fragments with negative coordinates
awk '{if($2 >= 0 && $3 >=0) print $0}' ${genome}_${enzyme}_flanking_sites_${fl}_2.bed | grep -v -E 'random|JH|GL' - | sort -k1,1 -k2,2n | uniq  > ${genome}_${enzyme}_flanking_sites_${fl}_unique_2.bed
#get the sequence of unique flanking coordinates
fastaFromBed -fi ${genome}.fa -bed ${genome}_${enzyme}_flanking_sites_${fl}_unique_2.bed -fo ${genome}_${enzyme}_flanking_sequences_${fl}_unique_2.fa
#get only unique sequences from FASTA file
grep -v '^>' ${genome}_${enzyme}_flanking_sequences_${fl}_unique_2.fa | sort | uniq -i -u | grep -xF -f - -B 1 ${genome}_${enzyme}_flanking_sequences_${fl}_unique_2.fa | grep -v '^--' > ${genome}_${enzyme}_flanking_sequences_${fl}_unique.fa

#remove unwanted intermediate files
rm up.txt
rm down.txt

#make a BED file of unqiue sequences
grep '^>' ${genome}_${enzyme}_flanking_sequences_${fl}_unique.fa > ${genome}_${enzyme}_flanking_sites_${fl}_unique.bed
sed -i 's/>//g' ${genome}_${enzyme}_flanking_sites_${fl}_unique.bed
sed -i 's/:\|-/\t/g' ${genome}_${enzyme}_flanking_sites_${fl}_unique.bed

exit 0;