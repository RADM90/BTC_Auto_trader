from tools import initializer as init
import datetime
import time
import schedule

def time_display():
    """로그용 시간 표시 기능"""
    return "[" + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M]")

upbit = init.upbit

while True:
    print(time_display(), "Loop Start")
    best_k = init.get_best_k()
    try:
        now = datetime.datetime.now()
        start_time = init.get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        # 분기점
        schedule.every().hour.do(lambda: init.predict_price("KRW-BTC"))
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = init.get_target_price("KRW-BTC", best_k)
            current_price = init.get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = init.get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw * 0.9995)
        else:
            btc = init.get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc * 0.9995)
        time.sleep(1)

        """FB Prophet 예측값을 통한 매매"""
        # schedule.run_pending()
        # if start_time < now < end_time - datetime.timedelta(seconds=10):
        #     target_price = init.get_target_price("KRW-BTC", best_k)
        #     current_price = init.get_current_price("KRW-BTC")
        #     if target_price < current_price < init.predicted_close_price:
        #         krw = init.get_balance("KRW")
        #         if krw > 5000:
        #             upbit.buy_market_order("KRW-BTC", krw * 0.9995)
        # else:
        #     btc = init.get_balance("BTC")
        #     if btc > 0.00008:
        #         upbit.sell_market_order("KRW-BTC", btc * 0.9995)

        """15일 이동평균선 조회를 통한 매매"""
        # if start_time < now < end_time - datetime.timedelta(seconds=10):
        #     target_price = init.get_target_price("KRW-BTC", best_k)
        #     ma15 = init.get_ma15("KRW-BTC")
        #     current_price = init.get_current_price("KRW-BTC")
        #     if target_price < current_price and ma15 < current_price:
        #         krw = init.get_balance("KRW")
        #         if krw > 5000:
        #             upbit.buy_market_order("KRW-BTC", krw * 0.9995)
        # else:
        #     btc = init.get_balance("BTC")
        #     if btc > 0.00008:
        #         upbit.sell_market_order("KRW-BTC", btc * 0.9995)
    except Exception as e:
        print(e)
        time.sleep(1)
    finally:
        print(time_display(), "Loop End")
