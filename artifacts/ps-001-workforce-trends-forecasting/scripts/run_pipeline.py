"""Build PS-001 interim and processed workforce outputs from landed raw CSV files."""

from __future__ import annotations

import sys
from pathlib import Path

import polars as pl
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
PS_SRC = PROJECT_ROOT / "artifacts" / "ps-001-workforce-trends-forecasting" / "src"
if str(PS_SRC) not in sys.path:
    sys.path.insert(0, str(PS_SRC))

from workforce_trends_utils import combine_workforce_frames, write_outputs  # noqa: E402


def load_raw_workforce_frames(raw_root: Path) -> dict[str, pl.DataFrame]:
    """Load each landed workforce CSV into a dictionary keyed by profession."""
    frames: dict[str, pl.DataFrame] = {}
    for csv_path in sorted(raw_root.glob("*.csv")):
        if csv_path.name == "combined_workforce.csv":
            continue
        frames[csv_path.stem] = pl.read_csv(csv_path)
    return frames


def main() -> None:
    raw_root = PROJECT_ROOT / "shared" / "data" / "1_raw" / "workforce"
    output_root = PROJECT_ROOT / "artifacts" / "ps-001-workforce-trends-forecasting"

    if not raw_root.exists():
        raise FileNotFoundError(f"Raw workforce directory not found: {raw_root}")

    frames = load_raw_workforce_frames(raw_root)
    if not frames:
        raise FileNotFoundError(
            "No workforce CSV files found under shared/data/1_raw/workforce"
        )

    combined = combine_workforce_frames(frames)
    write_outputs(combined, output_root)
    logger.info(f"PS-001 pipeline completed with {combined.height} rows")


if __name__ == "__main__":
    main()
