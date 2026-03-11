import io
import pandas as pd
from fastapi import UploadFile, HTTPException


ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
MAX_ROWS_FOR_LLM = 30


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
            for encoding in ("utf-8", "latin1", "cp1252"):
                try:
                    df = pd.read_csv(io.BytesIO(contents), encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("Could not decode CSV with any supported encoding")
        else:
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {exc}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file contains no data.")

    return df


def dataframe_to_summary_text(df: pd.DataFrame) -> str:
    """Convert a DataFrame to a compact text representation for the LLM."""
    sample = df.head(MAX_ROWS_FOR_LLM)

    # Build compact numeric summaries
    numeric_cols = df.select_dtypes(include="number")
    agg_lines = []
    for col in numeric_cols.columns:
        agg_lines.append(
            f"  {col}: sum={df[col].sum():.0f}, mean={df[col].mean():.1f}, "
            f"min={df[col].min()}, max={df[col].max()}"
        )

    summary_parts = [
        f"Dataset: {len(df)} rows, {len(df.columns)} columns.",
        f"Columns: {', '.join(df.columns.tolist())}",
        "",
        "--- Aggregated Metrics ---",
        "\n".join(agg_lines) if agg_lines else "(no numeric columns)",
        "",
        f"--- Sample Rows (first {len(sample)}) ---",
        sample.to_csv(index=False),
    ]
    return "\n".join(summary_parts)
