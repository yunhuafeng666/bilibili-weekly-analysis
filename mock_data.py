# -*- coding: utf-8 -*-
import json, os, random

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

UP_NAMES = ["老番茄", "凉风Kaze", "盗月社食遇记", "小潮院长", "绵羊料理", "罗翔说刑法", "原神", "手工耿", "某幻君",
            "泛式", "老师好我叫何同学", "TF家族", "才疏学浅的才浅", "敬汉卿", "哔哩哔哩晚会"]
ZONES = ["搞笑", "单机游戏", "日常", "短片·手书·配音", "美食制作", "电子竞技", "手机游戏", "影视杂谈", "科学科普",
         "鬼畜调教"]
TITLES = [
    "回村三天，二舅治好了我的精神内耗",
    "【何同学】我做了一个自己打字的键盘",
    "我被告知跟我22年的名字，我不能用要改名！我如何维权的",
    "敢杀我的马？！",
    "游戏科学新作《黑神话：悟空》13分钟实机演示",
    "做好防护，走出家门，大家的努力终将有回报",
]


def gen_video(vid):
    play = random.randint(500000, 8000000)
    danmu = int(play * random.uniform(0.005, 0.03))
    like = int(play * random.uniform(0.02, 0.12))
    coin = int(play * random.uniform(0.01, 0.06))
    fav = int(play * random.uniform(0.01, 0.08))
    reply = int(play * random.uniform(0.002, 0.02))
    share = int(play * random.uniform(0.001, 0.01))

    return {
        "aid": 100000 + vid,
        "bvid": f"BV{vid:010d}",
        "title": random.choice(TITLES) + f"（示例{vid}）",
        "owner": {"name": random.choice(UP_NAMES)},
        "tname": random.choice(ZONES),
        "stat": {
            "view": play,
            "danmaku": danmu,
            "reply": reply,
            "favorite": fav,
            "coin": coin,
            "share": share,
            "like": like,
        },
        "desc": "这是一条用于测试的模拟简介",
    }


def run(period_count=52):
    os.makedirs(SAVE_DIR, exist_ok=True)
    for number in range(1, period_count + 1):
        print(f"生成第 {number} 期...")
        video_list = [gen_video(number * 100 + i) for i in range(30)]
        data = {"code": 0, "message": "0", "data": {"list": video_list}}

        path = os.path.join(SAVE_DIR, f"period_{number}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"搞定，{period_count}期假数据已生成在 {SAVE_DIR}")


if __name__ == "__main__":
    run()