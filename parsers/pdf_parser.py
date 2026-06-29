import pdfplumber
from typing import List, Dict, Any


class PDFParser:
    """
    Extracts raw transaction-like rows from PDF bank statements.
    Uses pdfplumber to detect tables; falls back to text-line parsing
    when no clean table structure is found.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_tables(self) -> List[List[str]]:
        """Attempts table extraction page by page."""
        rows = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row and any(cell for cell in row):
                            rows.append(row)
        return rows

    def extract_text_lines(self) -> List[str]:
        """Fallback: extract raw text lines when no table is detected."""
        lines = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                lines.extend(text.split("\n"))
        return lines

    def parse(self) -> List[Dict[str, Any]]:
        """
        Main entry point. Returns a list of raw row dicts that the
        statement_cleaner will later standardize.
        """
        table_rows = self.extract_tables()

        if table_rows:
            return [{"raw_row": row, "source": "table"} for row in table_rows]

        # Fallback to plain text lines if no tables were detected
        text_lines = self.extract_text_lines()
        return [{"raw_row": line, "source": "text"} for line in text_lines if line.strip()]