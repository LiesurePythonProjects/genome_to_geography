# Author: Rajesh M
# Date: 24-08-2022

# !/usr/bin/python

import numpy as np
from pysam import VariantFile
import pandas as pd

from utils import start_progress, progress, end_progress


def read_input_files(args) -> None:
    sample, genotypes, variant_ids = [], [], []
    counter = 0
    with VariantFile(args.vcf_file) as vcf_reader:
        start_progress("\n% of vcf file read ")
        for record in vcf_reader:
            # if we consider all samples, it's resource expensive. so pick 1 record but for every 100 to avoid bias
            if counter % 100 == 0:
                if len(sample) == 0:  # as samples are same, avoid rewriting them in every iteration
                    samples = [sample for sample in record.samples]
                alleles = [record.samples[sample].allele_indices for sample in record.samples]
                genotypes.append(alleles)
                variant_ids.append(record.id)
            if counter % 4943 == 0:
                percent = round(100 * counter / 494328)
                progress(percent)
            counter += 1
        end_progress()

    genotypes = np.array(genotypes)
    genotypes = np.count_nonzero(genotypes, axis=2)
    genotypes = genotypes.T  # transpose the matrix to use samples instead of snips

    with open(args.panel_file) as panel_file:
        labels = {}  # {sample id: population code}
        for line in panel_file:
            line = line.strip().split('\t')
            labels[line[0]] = line[1]

    matrix = pd.DataFrame(genotypes, columns=variant_ids, index=samples)  # save a copy to use in collab for plot
    matrix['Population code'] = matrix.index.map(labels)
    matrix.to_csv("./data/matrix.csv")
