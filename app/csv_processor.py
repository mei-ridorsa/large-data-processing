import os

import pandas as pd

from config import base_dir


def process(filename, task_id):
    chunk = pd.read_csv(os.path.join('input', filename), chunksize=500)

    df = pd.concat(chunk)

    grouped = df.groupby(['Song', 'Date'])['Number of Plays'].sum()

    # I am using the task uuid as output filename for simplicity's sake. In reality, it would be better to save the
    # relation task_id->filename into Redis or similar
    grouped.to_csv(os.path.join(base_dir, 'output', task_id + '.csv'), sep=',', encoding='utf-8')

    return task_id
