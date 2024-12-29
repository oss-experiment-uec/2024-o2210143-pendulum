import unittest
from unittest.mock import patch
from datetime import date, timedelta
import pendulum
import jpholiday

# テスト対象関数をインポート
from holiday import check_holiday


class TestHolidayCheck(unittest.TestCase):
    @patch('holiday.pendulum.now')
    def test_today_is_holiday(self, mock_now):
        """今日が祝日の場合のテスト"""
        # モックで特定の日付（祝日）を指定
        mock_now.return_value = pendulum.datetime(2024, 1, 1, tz="Asia/Tokyo")  # 元日
        with patch('holiday.jpholiday.is_holiday', return_value=True):
            with patch('holiday.jpholiday.is_holiday_name', return_value="元日"):
                # 標準出力をテスト
                with self.assertLogs(level="INFO") as log:
                    check_holiday()
                    self.assertIn("今日は祝日です！ (元日)", log.output[0])

    @patch('holiday.pendulum.now')
    def test_today_is_not_holiday(self, mock_now):
        """今日が祝日ではない場合のテスト"""
        mock_now.return_value = pendulum.datetime(2024, 1, 2, tz="Asia/Tokyo")  # 平日
        with patch('holiday.jpholiday.is_holiday', return_value=False):
            with patch('holiday.jpholiday.is_holiday_name', return_value=None):
                # 標準出力をテスト
                with self.assertLogs(level="INFO") as log:
                    check_holiday()
                    self.assertIn("今日は祝日ではありません。", log.output[0])

    @patch('holiday.pendulum.now')
    def test_next_holiday(self, mock_now):
        """次の祝日を正しく取得できるかのテスト"""
        mock_now.return_value = pendulum.datetime(2024, 1, 2, tz="Asia/Tokyo")  # 平日
        with patch('holiday.jpholiday.is_holiday') as mock_is_holiday:
            with patch('holiday.jpholiday.is_holiday_name') as mock_is_holiday_name:
                # モックの設定
                mock_is_holiday.side_effect = lambda d: d == date(2024, 1, 8)  # 成人の日
                mock_is_holiday_name.side_effect = lambda d: "成人の日" if d == date(2024, 1, 8) else None
                
                # 標準出力をテスト
                with self.assertLogs(level="INFO") as log:
                    check_holiday()
                    self.assertIn("次の祝日は 2024-01-08 (成人の日) です。", log.output[0])

if __name__ == "__main__":
    unittest.main()
