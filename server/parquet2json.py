import json

import pandas as pd
import pyarrow as pa
from pyarrow import fs

local = fs.LocalFileSystem()
df = pd.read_parquet("data/ex_df.parquet").query("period == 2019")
table = pa.Table.from_pandas(df)

with local.open_output_stream("../front/static/expectancy.arrow") as file:
    with pa.RecordBatchFileWriter(file, table.schema) as writer:
      writer.write_table(table)

# feather.write_feather(
#     df.reset_index(), "../front/static/expectancy.feather", compression="uncompressed"
# )
# dico = df.reset_index().to_json("../front/static/expectancy.json")

# with open("../front/static/expectancy.json", "r") as f:
#     dico2 = json.load(f)

# df2 = pd.DataFrame.from_records(dico2)
