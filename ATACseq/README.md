# ATAC-processing
> interpreting code from: https://github.com/schmitzlab/Widespread-Long-range-Cis-Regulatory-Elements-in-the-Maize-Genome for producing high-confidence ACRs and redetermining summit per ACR.
# MOA-seq
The key step for using iSeg software
```
ln -vs /usr/lib/x86_64-linux-gnu/libboost_system.so /usr/lib/x86_64-linux-gnu/libboost_system.so.1.66.0
ln -vs /usr/lib/x86_64-linux-gnu/libboost_filesystem.so /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.66.0
```
plot bigwig Data
```
ComputeMatrix scale-regions -S /scratch.global/liang795/MOAseq/rmdupsbam/merged/MB.B73.log2ratio.10bpbin.absolute.sorted.bigWig /scratch.global/liang795/MOAseq/rmdupsbam/merged/MB.Mo17.log2ratio.10bpbin.absolute.sorted.bigWig -R cis-reQTL-control-heat-select-candidate-finalreQTLs.200bpextend.bed merged-cis-response-eQTL.complement.reQTL.bed --beforeRegionStartLength 1000 --regionBodyLength 400 --afterRegionStartLength 1000 -o test.mat.gz
```
> calling peaks using macs3 for MOAseq
the ```extsize``` is estimated using "samtools stats *bam"
```
macs3 callpeak -t Svm-C_STARAligned.max80.sortedByCoord.out.bam -g 3.96e8 -n SvmC -B -q 0.01 --nomodel --extsize 58
```
> calculating the effective genome size
```
1) samtools stats on the bam file to get the average fragment size, 2) "unique-kmers.py -q -k ${frg_length} -R ${eg_genome} ${Genome}" to get the mapable genome size. -k is the fragment length we get from samtools stats. -R is output. ${Genome} is the faidx of the genome fasta. Only take the first two columns of the faidx of the genome fasta.
```
