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
    first_url = "https://bitrix.avh.kz/reports/?file=crm_logistic_supply_reports&auth=%24Vd%7Brsk%3D%3Fv5Mojx%253CkOSAFGMP%23xFX3%27"
    first_response = await fetch_data(first_url)
    first_data = json.loads(first_response)

    usefullStages = ['Отклоненные', 'Доставка', 'Согласование автора и начальника отдела снабжения',
                     'Подтверждения получения товара', 'Создание ДО', 'Завершенные', 'Оплата']

    # ['Заявка в обработке', 'Подтверждения получения товара',
    #                  'Создание ДО', 'Заявка на создание ДО',
    #                  'Отклоненные', 'Создать ДО', 'Отмененные',
    #                  'Закрытые', 'Согласование заявки начальником отдела снабжения',
    #                  'Оплата', 'Завершенные', 'Новая заявка',
    #                  'Согласования заявки руководителем', 'Процесс доставки',
    #                  'Просрочено', 'Поиск машины', 'Распределение',
    #                  'Согласование автора и начальника отдела снабжения',
    #                  'Доставка', 'Подтверждение заявки', 'Отмененные заявителем']

           
           

    data_list = []
    for item in first_data:
        data_dict = {}
        
        if item["STAGE_ID"] in usefullStages and float(item["OPPORTUNITY"]) > 100000.00 and item["ID"] == "6769" or item["ID"] == "60":
        # if  item["ID"] == "42" :
            data_dict["uf_crm_data_oplaty_value"] = item["UF_CRM_DATA_OPLATY"]
            data_dict["id_value"] = item["ID"]
            # data_dict["STAGE_ID"] = item["STAGE_ID"]
            data_dict["podrazdelenie_value"] = "Аврора Сервис" if item["UF_CRM_6_1713191653"] == "Аврора 77" else item["UF_CRM_6_1713191653"]
            data_dict["snabjenec_value"] = item["ASSIGNED_BY_ID"]
            data_dict["postavshik_value"] = item["UF_CRM_6_1685075629194"]
            data_dict["num_chet_value"] = item["UF_CRM_6_1693999985544"]
            data_dict["sum_chet_value"] = str(float(item["OPPORTUNITY"]))
            data_dict["valuta_value"] = item["CURRENCY_ID"]
            data_dict["product_list"] = [product["PRODUCT_NAME"] for product in item["PRODUCTS"]] if item["PRODUCTS"] else []
            data_dict["city_value"] = item["UF_CRM_6_1685076926707"]
            # data_dict["city_value"] = (item["UF_CRM_6_1686132937"] if item["UF_CRM_6_1686132937"] else "") + item["UF_CRM_6_1685077108231"]
            data_dict["samovyvoz_value"] = item["UF_CRM_6_1685077108231"]
            data_dict["srok_value"] = item["UF_CRM_6_1685077043846"]

            data_list.append(data_dict)

    print(data_list)

    aps_url = "https://script.google.com/macros/s/AKfycbyprYJ9vjummPg1L1szXVhuwXDAMjUdoh6dfG8QtUHDbVPh2pWTzdP1cswfFBURw7nI/exec"
    params = {"get_data": "debtdoc"}
    sending = await send_data(aps_url, params, data_list)
    print(sending)
    # print("Data for POST request:", data)


def main_sync():
    asyncio.run(main())




