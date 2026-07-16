import requests
import json
import time
import random
import os

try:
    from fake_useragent import UserAgent
    ua = UserAgent()
except Exception:
    ua = None

API_URL = "https://api.bilibili.com/x/web-interface/popular/series/one"
SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
MAX_RETRY = 3
TIMEOUT = 8


def get_headers():
    if ua is not None:
        agent = ua.random
    else:
        # fake_useragent装不上或者网络问题拿不到UA库时的兜底
        agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36")
    return {
        "User-Agent": agent,
        "Referer": "https://www.bilibili.com/",
    }


def fetch_one_period(number):
    """抓取第number期的数据，失败自动重试，返回原始json（dict）或None"""
    params = {"number": number}
    for attempt in range(1, MAX_RETRY + 1):
        try:
            resp = requests.get(API_URL, params=params, headers=get_headers(), timeout=TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            # code不为0说明这期没数据了（比如超过了最新一期）
            if data.get("code") != 0:
                print(f"第{number}期返回code={data.get('code')}，可能已经没有更多数据了")
                return None
            video_list = data.get("data", {}).get("list", [])
            if not video_list:
                print(f"第{number}期没有视频数据，停止")
                return None
            print(f"第{number}期抓取成功，共{len(video_list)}个视频")
            return data
        except Exception as e:
            print(f"第{number}期第{attempt}次请求失败：{e}")
            time.sleep(random.uniform(1, 2))
    print(f"第{number}期重试{MAX_RETRY}次仍失败，跳过")
    return None


def run(start=1, end=None):
    """
    start/end: 抓取的期数区间，end为None时会一直抓到接口没数据为止
    """
    os.makedirs(SAVE_DIR, exist_ok=True)
    number = start
    empty_count = 0
    while True:
        if end is not None and number > end:
            break
        save_path = os.path.join(SAVE_DIR, f"period_{number}.json")
        if os.path.exists(save_path):
            print(f"第{number}期已经抓过了，跳过")
            number += 1
            continue

        result = fetch_one_period(number)
        if result is None:
            empty_count += 1
            if empty_count >= 2:  # 连续两期都拿不到数据，基本可以判断抓完了
                print("连续两期无数据，判定已抓取到最新一期，结束")
                break
        else:
            empty_count = 0
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

        number += 1
        time.sleep(random.uniform(0.8, 1.8))  # 控制请求频率，别太快被封


if __name__ == "__main__":
    # 从第1期开始一直抓到最新一期
    run(start=1, end=None)

