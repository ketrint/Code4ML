# Code4ML

## Kernels collection and parsing running

### Kaggle kernels links collection

1. Collection of kernels links to kernel_lists directory.

`mkdir kernel_lists`

`python collect_kernels_from_competitions.py`

The script does the following:
- Collects the links to the Kaggle competitions to ‘competitions_ref.csv’
- Runs competition_kernels.sh, which collect kernels of every competition
- Collects .csv files with the  Kaggle kernels links to kernel_lists directory 

2. Combining table data into one .csv table

`python unite_kernel_lists_w_year.py`  


3. Combining table data into one .csv table

`python unite_kernel_lists.py`

Input: kernel_lists directory
Output: .csv table with link to the kernel and submission year



### Kaggle kernels parsing
In order to download code files and metadata associated with a Notebook, one can use the following command:

`kaggle kernels pull [KERNEL] -p /path/to/download -m`


