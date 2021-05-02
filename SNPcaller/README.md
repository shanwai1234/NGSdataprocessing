## calling snp using GATK in RNA-seq data
https://gatk.broadinstitute.org/hc/en-us/articles/360035531192-RNAseq-short-variant-discovery-SNPs-Indels
### reference genome needs to use gatk ```gatk CreateSequenceDictionary``` function to create a dictionary
### ```gatk BaseRecalibrator``` have several places need to change
> 1. vcf requires to have more headers, such as
```
##fileformat=VCFv4.2
###filedate=20210412
###source="beagle.05Apr21.9b7.jar"
###INFO=<ID=AF,Number=A,Type=Float,Description="Estimated ALT Allele Frequencies">
###INFO=<ID=DR2,Number=A,Type=Float,Description="Dosage R-Squared: estimated squared correlation between estimated REF dose [P(RA) + 2*P(RR)] and true REF dose">
###INFO=<ID=IMP,Number=0,Type=Flag,Description="Imputed marker">
###FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
###FORMAT=<ID=DS,Number=A,Type=Float,Description="estimated ALT dose [P(RA) + 2*P(AA)]">
```
> 2. Indexing the vcf file using ```gatk IndexFeatureFile -I yourname.vcf```
> 3. ```*splitnc.bam``` generated from ```gatk SplitNCigarReads``` needs to be grouped uniquely, an additional command needs to perform grouping for splitnc.bam file. Using ``` picard AddOrReplaceReadGroups I=H18.splitnc.bam O=test.bam RGID=1 RGLB=lib2 RGPL=illumina RGPU=unit1 RGSM=3```
## calling snp using GATK in DNA
https://gencore.bio.nyu.edu/variant-calling-pipeline/
