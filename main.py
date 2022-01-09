from typing import Literal

import numpy as np
import pandas as pd
from fastapi import FastAPI
from scipy.interpolate import interp1d

app = FastAPI()

ex2 = pd.read_parquet("ex_df.parquet")


def interp_bounds(df: pd.DataFrame):
    interpolated = interp1d(
        df["mid"].values,
        df["remaining"].values,
        kind="cubic",
        bounds_error=False,
        fill_value=np.nan,
    )

    def f(x):
        xmax = interpolated.x.max()
        value = interpolated(x).item()
        if value == value:
            return value
        if x < interpolated.x.min():
            return interpolated.y[0]
        elif x > xmax:
            pt = interpolated.y[-1]
            return pt * np.exp(-(x - xmax) / 11)

    return f


@app.get("/remaining/")
async def remaining(
    country: str,
    current: float,
    year: int = 2019,
    sex: Literal["Male", "Female"] = "Female",
):
    subset = ex2.loc[(country, year, sex), :]
    f = interp_bounds(subset)
    rem = f(current)
    return {"remaining": rem}
