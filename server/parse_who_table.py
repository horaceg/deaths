import numpy as np
import pandas as pd


def make_ex() -> pd.DataFrame:
    df = pd.read_csv("who_life_tables.csv")
    ex = df.loc[lambda f: f["Indicator"].str.startswith("ex")]
    ex.columns = ex.columns.str.lower()
    ex2 = (
        ex.join(
            ex["dim2"]
            .str.replace(r"<", r"0-")
            .str.extract(r"(?P<lower>\d+)-?\s*(?P<upper>\d+|\+)", expand=True)
            .replace("+", np.inf)
            .astype(float)
        )
        .dropna(how="all", axis=1)
        .assign(remaining=lambda f: f["value"].astype(float))
        .rename({"dim1": "sex", "spatialdimvaluecode": "country_code"}, axis=1)
        .assign(
            mid=lambda f: f["lower"].add(f["upper"].replace(np.inf, 90)).div(2),
            total=lambda f: f["mid"].add(f["remaining"]),
        )
        .set_index(["location", "period", "sex", "lower", "upper"])
        .sort_index()[["country_code", "parentlocation", "mid", "total", "remaining"]]
    )
    return ex2


if __name__ == "__main__":
    ex2 = make_ex()
    ex2.to_parquet("data/ex_df.parquet")
