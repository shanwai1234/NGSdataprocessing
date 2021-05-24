### Synteny plot
https://ksamuk.github.io/syntR/articles/syntr_tutorial.html
### MDS (Multidimensional scaling) calculator

> plink --noweb --bfile allpops --genome --out allpopsIBD

> plink --noweb --bfile allpops --read-genome allpopsIBD.genome --cluster --mds-plot 2 --out allpopsmds

MDS vs. PCA. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2795880/

### Effective SNPs calculator
http://pmglab.top/gec/#/download

>java -Xmx4g -jar ~/software/gec/gec.jar --effect-number --filter-maf-le 0.1 --plink-binary <plink bed format file for snp> --genome --out test
