import re
from datetime import datetime
from typing import List, Dict, Any, Optional


class StatementCleaner:
    """
    Normalizes raw rows from PDFParser/CSVParser into a consistent schema:
    { date, description, amount, transaction_type, raw_text }

    This is intentionally heuristic-driven since bank statement formats
    vary widely across institutions.
    """

    DATE_PATTERNS = [
        "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d %b %Y", "%b %d, %Y",
        "%d-%m-%y", "%m/%d/%Y",
    ]

    AMOUNT_PATTERN = re.compile(r"[-+]?\d[\d,]*\.?\d{0,2}")

    COLUMN_ALIASES = {
        "date": ["date", "txn date", "transaction date", "value date"],
        "description": ["description", "narration", "particulars", "details", "remarks"],
        "amount": ["amount", "debit", "credit", "withdrawal", "deposit", "txn amount"],
    }

    def __init__(self, raw_rows: List[Any]):
        self.raw_rows = raw_rows

    def _match_column(self, row: Dict[str, Any], field: str) -> Optional[str]:
        for key in row.keys():
            normalized_key = str(key).strip().lower()
            if normalized_key in self.COLUMN_ALIASES[field]:
                return key
        return None

    def _parse_date(self, value: Any) -> Optional[datetime]:
        if value is None:
            return None
        value = str(value).strip()
        for fmt in self.DATE_PATTERNS:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None

    def _parse_amount(self, value: Any) -> Optional[float]:
        if value is None:
            return None
        match = self.AMOUNT_PATTERN.search(str(value).replace(",", ""))
        if match:
            try:
                return float(match.group())
            except ValueError:
                return None
        return None

    def _clean_dict_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        date_col = self._match_column(row, "date")
        desc_col = self._match_column(row, "description")
        amount_col = self._match_column(row, "amount")

        if not date_col and not amount_col:
            keys = list(row.keys())
            if len(keys) >= 3:
                date_col, desc_col, amount_col = keys[0], keys[1], keys[2]

        date = self._parse_date(row.get(date_col)) if date_col else None
        amount = self._parse_amount(row.get(amount_col)) if amount_col else None
        description = str(row.get(desc_col, "")).strip() if desc_col else ""

        if not date or amount is None:
            return None

        return {
            "date": date,
            "description": description,
            "amount": amount,
            "transaction_type": "debit" if amount < 0 else "credit",
            "raw_text": str(row),
        }

    def _clean_text_row(self, line: str) -> Optional[Dict[str, Any]]:
        amount_match = self.AMOUNT_PATTERN.findall(line.replace(",", ""))
        if not amount_match:
            return None

        amount = self._parse_amount(amount_match[-1])
        date = None
        for fmt in self.DATE_PATTERNS:
            date_match = re.search(r"\d{1,2}[-/ ]\w+[-/ ]\d{2,4}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}", line)
            if date_match:
                date = self._parse_date(date_match.group())
                if date:
                    break

        if not date or amount is None:
            return None

        return {
            "date": date,
            "description": line.strip(),
            "amount": amount,
            "transaction_type": "debit" if amount < 0 else "credit",
            "raw_text": line,
        }

    def clean(self) -> List[Dict[str, Any]]:
        cleaned = []

        for row in self.raw_rows:
            if isinstance(row, dict) and "raw_row" in row:
                if row["source"] == "text":
                    result = self._clean_text_row(row["raw_row"])
                else:
                    table_row = {f"col_{i}": v for i, v in enumerate(row["raw_row"])}
                    result = self._clean_dict_row(table_row)
            elif isinstance(row, dict):
                result = self._clean_dict_row(row)
            else:
                result = None

            if result:
                cleaned.append(result)

        return cleaned