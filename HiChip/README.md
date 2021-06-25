# DE loop analysis for data generated from different reference genotypes
> https://rpubs.com/bman/79395
> https://www.r-bloggers.com/2020/09/generalized-linear-models-and-plots-with-edger-advanced-differential-expression-analysis/

# FitHiChip diffloop command
```
Rscript ~/software/FitHiChIP/Imp_Scripts/DiffAnalysisHiChIP.r --AllLoopList B73H3K27ac_repl1_H3K27acPtoARaw.bed,B73H3K27ac_repl2_H3K27acPtoARaw.bed,Mo17H3K27ac_repl1_H3K27acPtoARaw.bed,Mo17H3K27ac_repl2_H3K27acPtoARaw.bed --ChrSizeFile ~/genomeinfo/chromosome-sizes/B73v4-chromosome.sizes --FDRThr 0.01 --CovThr 25 --ChIPAlignFileList B73H3K27ac_ChIPAlign.bam,Mo17H3K27ac_ChIPAlign.bam --OutDir ./ --CategoryList B73H3K27ac,Mo17H3K27ac --ReplicaCount 2,2 --ReplicaLabels1 R1,R2 --ReplicaLabels2 R1,R2 --FoldChangeThr 2 --DiffFDRThr 0.05 --bcv 0.4
```