import sys
import os
import warnings

# 忽略sklearn的一些警告，省得控制台太乱
warnings.filterwarnings("ignore", category=UserWarning)

# 确保能导入同级的模块
sys.path.append(os.path.dirname(__file__))

import pandas as pd

# 导入项目自己的模块
import crawler
import mock_data
import clean_data
import analysis
import ml_model
import visualize

# 定义用于模型的特征，这里特意没放播放量(view)，防止数据泄露
FEATURES = ["danmaku", "reply", "like", "coin", "favorite", "share"]


def main():
    # 简单的命令行参数解析，加个--mock就用假数据跑
    use_mock = False
    if len(sys.argv) > 1 and sys.argv[1] == '--mock':
        use_mock = True

    print(">>> 开始执行主流程...")

    # 1. 数据采集
    print("1. 正在获取数据...")
    if use_mock:
        # 调试时用mock数据快一点
        mock_data.run(period_count=52)
    else:
        # 正式爬取
        crawler.run(start=1, end=None)
    print("   数据获取完成。")

    # 2. 数据清洗
    print("2. 正在清洗数据...")
    clean_data.run()
    print("   数据清洗完成。")

    # 3. 统计分析
    print("3. 正在做统计分析...")
    analysis.run()
    print("   统计分析完成。")

    # 4. 机器学习建模
    print("4. 正在训练模型...")
    # 接收模型和特征重要性
    model, importance_data = ml_model.run()
    print("   模型训练完成。")

    # 5. 可视化
    print("5. 正在生成可视化图表...")
    visualize.run()
    print("   可视化完成。")

    # --- 结果展示 ---
    print("\n--- 模型特征重要性 ---")
    # 直接打印特征和对应的权重
    for i, name in enumerate(FEATURES):
        print(f"{name}: {model.feature_importances_[i]:.4f}")

    # 简单测试一下模型
    print("\n--- 模型预测测试 ---")
    # 构造一个测试样本
    test_data = pd.DataFrame([[2000, 210, 1500, 800, 650, 320]], columns=FEATURES)
    pred = model.predict(test_data)

    print("测试数据: 弹幕2000, 评论210, 点赞1500, 投币800, 收藏650, 转发320")
    if pred[0] == 1:
        print("预测结果: 这个视频能火，可以进每周必看！")
    else:
        print("预测结果: 这个视频热度不够，进不了榜。")

    print("\n✅ 全部搞定！结果在 output 文件夹里。")


if __name__ == "__main__":
    main()