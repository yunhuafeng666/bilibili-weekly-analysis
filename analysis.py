# -*- coding: utf-8 -*-
"""
用pandas对清洗后的数据做统计分析：
1. 各项数据（投币/弹幕/收藏/点赞/评论/转发/播放量）Top10视频、Top10 up主（按累计值）
2. up主上榜次数统计、话题（分区）出现次数统计，算占比
3. 各指标之间的相关性分析
"""
import os
import pandas as pd

# 1. 统一路径处理（修复找不到文件核心问题）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前脚本绝对目录
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)                # 项目根目录
DATA_PATH = os.path.join(PROJECT_DIR, "data", "cleaned.csv")
OUT_DIR = os.path.join(PROJECT_DIR, "output")

# 自动创建文件夹
os.makedirs(os.path.join(PROJECT_DIR, "data"), exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def top10_video_by(df, col):
    """按单指标降序取TOP10视频"""
    return df.sort_values(col, ascending=False).head(10)[["title", "up_name", col]]

def top10_up_by(df, col):
    """up主数据汇总求和，取TOP10"""
    grouped = df.groupby("up_name")[col].sum().sort_values(ascending=False).head(10)
    return grouped.reset_index()

def up_rank_ratio(df):
    """统计up主上榜次数及占比"""
    cnt = df["up_name"].value_counts().head(10)
    ratio = (cnt / cnt.sum() * 100).round(2)
    return pd.DataFrame({"up_name": cnt.index, "count": cnt.values, "ratio_%": ratio.values})

def zone_ratio(df):
    """统计分区出现次数及占比"""
    cnt = df["zone"].value_counts().head(10)
    ratio = (cnt / cnt.sum() * 100).round(2)
    return pd.DataFrame({"zone": cnt.index, "count": cnt.values, "ratio_%": ratio.values})

def correlation_analysis(df):
    """数值指标相关性矩阵"""
    cols = ["view", "danmaku", "reply", "like", "coin", "favorite", "share"]
    corr = df[cols].corr().round(3)
    return corr

def load_csv_safe(file_path):
    """兼容多编码读取CSV，解决中文乱码"""
    encodings = ["utf-8-sig", "utf-8", "gbk", "gb2312"]
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            print(f"✅ 文件读取成功，编码：{enc}")
            return df
        except UnicodeDecodeError:
            continue
    raise Exception("CSV文件编码不支持，尝试utf-8/gbk均失败")

def run():
    print(f"📂 待读取数据路径：{DATA_PATH}")
    # 文件存在性校验
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"未找到清洗数据文件！\n路径：{DATA_PATH}\n请先运行clean_data.py生成cleaned.csv"
        )
    # 读取数据
    df = load_csv_safe(DATA_PATH)
    print(f"📊 数据集共 {df.shape[0]} 条视频数据")

    metrics = {
        "coin": "投币",
        "danmaku": "弹幕",
        "favorite": "收藏",
        "like": "点赞",
        "reply": "评论",
        "share": "转发",
        "view": "播放量",
    }
    excel_file = os.path.join(OUT_DIR, "analysis_result.xlsx")
    # 指定openpyxl引擎，避免Excel版本报错
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        for col, name in metrics.items():
            top10_video_by(df, col).to_excel(writer, sheet_name=f"{name}最多视频TOP10", index=False)
            top10_up_by(df, col).to_excel(writer, sheet_name=f"{name}最多up主TOP10", index=False)
        up_rank_ratio(df).to_excel(writer, sheet_name="上榜次数前十up主占比", index=False)
        zone_ratio(df).to_excel(writer, sheet_name="上榜次数前十话题占比", index=False)
        correlation_analysis(df).to_excel(writer, sheet_name="指标相关性分析")

    print(f"\n🎉 分析完成！结果保存至：{excel_file}")
    # 打印相关性摘要
    corr = correlation_analysis(df)
    print("\n===== 核心指标相关性（报告可用） =====")
    print(f"播放量 ↔ 点赞：{corr.loc['view', 'like']}")
    print(f"播放量 ↔ 收藏：{corr.loc['view', 'favorite']}")
    print(f"弹幕数 ↔ 评论数：{corr.loc['danmaku', 'reply']}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"\n❌ 程序运行失败：{e}")