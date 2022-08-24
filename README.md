[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6607065.svg)](https://doi.org/10.5281/zenodo.6607065)

# Code4ML code blocks extractions

##Prerequisites

In order to load data form Kaggle one should have a kaggle.json file with the username and key specified.

An example of collecting code snippets from Kaggle can be found [[here](https://github.com/ketrint/Code4ML/blob/main/code_blocks_collection_example.ipynb)].

##Overview

This is an official repository for code snippets from Kaggle kernels collecting. 

You can find the instructions above.

## Kaggle kernels links collection

1. Collection of kernels links to `kernel_lists` directory.

`mkdir kernel_lists`

`python collect_kernels_from_competitions.py`

The script does the following:
- Collects the links to the Kaggle competitions to ‘competitions_ref.csv’
- Runs competition_kernels.sh, which collect kernels information of every competition
- Collects .csv files with the Kaggle kernels links to `kernel_lists` directory 

2. Combining  kernels links tables into one .csv table

`python unite_kernel_lists.py`  

Input: 'kernel_lists' directory
Output: .csv table with the links to the Kaggle kernels

## Kaggle kernels parsing

`python code_blocks_extraction.py`

Input: .csv table with the links to the Kaggle kernels
Output: .csv table with the following columns: "kernel_id", "code_block", "code_block_id".

