import pandas as pd


def dataframeDateAssign(df: pd.DataFrame, dateCol="pdate"):
    df[dateCol] = pd.to_datetime(df[dateCol])
    dates = pd.date_range(start=df[dateCol].min(), end=df[dateCol].max())
    df = df.set_index(dateCol).reindex(dates, fill_value=0).reset_index()
    df[dateCol] = [str(i)[:10] for i in df["index"]]
    df = df.drop(columns=["index"])
    return df
