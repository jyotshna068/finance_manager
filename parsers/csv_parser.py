import pandas as pd
from typing import List, Dict, Any


class CSVParser:
    """
    Parses CSV and Excel transaction exports into a uniform list of dicts.
    Handles both .csv and .xlsx/.xls since formats are structurally similar.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_dataframe(self) -> pd.DataFrame:
        if self.file_path.lower().endswith(".csv"):
            return pd.read_csv(self.file_path)
        elif self.file_path.lower().endswith((".xlsx", ".xls")):
            return pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {self.file_path}")

    def parse(self) -> List[Dict[str, Any]]:
        """
        Loads the file and returns raw rows as dicts.
        Column names are kept as-is here; standardization happens
        downstream in statement_cleaner.py.
        """
        df = self._load_dataframe()

        # Drop fully empty rows/columns to reduce noise early
        df = df.dropna(how="all").dropna(axis=1, how="all")

        return df.to_dict(orient="records")