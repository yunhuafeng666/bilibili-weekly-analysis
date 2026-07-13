# -*- coding: utf-8 -*-
import os
import pandas as pd

# 数据路径
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned.csv")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

def run():
    df = pd.read_csv(DATA_PATH)
    # 先看看数据
    print(df.head())

    os.makedirs(OUT_DIR, exist_ok=True)
    excel_file = os.path.join(OUT_DIR, "analysis_result.xlsx")

    # 要分析的几个指标
    metrics = {
        "coin": "投币",
        "danmaku": "弹幕",
        "favorite": "收藏",
        "like": "点赞",
        "reply": "评论",
        "share": "转发",
        "view": "播放量",
    }

    print("开始分析...")
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        for col, name in metrics.items():
            # 1. 视频TOP10
            top_video = df.sort_values(col, ascending=False).head(10)[["title", "up_name", col]]
            top_video.to_excel(writer, sheet_name=f"{name}最多视频TOP10", index=False)

            # 2. up主TOP10 (按累计值)
            top_up = df.groupby("up_name")[col].sum().sort_values(ascending=False).head(10).reset_index()
            top_up.to_excel(writer, sheet_name=f"{name}最多up主TOP10", index=False)

        # 3. up主上榜次数
        up_cnt = df["up_name"].value_counts().head(10)
        up_ratio = (up_cnt / up_cnt.sum() * 100).round(2)
        pd.DataFrame({"up_name": up_cnt.index, "count": up_cnt.values, "ratio_%": up_ratio.values}).to_excel(writer, sheet_name="上榜次数前十up主占比", index=False)

        # 4. 话题（分区）占比
        zone_cnt = df["zone"].value_counts().head(10)
        zone_ratio = (zone_cnt / zone_cnt.sum() * 100).round(2)
        pd.DataFrame({"zone": zone_cnt.index, "count": zone_cnt.values, "ratio_%": zone_ratio.values}).to_excel(writer, sheet_name="上榜次数前十话题占比", index=False)

        # 5. 相关性分析
        cols = ["view", "danmaku", "reply", "like", "coin", "favorite", "share"]
        corr = df[cols].corr().round(3)
        corr.to_excel(writer, sheet_name="指标相关性分析")

    print(f"搞定，分析结果已保存到 {excel_file}")

    # 打印几个关键的相关性
    print("\n===== 核心指标相关性（报告可用） =====")
    print(f"播放量 ↔ 点赞：{corr.loc['view', 'like']}")
    print(f"播放量 ↔ 收藏：{corr.loc['view', 'favorite']}")
    print(f"弹幕数 ↔ 评论数：{corr.loc['danmaku', 'reply']}")

if __name__ == "__main__":
    run()