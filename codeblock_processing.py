import copy
from csv import writer
from io import StringIO
import json

import pandas as pd



METADATA_FIELDS = {
    "kaggle_score": "kernel__bestPublicScore",
    "kaggle_comments": "menuLinks__-1__count",
    "kaggle_upvotes": "kernel__upvoteCount",
    "kaggle_link": "baseUrl",
    "kaggle_id": "kernel__id",
    "kaggle_dataset":"dataSources__mountSlug"
}

CODE_BLOCK_COLUMN = "code_blocks"
CODE_BLOCK_ID_COLUMN = "code_block_id"
DATA_SOURCE_COLUMN = "data_source"
ALL_COLUMNS = (
    list(METADATA_FIELDS.keys()) +
    [DATA_SOURCE_COLUMN, CODE_BLOCK_COLUMN, CODE_BLOCK_ID_COLUMN]
)


def is_kernel_view(tag):
    return (tag.name == "script" and tag.has_attr("class") and
            tag["class"][0] == "kaggle-component")


def collect_metadata(kernel_json):
    """
    Collects data for fields in METADATA_FIELDS
    """
    def nested_lookup(json_obj, complex_key):
        keys = complex_key.split("__")
        current_level = json_obj
        for key in keys:
            if isinstance(current_level, list):
                try: 
                    next_level = current_level[int(key)]
                except ValueError:
                    next_level = current_level[0].get(key) 
            else:
                next_level = current_level.get(key)

            if next_level is None:
                return None
            current_level = next_level

        return current_level

    result = []
    for field_name, field_json_key in METADATA_FIELDS.items():
        result.append(nested_lookup(kernel_json, field_json_key))
    return result



def code_blocks_from_json(kernel_source):
    """
    Code block generator
    """
    ipynb_source = json.loads(kernel_source)

    for cell in ipynb_source["cells"]:
        if cell["cell_type"] == "code" and cell["source"] is not None and len(cell["source"].strip()) > 0:
            yield cell["source"]



def process_kernel(response):
    """
    Parses notebook codeblocks and metadata
    Input:  loaded kernel
    Output: code blocks
    """
    soup = BeautifulSoup(response.text, "html.parser")
    potential_notebook_views = soup.find_all(is_kernel_view)

    kernel_view = potential_notebook_views[1]
    kernel_raw = kernel_view.string

    data_begin_marker = "Kaggle.State.push("
    data_end_marker = ");performance"

    data_begin = kernel_raw.index(data_begin_marker) + len(data_begin_marker)
    data_end = kernel_raw.index(data_end_marker)

    kernel_json = json.loads(kernel_raw[data_begin: data_end])

    metadata = collect_metadata(kernel_json)

    new_blocks = 0
    if kernel_json.get("kernelBlob") is None:
        for idx, block in enumerate(code_blocks_from_iframe(kernel_json)):
            code_block_data = copy.copy(metadata)
            code_block_data.append(block)
            code_block_data.append(idx)
            buffer_writer.writerow(code_block_data)
            new_blocks += 1

    elif kernel_json["kernelBlob"].get("source") is None:
        return 0

    else:
        for idx, block in enumerate(code_blocks_from_json(kernel_json["kernelBlob"]["source"])):
            code_block_data = copy.copy(metadata)
            code_block_data.append(block)
            code_block_data.append(idx)
            buffer_writer.writerow(code_block_data)
            new_blocks += 1

    return new_blocks




