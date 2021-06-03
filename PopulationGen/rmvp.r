MVP.Data(fileNum="Selected-102genos-Widiv-filtered-MAF01-Het01-prune.geno",          
         filePhe="Selected-102genos-Widiv-filtered-MAF01-Het01-prune.pheno",
          fileMap="Selected-102genos-Widiv-filtered-MAF01-Het01-prune.snp",
          sep.num="\t",
          sep.map="\t", 
          sep.phe="\t",
          fileKin=FALSE,
          filePC=FALSE,
          #priority="memory",
          #maxLine=10000,
          out="mvp.num"
          )

genotype <- attach.big.matrix("mvp.num.geno.desc")
phenotype <- read.table("mvp.num.phe",head=TRUE)
map <- read.table("mvp.num.geno.map" , head = TRUE)
Kinship <- attach.big.matrix("mvp.kin.desc")
Covariates <- bigmemory::as.matrix(attach.big.matrix("mvp.pc.desc"))

MVP.Data.Kin("Selected-102genos-Widiv-filtered-MAF01-Het01-prune.cXX.txt", out="mvp", priority='memory', sep='\t')
MVP.Data.PC("Selected-102genos-Widiv-filtered-MAF01-Het01-prune-5PC.cov", out='mvp', sep='\t')

for(i in 2:ncol(phenotype)){
  imMVP <- MVP(
    phe=phenotype[, c(1, i)],
    geno=genotype,
    map=map,
    K=Kinship,
    CV.GLM=Covariates,
    CV.MLM=Covariates,
    CV.FarmCPU=Covariates,
    nPC.GLM=5,
    nPC.MLM=5,
    nPC.FarmCPU=5,
    priority="speed",
    #ncpus=10,
    vc.method="BRENT",
    maxLoop=10,
    method.bin="static",
    #permutation.threshold=TRUE,
    #permutation.rep=100,
    threshold=0.05,
    method=c("GLM", "MLM", "FarmCPU")
  )
  gc()
}
