import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from config.auth import get_current_user
from config.settings import settings

from parsers.pdf_parser import PDFParser
from parsers.csv_parser import CSVParser
from parsers.statement_cleaner import StatementCleaner
from services.expense_service import save_transactions
from database.crud import get_user_accounts, create_account

router = APIRouter(prefix="/upload", tags=["Document Upload"])

ALLOWED_EXTENSIONS = {".pdf", ".csv", ".xlsx", ".xls"}


def _validate_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    return ext


@router.post("/statement")
def upload_statement(
    file: UploadFile = File(...),
    account_id: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Accepts a PDF/CSV/Excel statement, runs it through the parsing +
    cleaning pipeline, and persists structured transactions.
    """
    ext = _validate_file(file)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    saved_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Format detection -> appropriate parser
    if ext == ".pdf":
        raw_rows = PDFParser(saved_path).parse()
    else:
        raw_rows = CSVParser(saved_path).parse()

    cleaned_transactions = StatementCleaner(raw_rows).clean()

    if not cleaned_transactions:
        raise HTTPException(status_code=422, detail="Could not extract any valid transactions from this file.")

    # Resolve account — use provided account_id or default to user's first account
    if not account_id:
        accounts = get_user_accounts(db, current_user.id)
        if not accounts:
            account = create_account(db, current_user.id, "Default Account", "general")
            account_id = account.id
        else:
            account_id = accounts[0].id

    inserted_count = save_transactions(db, current_user.id, account_id, cleaned_transactions)

    return {
        "message": "Statement processed successfully.",
        "transactions_inserted": inserted_count,
        "file_name": file.filename,
    }