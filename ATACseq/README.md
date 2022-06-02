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
# Commands for calling peaks of MOA-seq

> Comparing difference between bigwig files
```
bigwigCompare -b1 B_H.q255.20.bp.rand.EG.bw -b2 B_C.q255.20.bp.rand.EG.bw --scaleFactors 1:1 -bs 20 -o B73_Diff_20bp.bedGraph -of bedgraph
```
> merged B-C
```
macs3 callpeak -t B_C1_3.merged.max80.255.bam -g 1.24e9 --buffer-size 10000000 --keep-dup all -n B_C1_q001 -q 0.01 --nomodel --extsize 59 --min-length 59 --max-gap 118
```
> peak calling for bed files
```
callpeak -t B_C.q255.20.bp.rand.EG.bedGraph -n test --outdir tesetfolder -f BED -q 0.01 -g 1241792540 -s 20 --min-length 20 --max-gap 40 --nomodel --extsize 20 --keep-dup all --buffer-size 100000000
```
> Compared coverage files
```
bigwigCompare -b1 M_H.q255.20.bp.rand.EG.bw -b2 M_C.q255.20.bp.rand.EG.bw --scaleFactors 1:1 -bs 20 -o Mo17_Diff_20bp.bedGraph -of bedgraph
```
> redefining peak regions
```
macs3 refinepeak -b B73-MAPQ255-diffpeaks.bed -i /scratch.global/liang795/MOAseqbam/ftp.mpipz.mpg.de/Nathan/BAM/merged/B_H1_3.merged.max80.255.bam -o B73-MAPQ255-diffpeaks-summits
```
> peak annotation
```
annotatePeaks.pl B73-MAPQ255-diffpeaks.bed ~/genomeinfo/genome-fasta/Zm-B73-REFERENCE-GRAMENE-4.0-noChr.fa -gtf ~/genomeinfo/geneannotation/Zea_mays.B73_RefGen_v4.41.primary.noChr.gtf > B73-MAPQ255-diffpeaks-ann.bed
```
