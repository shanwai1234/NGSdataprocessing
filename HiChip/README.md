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
