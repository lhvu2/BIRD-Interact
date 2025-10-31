import os
import json
import numpy as np
import pandas as pd
from os.path import join

def stratify_select(df, N: int=50):
    # compute counts per class
    counts = df['selected_database'].value_counts()

    # proportional allocation
    proportions = counts / counts.sum()
    samples_per_class = (proportions * N).round().astype(int)

    # adjust for rounding issues (make sure total = N)
    diff = N - samples_per_class.sum()
    if diff != 0:
        # adjust by adding/subtracting from the largest/smallest groups
        adjust_indices = samples_per_class.sort_values(ascending=(diff < 0)).index[:abs(diff)]
        samples_per_class.loc[adjust_indices] += np.sign(diff)

    # sample rows
    df_sample = (
        df.groupby('selected_database', group_keys=False)
        .apply(lambda x: x.sample(samples_per_class[x.name], random_state=42))
    )

    #print(df_sample.shape)
    #df_sample.head()
    return df_sample


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.realpath(__file__))
    print(script_directory)

    mode = "bird-interact-full"
    N = 50
    infile_path = join(script_directory, f"data/{mode}/bird_interact_data-orig.jsonl")
    outfile_path = join(script_directory, f"data/{mode}/bird_interact_data_{N}.jsonl")
    rows = []
    with open(infile_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # skip empty lines
                rows.append(json.loads(line))

    df = pd.DataFrame(rows)
    print(df.head())

    df_sample = stratify_select(df=df, N=N)
    df_sample.to_json(outfile_path, orient="records", lines=True)
    pass