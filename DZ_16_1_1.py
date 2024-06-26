from bs4 import BeautifulSoup
import requests
import csv
from model import Products
import datetime

date = datetime.datetime.now().strftime("%H.%M %d.%m.%Y")

def parser(url: str):

        dict_1 = {}
        list_coins = []
        sum_market_capitalization = 0
        page = 0

        for i in range(10):
            page += i
            response = requests.get(f'{url}?page={page}')
            soup = BeautifulSoup(response.text, 'lxml')
            coins = soup.find_all('div', class_="sc-4c05d6ef-0 bLqliP")

            for coin in coins:
                name_coin = coin.find("p", class_="sc-71024e3e-0 ehyBa-d").text
                market_capitalization = coin.find_next("span", class_="sc-11478e5d-1 hwOFkt").text
                dict_1[name_coin] = [market_capitalization]
                sum_market_capitalization += int(market_capitalization[1:].replace(',', ''))

        for key in dict_1:
            percentage_market_capitalization = round(int(''.join(dict_1[key][0]).replace(',', '')[1:])
                                                     / sum_market_capitalization * 100, 2)
            dict_1[key] += [f"{percentage_market_capitalization}%"]

        for key in dict_1:
            list_coins.append(Products(name_coin=key,
                                       market_capitalization=dict_1[key][0],
                                       percentage_market_capitalization=dict_1[key][1]))
        create_csv()
        writer_csv(list_coins)

def create_csv():
    with open(f'{date}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Name",
            "MC",
            "MP "
        ])

def writer_csv(coins: list[Products]):
    with open(f'{date}.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for coin in coins:
            writer.writerow([
                coin.name_coin,
                coin.market_capitalization,
                coin.percentage_market_capitalization
            ])


if __name__ == "__main__":
    parser(url='https://coinmarketcap.com/ru/')