import pandas as pd


def flatten_json(y, parent_key="", sep="."):
    """Recursively flattens a nested dictionary into a single dictionary with compound keys."""
    items = []
    if isinstance(y, dict):
        for k, v in y.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten_json(v, new_key, sep=sep).items())
    elif isinstance(y, list):
        # If it's a list of dicts, we keep it as a list and handle it later
        items.append((parent_key, y))
    else:
        items.append((parent_key, y))
    return dict(items)


def recursive_expand_rows(data, list_keys, sep="."):
    """
    Recursively expands nested lists in a JSON object into a flat list of rows.

    Parameters:
    - data: The JSON data to expand
    - list_keys: A list of paths to the lists to expand, in order of expansion
    - sep: The separator to use for compound keys

    Returns:
    - A list of flattened rows
    """
    if not list_keys:
        return [data]

    current_key = list_keys[0]
    remaining_keys = list_keys[1:]

    # First flatten to access the nested list by path
    flat_data = flatten_json(data, sep=sep)

    # Get the list to expand safely
    list_to_expand = flat_data.get(current_key, [])

    # Create a copy of flat_data without the current_key
    base_data = {k: v for k, v in flat_data.items() if k != current_key}

    # If the list is empty or not found, return the data as is
    if not list_to_expand or not isinstance(list_to_expand, list):
        return [flat_data]

    rows = []
    for item in list_to_expand:
        # Create a new row combining base data and item
        row_data = {**base_data}

        # Add the item properties to the row with prefixed keys
        item_dict = item if isinstance(item, dict) else {current_key: item}
        for k, v in flatten_json(item_dict, sep=sep).items():
            row_data[f"{current_key}{sep}{k}"] = v

        # Recursively expand any remaining lists
        expanded_rows = recursive_expand_rows(row_data, remaining_keys, sep)
        rows.extend(expanded_rows)

    return rows
