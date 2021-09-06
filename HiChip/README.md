# DE loop analysis for data generated from different reference genotypes
> https://rpubs.com/bman/79395
> https://www.r-bloggers.com/2020/09/generalized-linear-models-and-plots-with-edger-advanced-differential-expression-analysis/

# FitHiChip diffloop command
```
Rscript ~/software/FitHiChIP/Imp_Scripts/DiffAnalysisHiChIP.r --AllLoopList B73H3K27ac_repl1_H3K27acPtoARaw.bed,B73H3K27ac_repl2_H3K27acPtoARaw.bed,Mo17H3K27ac_repl1_H3K27acPtoARaw.bed,Mo17H3K27ac_repl2_H3K27acPtoARaw.bed --ChrSizeFile ~/genomeinfo/chromosome-sizes/B73v4-chromosome.sizes --FDRThr 0.01 --CovThr 25 --ChIPAlignFileList B73H3K27ac_ChIPAlign.bam,Mo17H3K27ac_ChIPAlign.bam --OutDir ./ --CategoryList B73H3K27ac,Mo17H3K27ac --ReplicaCount 2,2 --ReplicaLabels1 R1,R2 --ReplicaLabels2 R1,R2 --FoldChangeThr 2 --DiffFDRThr 0.05 --bcv 0.4
```
# digest a genome
```
python ~/software/HiC-Pro/bin/utils/digest_genome.py -r dpnii -o Simulate_Mo17_dpnii.bed Zm-B73-REFERENCE-GRAMENE-4.0-LaiMo17SNP.fa
```

# dominant and additive genes
>https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004745#pgen.1004745.s006
>https://link.springer.com/article/10.1007/s00122-019-03489-9#Sec2
>https://link.springer.com/article/10.1186/s12864-016-3296-8#Sec18
>https://www.nature.com/articles/s41598-021-92938-x#Sec7
> key important paper https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6356826/
> https://genome.cshlp.org/content/22/12/2445.full#sec-1 similar approach as I used

# cis and trans gene regulation
>https://www.frontiersin.org/articles/10.3389/fpls.2020.00410/full
>https://www.nature.com/articles/s41467-019-13386-w#Sec12
> detailed explaination: https://genome.cshlp.org/content/20/6/816.full

# metaplot drawing in python
```
computeMatrix reference-point --referencePoint TSS -b 2000 -a 2000 -R ../Zea_mays.B73_RefGen_v4.41.Chr.simplify.generegion -S B73-H3K27ac-rmdups.bw --skipZeros -o B73-H3K27ac-rmdups.gz -p 6 --outFileSortedRegions B73-H3K27ac-rmdups.bed

plotProfile -m B73-H3K27ac-rmdups.gz -out test.svg --perGroup --colors green --plotTitle "" --samplesLabel "test" --refPointLabel "TSS" -T "Test" -z ""
```

# Plotting interaction matrix
> https://nservant.github.io/HiC-Pro/UTILS.html
```
hicConvertFormat -m merged_5000.matrix --bedFileHicpro merged_5000_abs.bed --inputFormat hicpro --outputFormat cool -o matrix.cool

hicConvertFormat -m matrix.cool --inputFormat cool --outputFormat h5 -o matrix.h5

hicCorrectMatrix diagnostic_plot -m B73-to-B73-H3K4me3-HiCPro.h5 -o mytest.png

hicPlotMatrix -m B73-to-B73-H3K4me3-HiCPro.h5 --region Chr6:22483501-25398000 -o B73-to-B73-H3K4me3-PAV.svg --vMax 30 --colorMap "RdYlBu"

hicNormalize -m B73-to-B73-H3K4me3-HiCPro.h5 Mo17-to-SimuMo17-H3K4me3-HiPro.h5 --normalize smallest -o B73-to-B73-H3K4me3-HiCPro-normtoSimuMo17.h5 Mo17-to-SimuMo17-H3K4me3-HiPro-normtoB73.h5
```
# 4C-seq running

> generating the fragment end libraries of the reference genome using the code ```4Cker.sh```
> building index using bowtie2
> producing results using ```pipe4C```

collapsing overlapping regions for visualization
```
bedtools merge -i B4C11_aligned_rm_self_und.normalize.sort.bedGraph -c 4 -o max
```

# 4C-ker details

```
> library(R.4Cker)
> enz_file=read.table("~/genomeinfo/4Cker-index/reduced_genome/R.4Cker/B73v4_dpnii_flanking_sites_125_unique_2.bed", stringsAsFactors = FALSE)
> my_obj = createR4CkerObjectFromFiles(files="./B4C13_aligned.bedGraph",bait_chr="Chr7",bait_coord=176070000,bait_name="exp4-1",primary="GATC",samples="exp4-1",conditions="control",replicates=1,species="maize",output_dir="example4",enz_file=enz_file)
```
