library(diffloop)

bed_dir = "diffloop"
samples = c("B73_H3K27ac_1","B73_H3K27ac_2","Mo17_H3K27ac_1","Mo17_H3K27ac_2")
full = loopsMake(bed_dir, samples)
celltypes = c("B73", "Mo17")
full = updateLDGroups(full, celltypes)
full1 = subsetLoops(full, full@rowData$loopWidth >= 0)
loopMetrics(full1)
km_filt = full1[,c(1,2,3,4)]
km_res = quickAssoc(km_filt)
fit = summary(km_res)
