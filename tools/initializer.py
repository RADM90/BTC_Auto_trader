import pyupbit
import numpy as np
import schedule
from fbprophet import Prophet


def get_keys():
    """API키 불러오기"""
    obj = {}
    with open('static/upbit_keys.txt', 'r+', encoding='utf8') as txt:
        line1 = txt.readline().replace("\n", "").split("\t")
        line2 = txt.readline().split("\t")
        obj['UPBIT_OPEN_API_ACCESS_KEY'] = line1[1] if line1[0] == 'Access key' else ''
        obj['UPBIT_OPEN_API_SECRET_KEY'] = line2[1] if line2[0] == 'Secret key' else ''
    return obj


def get_balance(currency):
    """계좌 잔고 조회"""
    balances = upbit.get_balances()
    for dic_obj in balances:
        if dic_obj['currency'] == currency:
            if dic_obj['balance'] is not None:
                return float(dic_obj['balance'])
            else:
                return 0
    return 0


def get_current_price(currency):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=currency)["orderbook_units"][0]["ask_price"]


def get_start_time(currency):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(currency, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_ror(k=0.5):
    """변동폭 상수 별 누적수익률 계산"""
    df = pyupbit.get_ohlcv("KRW-BTC", count=7)  # OHLCV(Open/High/Low/Close/Volume; 시가/고가/저가/종가/거래량) 데이터
    df['range'] = (df['high'] - df['low']) * k  # 변동폭 계산((고가 - 저가) * k값)
    df['target'] = df['open'] + df['range'].shift(1)  # target(매수가격), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)  # ror(수익률; Rate of Revenue)
    ror = df['ror'].cumprod()[-2]  # 누적 곱 계산(cumprod)을 통한 누적 수익률 계산
    # df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100  # Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
    # mdd = df['dd'].max()  #MDD 계산
    return ror


def get_best_k():
    """최적 상수 k를 찾기 위한 함수"""
    k_arr = []
    ror_arr = []
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(k)
        k_arr.append(k)
        ror_arr.append(ror)
    return k_arr[ror_arr.index(min(ror_arr))]


def get_target_price(currency, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(currency, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


predicted_close_price = 0
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute60")
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]
    model = Prophet()
    model.fit(data)
    future_dataframe = model.make_future_dataframe(periods=24, freq='H')
    prediction = model.predict(future_dataframe)
    close_dataframe = prediction[prediction['ds'] == prediction.iloc[-1]['ds'].replace(hour=9)]
    if len(close_dataframe) == 0:
        close_dataframe = prediction[prediction['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    close_value = close_dataframe['yhat'].values[0]
    predicted_close_price = close_value


def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15


access_key, secret_key = get_keys().values()  # API 키 호출
upbit = pyupbit.Upbit(access_key, secret_key)  # 로그인
