## tips for building UCSC genome browser

### adding interaction loops
For example:
```
bedToBigBed -as=interact.as -type=bed5+13 B73H3K4me3PtoP_Interactions_narrowed_organized_sort.bed ~/genomeinfo/chromosome-sizes/B73v4-chromosome.sizes B73H3K4me3PtoP_Interactions_narrowed.bb
```
