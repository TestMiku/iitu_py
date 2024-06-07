import aiohttp
import asyncio
import json

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def send_data(url, params, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, json=data) as response:
            return await response.text()

async def main():
    first_url = "https://script.google.com/macros/s/AKfycbw63gXKFMPd8oi80wDSaH1plSWCTANQlzzCYSDscKyN2bggy2T1oIrHspNBkmsLXnKl/exec"
    first_response = await fetch_data(first_url)
    first_data = json.loads(first_response)  
    print("First response:")
    # print("First response:", first_data)

    # GET запрос по второй ссылке
    second_url = "https://bitrix.avh.kz/reports/?file=crm_logistic_supply_reports&auth=%24Vd%7Brsk%3D%3Fv5Mojx%253CkOSAFGMP%23xFX3%27"
    second_response = await fetch_data(second_url)
    second_data = json.loads(second_response)
    print("Second response:")
    # print("Second response:", second_data)

    data = []
    for item in first_data:
        id_value = item["id"]
        # if id_value in second_data and second_data[id_value] == "Завершенные":
        #     num_do_value = item["num_do"]
        #     data.append(num_do_value)
        for entry in second_data:
            if entry.get("ID") == id_value and entry.get("STAGE_ID") == "Завершенные":
                num_do_value = item["num_do"]
                data.append(num_do_value)
            
    aps_url = "https://script.google.com/macros/s/AKfycbw63gXKFMPd8oi80wDSaH1plSWCTANQlzzCYSDscKyN2bggy2T1oIrHspNBkmsLXnKl/exec"
    params = {"get_data": "debtdoc"}
    sending = await send_data(aps_url, params, data)
    print(sending)
    # print("Data for POST request:", data)


def main_sync():
    asyncio.run(main())
#https://script.google.com/macros/s/AKfycbw63gXKFMPd8oi80wDSaH1plSWCTANQlzzCYSDscKyN2bggy2T1oIrHspNBkmsLXnKl/exec
#https://script.google.com/macros/s/AKfycbzUH2mPRUy682XAe7eC-f7sh61Iw8WyJ7edIc-GG09_U9AiyKu0NIVwgqTg91AJHQGX3Q/exec