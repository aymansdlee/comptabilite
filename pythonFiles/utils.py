def clean_item_name(item_name):
    return item_name.replace("/ Black", "").replace("/ Silver", "").replace("/", "").strip()
