import pandas as pd

def read_excel(filename: str):
    return pd.read_excel(filename).to_dict()

def write_excel(filename: str, data: dict):
    df = pd.DataFrame.from_dict(data)
    df.to_excel(filename, index=False)