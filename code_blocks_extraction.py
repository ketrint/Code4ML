# -*- coding: utf-8 -*-
"""code_blocks_extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qpRzYU7M9h_r4-OmFfxkHj0pDo1bdfFx
"""

import pandas as pd
import subprocess
import json
import os

LISTS_FOLDER = "./kernel_lists"
MERGED_LIST = "kernels.csv"
CODEBLOCKS_TABLE = "code_blocks.csv"

kernels = pd.read_csv(MERGED_LIST)
code_blocks = pd.DataFrame(columns = ["kernel_id", "code_block", "code_block_id"])


for kernel_link in kernels.ref:
  kernel_name = kernel_link.split('/')[1]
  kernel_directory = LISTS_FOLDER + '/' + kernel_name + '/'
  #loading the kernel and corresponding meta
  subprocess.run(
        args=["kaggle", "kernels", "pull", kernel_link, '-p', kernel_directory, '-m']
    )
  #extract the kernel path
  kernel_path = kernel_directory + kernel_name + ".ipynb"
  metadata_path = kernel_directory + "kernel-metadata.json"
  try:
    #loading the kernel
    with open(kernel_path, mode= "r", encoding= "utf-8") as f:
      kernel = json.loads(f.read())
    #loading the metadata
    with open(metadata_path, mode= "r", encoding= "utf-8") as f:
      metadata = json.loads(f.read())
    #extracting the blocks and meta
    blocks = []
    blocks_id = []
    for i in range(len(kernel['cells'])-1):
      cell = kernel['cells'][i]
      if cell["cell_type"] == "code" and cell['source'] is not None:
        blocks_id.append(i)
        blocks.append(cell['source'])
    kernel_id = [metadata['id_no']]*len(blocks)
    kernel_code_blocks = pd.DataFrame({"kernel_id": kernel_id, 
                                      "code_block": blocks, "code_block_id": blocks_id})
    #collecting code_blocks from all kernels
    code_blocks = code_blocks.append(kernel_code_blocks)
  except FileNotFoundError:
    print("The kernel was not loaded.")

code_blocks.reset_index(drop=True, inplace = True)
code_blocks.to_csv(CODEBLOCKS_TABLE)

# delete files from LISTS_FOLDER
os.rmdir(LISTS_FOLDER)
