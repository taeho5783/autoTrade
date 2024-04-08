import pyupbit
import time
import datetime
import requests

access = "DxCIIhohzsmTPW2RIlrn1fF9xzdFFOkTxMMyvuFu"          # 본인 값으로 변경
secret = "KSxIJ4Pfys9tSFUNH9xNxrPjPPbGBSS2ALL72FYT"          # 본인 값으로 변경


def send_message(msg):
    """디스코드 메세지 전송"""
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1203596642020757504/eE1V7osNQbIFGmqlg3FYsCsCEwhGbyzkzFY5SQT72-vyPsulBy7Y-krEqiWXTpTQiYFt"
    requests.post(DISCORD_WEBHOOK_URL, data=message)
    print(message)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 시작 메세지 슬랙 전송
send_message("autotrade start")

while True:
    t_now = datetime.datetime.now()
    try:
        # 각 코인의 매도 가격 설정(+25%이상 -10%이하)
        coins_to_sell = {
            "POLYX"  : {"sell_price": 975.875, "target_price": 585.525},
            "BCH"    : {"sell_price": 1223375, "target_price": 734025},
            "HIFI"   : {"sell_price": 2082.5,  "target_price": 1249.5},
            "PUNDIX" : {"sell_price": 1488.75, "target_price": 1071.9},
            "T"      : {"sell_price": 82.2625, "target_price": 49.3575}
        }

        # 매도 주문 실행
        for coin, info in coins_to_sell.items():
            ticker = f"KRW-{coin}"
            current_price = pyupbit.get_current_price(ticker)
            if current_price >= info['sell_price']:
                coin_balance = upbit.get_balance(ticker)
                if coin_balance > 0:
                    sell_result = upbit.sell_market_order(ticker, coin_balance)
                    sendmsg = f"Sold {coin} successfully at market price."
                    send_message(sendmsg)
            elif current_price <= info['target_price']:
                coin_balance = upbit.get_balance(ticker)
                if coin_balance > 0:
                    sell_result = upbit.sell_market_order(ticker, coin_balance)
                    sendmsg = f"Sold {coin} successfully at market price due to reaching target price."
                    send_message(sendmsg)
            
            if t_now.hour == 10 and t_now.minute == 37 and t_now.second <= 5: 
                sendmsg = f" {coin} current_price is {current_price}."
                send_message(sendmsg)
                time.sleep(5)
            time.sleep(1)
    except Exception as e:
        print(f"Error occurred: {e}")
        send_message(f"Error occurred: {e}")
        time.sleep(1)



