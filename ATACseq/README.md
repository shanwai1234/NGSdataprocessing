# ATAC-processing
> interpreting code from: https://github.com/schmitzlab/Widespread-Long-range-Cis-Regulatory-Elements-in-the-Maize-Genome for producing high-confidence ACRs and redetermining summit per ACR.
# MOA-seq
The key step for using iSeg software
```
ln -vs /usr/lib/x86_64-linux-gnu/libboost_system.so /usr/lib/x86_64-linux-gnu/libboost_system.so.1.66.0
ln -vs /usr/lib/x86_64-linux-gnu/libboost_filesystem.so /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.66.0
```
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 37c4ca66dd3110a9cf403dc166693076c5c5aaf9
=======
>>>>>>> 37c4ca66dd3110a9cf403dc166693076c5c5aaf9
plot bigwig Data
```
ComputeMatrix scale-regions -S /scratch.global/liang795/MOAseq/rmdupsbam/merged/MB.B73.log2ratio.10bpbin.absolute.sorted.bigWig /scratch.global/liang795/MOAseq/rmdupsbam/merged/MB.Mo17.log2ratio.10bpbin.absolute.sorted.bigWig -R cis-reQTL-control-heat-select-candidate-finalreQTLs.200bpextend.bed merged-cis-response-eQTL.complement.reQTL.bed --beforeRegionStartLength 1000 --regionBodyLength 400 --afterRegionStartLength 1000 -o test.mat.gz
```
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 37c4ca66dd3110a9cf403dc166693076c5c5aaf9
=======
>>>>>>> 37c4ca66dd3110a9cf403dc166693076c5c5aaf9
=======
>>>>>>> 37c4ca66dd3110a9cf403dc166693076c5c5aaf9
