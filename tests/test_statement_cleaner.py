from datetime import datetime
from parsers.statement_cleaner import StatementCleaner


def test_cleans_valid_csv_row():
    raw_rows = [{"Date": "15-06-2026", "Description": "AMZN MKTPLACE", "Amount": "-1200.50"}]
    cleaned = StatementCleaner(raw_rows).clean()

    assert len(cleaned) == 1
    assert cleaned[0]["amount"] == -1200.50
    assert cleaned[0]["transaction_type"] == "debit"
    assert isinstance(cleaned[0]["date"], datetime)


def test_discards_row_without_date():
    raw_rows = [{"Description": "Unknown txn", "Amount": "500"}]
    cleaned = StatementCleaner(raw_rows).clean()
    assert cleaned == []


def test_discards_row_without_amount():
    raw_rows = [{"Date": "01-01-2026", "Description": "Unknown txn"}]
    cleaned = StatementCleaner(raw_rows).clean()
    assert cleaned == []


def test_handles_credit_transaction():
    raw_rows = [{"Date": "01-01-2026", "Description": "Salary Credit", "Amount": "50000"}]
    cleaned = StatementCleaner(raw_rows).clean()
    assert cleaned[0]["transaction_type"] == "credit"


def test_parses_text_line_from_pdf():
    raw_rows = [{"raw_row": "01-01-2026 STARBUCKS COFFEE 450.00", "source": "text"}]
    cleaned = StatementCleaner(raw_rows).clean()
    assert len(cleaned) == 1
    assert cleaned[0]["amount"] == 450.00