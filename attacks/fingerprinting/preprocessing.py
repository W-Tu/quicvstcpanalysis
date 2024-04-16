import pandas as pd
import torch
import numpy as np

def unique_packet_size(df):
    one_hot = pd.get_dummies(df["Length"]).reindex(columns=range(54, 1513))
    one_hot[1513] = (one_hot.sum(axis=1) - 1) ** 2
    small = one_hot.loc[:,54:149].max(axis=1).rename("SMALL")
    medium = one_hot.loc[:,150:999].max(axis=1).rename("MEDIUM")
    large = one_hot.loc[:,1000:].max(axis=1).rename("LARGE")
    return pd.concat([small, medium, large], axis=1)

def inter_arrival_time(df):
    return df["Time delta"]

def outbound(df: pd.DataFrame) -> pd.DataFrame: 
    return ((pd.DataFrame({"OUTBOUND" : pd.get_dummies(df["Source"])["10.247.230.86"]}, dtype=float) * 2) - 1)

def burst_len(df):
    y = pd.get_dummies(df["Source"])["10.247.230.86"]
    return pd.DataFrame({"BURSTLEN" : y.groupby((y != y.shift()).cumsum()).cumcount() + 1})

def protocol(df):
    return pd.get_dummies(df["Protocol"]).reindex(columns=["DNS", "HTTP", "QUIC", "SSDP", "TCP", "TLSv1.2", "TLSv1.3", "UDP"])

def clean_df(file, c, group=100):
    df = pd.read_csv(file)
    p = protocol(df)
    iat = inter_arrival_time(df)
    ciat = iat.groupby(np.arange(len(df.index)) // group, axis=0).cumsum()
    o = outbound(df)
    ups = unique_packet_size(df)
    uups = ups.groupby(np.arange(len(df.index)) // group, axis=0).max()
    cups = ups.groupby(np.arange(len(df.index)) // group, axis=0).cumsum()
    dups = (ups.mul(o["OUTBOUND"], axis=0)).groupby(np.arange(len(df.index)) // group, axis=0).cumsum()
    bl = burst_len(df)
    medbl = bl.groupby(np.arange(len(df.index)) // group, axis=0).mean()
    maxbl = bl.groupby(np.arange(len(df.index)) // group, axis=0).max()
    pos = pd.get_dummies(df.groupby(np.arange(len(df.index)) // group, axis=0).cumcount() + 1)

    df = p.rename({"Protocol": "PROTOCOL"})
    df["TIME"] = iat
    df["CUMULATIVETIME"] = ciat
    df["OUTBOUND"] = o
    df[[f"UNIQUE{r}" for r in ["SMALL", "MEDIUM", "LARGE"]]] = uups
    df[[f"CUMULATIVE{r}" for r in ["SMALL", "MEDIUM", "LARGE"]]] = cups
    df[[f"DIRECTIONALCUMULATIVE{r}" for r in ["SMALL", "MEDIUM", "LARGE"]]] = dups
    df["BURSTLEN"] = bl
    df["MEDIANBURSTLEN"] = medbl
    df["MAXBURSTLEN"] = maxbl
    df = pd.concat([pos, df], axis=1)

    df.fillna(0, inplace=True)
    
    df[["SLIDES", "DOCS", "SHEETS"]] = 0

    df[["SLIDES", "DOCS", "SHEETS"][c]] = 1

    return df

def group_df(df, group=100):
    return np.resize(df.to_numpy(), (df.size // (group * df.shape[1]), group, df.shape[1]))

def grouped_tensors_from_file(file, c, group=100):
    return torch.Tensor(group_df(clean_df(file, c, group), group))

def grouped_nparray_from_file(file, c, group=100):
    return group_df(clean_df(file, c, group), group)

grouped_tensors_from_file("Data/GOOGLE DOCS QUIC.csv", 1, 20)