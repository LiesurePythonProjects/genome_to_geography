# Author: Rajesh M
# Date: 24-08-2022

# !/usr/bin/python

import argparse

from vcf_to_matrix import read_input_files


def main():
    parser = argparse.ArgumentParser(description="Shows the relation between human genome and their geography")

    parser.add_argument("--vcf-file", '-v', help="Input VCF file.", dest="vcf_file", required=True)
    parser.add_argument("--panel-file", '-p', help="Input panel file.", dest="panel_file", required=True)
    parser.add_argument("--output", '-o', help="Output matrix csv file", dest="matrix_file", required=True)

    args = parser.parse_args()

    read_input_files(args)


if __name__ == "__main__":
    main()
