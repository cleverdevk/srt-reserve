import asyncio
import os
import random
import time

from SRT import SRT
from telegram import Bot


async def main():
    password = os.environ.get("SRT_PASSWORD")
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    srt = SRT("2193428384", password)

    telegram_bot = None
    if telegram_token is not None and telegram_chat_id is not None:
        telegram_bot = Bot(telegram_token)

    dep = "수서"
    arr = "동탄"
    date = "20240330"
    dep_time = "150000"
    deadline_time = "170000"

    starting_message = '''
SRT Bot is starting to search train with
{} to {} at {} ~ {}'''.format(dep, arr, dep_time, deadline_time)

    if telegram_bot is not None:
        await telegram_bot.send_message(telegram_chat_id, starting_message)

    trains = srt.search_train(dep, arr, date, dep_time)

    loop = True

    while loop:
        print("searching...")
        for train in trains:
            if train.dep_time < deadline_time:
                _ = srt.reserve(train)
                print("reservation success: ", train)
                reservation_message = '''
Reservation Notification
{} 열차가 예약되었습니다. 결제가 필요합니다.
https://etk.srail.kr/hpg/hra/02/selectReservationList.do
'''.format(train)
                if telegram_bot is not None:
                    await telegram_bot.send_message(telegram_chat_id, reservation_message)
                loop = False
                break
        if not loop:
            break
        time.sleep(20 + int(10.0 * random.uniform(0.1, 0.9)))

if __name__ == "__main__":
    asyncio.run(main())
