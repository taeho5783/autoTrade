import time
import pyupbit
import datetime
import requests

access = "DxCIIhohzsmTPW2RIlrn1fF9xzdFFOkTxMMyvuFu"          # 본인 값으로 변경
secret = "KSxIJ4Pfys9tSFUNH9xNxrPjPPbGBSS2ALL72FYT"          # 본인 값으로 변경
myToken = "xoxb-your-token"

def send_message(msg):
    """디스코드 메세지 전송"""
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1203596642020757504/eE1V7osNQbIFGmqlg3FYsCsCEwhGbyzkzFY5SQT72-vyPsulBy7Y-krEqiWXTpTQiYFt"
    requests.post(DISCORD_WEBHOOK_URL, data=message)
    print(message)


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
send_message("autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            ma15 = get_ma15("KRW-BTC")
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    send_message("BTC buy : " +str(buy_result))
            else:
                if (now.hour == 11  or now.hour == 20) and  now.minute == 30 and now.second <= 5: 
                    btc_bal = get_balance("BTC")
                    krw_bal = get_balance("KRW")
                    send_message("BTC  : " +str(btc_bal))
                    send_message("KRW  : " +str(krw_bal))
                    time.sleep(5)
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                sell_result = upbit.sell_market_order("KRW-BTC", btc*0.9995)
                send_message("BTC buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        send_message(e)
        time.sleep(1)