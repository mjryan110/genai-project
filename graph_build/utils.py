
import re

def normalize_column_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[^\w]", "_", name)  # Replace all non-word characters with underscores
    name = re.sub(r"__+", "_", name)    # Collapse multiple underscores
    return name