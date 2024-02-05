import pyupbit
import datetime

access = "DxCIIhohzsmTPW2RIlrn1fF9xzdFFOkTxMMyvuFu"          # 본인 값으로 변경
secret = "KSxIJ4Pfys9tSFUNH9xNxrPjPPbGBSS2ALL72FYT"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회


now = datetime.datetime.now()

print(now.hour)