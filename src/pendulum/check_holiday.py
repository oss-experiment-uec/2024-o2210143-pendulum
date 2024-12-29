from __future__ import annotations
import pendulum
import jpholiday
from datetime import date
from datetime import datetime
from datetime import timedelta

def check_holiday():
    # 現在の日本時間を取得
    now = pendulum.now('Asia/Tokyo')
    current_date = now.date()
    
    # 今日が祝日かどうか
    is_holiday = jpholiday.is_holiday(current_date)
    holiday_name = jpholiday.is_holiday_name(current_date)
    
    # 次の祝日を検索
    next_holiday = None
    for day in range(1, 365):  # 最大1年先まで検索
        future_date = current_date.add(days=day)
        if jpholiday.is_holiday(future_date):
            next_holiday = (future_date, jpholiday.is_holiday_name(future_date))
            break
    
    # 結果を表示
    print(f"現在の日本時間: {now}")
    if is_holiday:
        print(f"今日は祝日です！ ({holiday_name})")
    else:
        print("今日は祝日ではありません。")
        if next_holiday:
            next_date, next_name = next_holiday
            print(f"次の祝日は {next_date} ({next_name}) です。")
        else:
            print("次の祝日が見つかりませんでした。")

# 実行
if __name__ == "__main__":
    check_holiday()