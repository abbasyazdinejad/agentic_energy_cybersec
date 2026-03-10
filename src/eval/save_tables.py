from pathlib import Path
import pandas as pd


def save_dataframe_table(df: pd.DataFrame, filename: str):
    out_dir = Path("outputs/tables")
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / f"{filename}.csv"
    tex_path = out_dir / f"{filename}.tex"

    df.to_csv(csv_path, index=False)

    latex_str = df.to_latex(index=False, float_format="%.3f")
    tex_path.write_text(latex_str, encoding="utf-8")

    print(f" Saved table: {csv_path}")
    print(f" Saved LaTeX table: {tex_path}")