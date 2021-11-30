## tips for building UCSC genome browser

### adding interaction loops
For example:
```
bedToBigBed -as=interact.as -type=bed5+13 B73H3K4me3PtoP_Interactions_narrowed_organized_sort.bed ~/genomeinfo/chromosome-sizes/B73v4-chromosome.sizes B73H3K4me3PtoP_Interactions_narrowed.bb
```
### adding gene annotation
```
gff3ToGenePred -geneNameAttr=gene_name Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.gff3 stdout | sort -k2,2 -k4n,4n > Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.genePred
genePredToBed Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.genePred Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.bed
bedToBigBed Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.bed ~/genomeinfo/chromosome-sizes/B73v5-chromosome.sizes Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.bb
```
