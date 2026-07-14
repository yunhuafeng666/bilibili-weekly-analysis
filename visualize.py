# -*- coding: utf-8 -*-
import os
import pandas as pd
from pyecharts.charts import Bar, Pie, Page
from pyecharts import options as opts

# 数据路径
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned.csv")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

# 图表配色，用个暗红色，跟截图里差不多
BAR_COLOR = "#8B1E3F"

def run():
    df = pd.read_csv(DATA_PATH)
    # 先看看数据
    print(df.head())

    os.makedirs(OUT_DIR, exist_ok=True)
    page = Page(layout=Page.SimplePageLayout)

    # 要画的几个指标
    metrics = {
        "coin": "投币",
        "danmaku": "弹幕",
        "favorite": "收藏",
        "like": "点赞",
    }

    print("开始画图...")
    for col, name in metrics.items():
        # 1. 视频TOP10
        top_video = df.sort_values(col, ascending=False).head(10)
        bar1 = Bar().add_xaxis(top_video["title"].str.slice(0, 12).tolist()).add_yaxis(name, top_video[col].tolist(), itemstyle_opts=opts.ItemStyleOpts(color=BAR_COLOR), label_opts=opts.LabelOpts(is_show=False))
        bar1.set_global_opts(title_opts=opts.TitleOpts(title=f"{name}最多的视频", pos_left="center"), xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
        page.add(bar1)

        # 2. up主TOP10 (按累计值)
        top_up = df.groupby("up_name")[col].sum().sort_values(ascending=False).head(10)
        bar2 = Bar().add_xaxis(top_up.index.tolist()).add_yaxis(name, top_up.values.tolist(), itemstyle_opts=opts.ItemStyleOpts(color=BAR_COLOR), label_opts=opts.LabelOpts(is_show=False))
        bar2.set_global_opts(title_opts=opts.TitleOpts(title=f"{name}最多的up主", pos_left="center"), xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
        page.add(bar2)

    # 3. up主上榜次数
    up_cnt = df["up_name"].value_counts().head(10)
    bar3 = Bar().add_xaxis(up_cnt.index.tolist()).add_yaxis("上榜次数", up_cnt.values.tolist(), itemstyle_opts=opts.ItemStyleOpts(color=BAR_COLOR), label_opts=opts.LabelOpts(is_show=False))
    bar3.set_global_opts(title_opts=opts.TitleOpts(title="上榜次数前十的up主", pos_left="center"), xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
    page.add(bar3)

    pie1 = Pie().add("", list(zip(up_cnt.index.tolist(), up_cnt.values.tolist())), radius=["35%", "65%"]).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} {d}%"))
    pie1.set_global_opts(title_opts=opts.TitleOpts(title="上榜次数前十的up主占比", pos_left="center"))
    page.add(pie1)

    # 4. 话题（分区）占比
    zone_cnt = df["zone"].value_counts().head(10)
    bar4 = Bar().add_xaxis(zone_cnt.index.tolist()).add_yaxis("上榜次数", zone_cnt.values.tolist(), itemstyle_opts=opts.ItemStyleOpts(color=BAR_COLOR), label_opts=opts.LabelOpts(is_show=False))
    bar4.set_global_opts(title_opts=opts.TitleOpts(title="上榜次数前十的话题", pos_left="center"), xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
    page.add(bar4)

    pie2 = Pie().add("", list(zip(zone_cnt.index.tolist(), zone_cnt.values.tolist())), radius=["35%", "65%"]).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} {d}%"))
    pie2.set_global_opts(title_opts=opts.TitleOpts(title="上榜次数前十的话题占比", pos_left="center"))
    page.add(pie2)

    out_path = os.path.join(OUT_DIR, "visualization.html")
    page.render(out_path)
    print(f"搞定，图都画好了，在 {out_path}")

if __name__ == "__main__":
    run()
