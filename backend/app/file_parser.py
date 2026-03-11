import io
import pandas as pd
from fastapi import UploadFile, HTTPException


ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
MAX_ROWS_FOR_LLM = 500


def validate_file(file: UploadFile) -> None:
    filename = file.filename or ""
    ext = filename[filename.rfind("."):].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )


async def parse_file(file: UploadFile) -> pd.DataFrame:
    validate_file(file)
    contents = await file.read()
    filename = file.filename or ""
    ext = filename[filename.rfind("."):].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {exc}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file contains no data.")

    return df


def dataframe_to_summary_text(df: pd.DataFrame) -> str:
    """Convert a DataFrame to a concise text representation for the LLM."""
    truncated = df.head(MAX_ROWS_FOR_LLM)
    summary_parts = [
        f"Dataset contains {len(df)} rows and {len(df.columns)} columns.",
        f"Columns: {', '.join(df.columns.tolist())}",
        "",
        "--- Descriptive Statistics ---",
        df.describe(include="all").to_string(),
        "",
        "--- First rows (sample) ---",
        truncated.to_string(index=False),
    ]
    return "\n".join(summary_parts)
