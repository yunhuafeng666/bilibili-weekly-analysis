# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
import re

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned.csv")


def load_all_periods():
    """读取所有期的json数据"""
    rows = []
    files = [f for f in os.listdir(RAW_DIR) if f.startswith("period_") and f.endswith(".json")]
    files.sort(key=lambda x: int(re.findall(r"\d+", x)[0]))

    for fname in files:
        period_num = int(re.findall(r"\d+", fname)[0])
        with open(os.path.join(RAW_DIR, fname), "r", encoding="utf-8") as f:
            raw = json.load(f)

        video_list = raw.get("data", {}).get("list", [])
        for v in video_list:
            def clean_text(text):
                if not isinstance(text, str): return ""
                return re.sub(r"\s+", " ", text.strip())

            stat = v.get("stat", {})
            rows.append({
                "period": period_num,
                "title": clean_text(v.get("title")),
                "up_name": clean_text(v.get("owner", {}).get("name")),
                "zone": clean_text(v.get("tname")),
                "view": stat.get("view", 0),
                "danmaku": stat.get("danmaku", 0),
                "reply": stat.get("reply", 0),
                "like": stat.get("like", 0),
                "coin": stat.get("coin", 0),
                "favorite": stat.get("favorite", 0),
                "share": stat.get("share", 0),
                "desc": clean_text(v.get("desc")),
            })
    print("数据加载完成")
    return pd.DataFrame(rows)


def clean(df):
    """数据清洗和打标签"""
    df = df.dropna(subset=["title", "up_name"])
    df = df[df["view"] > 0]

    num_cols = ["view", "danmaku", "reply", "like", "coin", "favorite", "share"]
    for col in num_cols:
        df.loc[df[col] < 0, col] = 0

    df = df.drop_duplicates(subset=["period", "title", "up_name"])

    df["view_rank_in_period"] = df.groupby("period")["view"].rank(ascending=False, method="first")
    df["is_top10"] = (df["view_rank_in_period"] <= 10).astype(int)

    print("数据清洗完成")
    return df.reset_index(drop=True)


def run():
    df = load_all_periods()
    print(f"原始数据共 {len(df)} 条")

    df = clean(df)
    print(f"清洗后剩余 {len(df)} 条")

    df.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")
    print(f"已保存到 {OUT_PATH}")
    return df


if __name__ == "__main__":
    run()