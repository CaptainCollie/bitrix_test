import datetime
from currency1.src.update_currency import start

while True:
    now = datetime.datetime.now()
    print(now)
    if now.hour == 12 and now.minute == 0 and now.second == 0:
        start()
