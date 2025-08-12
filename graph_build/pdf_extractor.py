from pathlib import Path
from typing import List, Dict, Optional
import fitz  # PyMuPDF
import os


import os
from pathlib import Path
import os
from pathlib import Path

class PDFTextExtractor:
    def __init__(self, secret_key: str = "UNSTRUCTURED_DATA_PATH"):
        pdf_dir = os.getenv(secret_key)
        print(f"[DEBUG] Loaded env var {secret_key} = {pdf_dir}")
        if not pdf_dir:
            raise ValueError(f"Secret `{secret_key}` not found or empty.")

        base_path = Path(__file__).resolve().parent.parent
        abs_path = (base_path / pdf_dir).resolve()

        print(f"[DEBUG] Resolved absolute path = {abs_path}")

        if not abs_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {abs_path}")

        self.pdf_paths = list(abs_path.glob("*.pdf"))
        print(f"[DEBUG] Found PDF files: {self.pdf_paths}")

    def extract_texts(self) -> Dict[str, str]:
        texts = {}
        for path in self.pdf_paths:
            doc = fitz.open(str(path))
            full_text = "\n".join(page.get_text() for page in doc)
            texts[path.name] = full_text
        return texts


