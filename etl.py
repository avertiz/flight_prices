import quotes
import os
import sqlite3
import time
from datetime import date, datetime, timedelta

def main():

    date_from = date.today().strftime("%d/%m/%Y")
    date_to = date.today() + timedelta(days=365)
    date_to = date_to.strftime("%d/%m/%Y")

    cities = ["city:SFO", 
        "city:LAS", 
        "city:AUS", 
        "city:DEN", 
        "city:NYC", 
        "city:SEA",
        "city:MAD", 
        "city:BCN",
        "city:LAX",
        "city:PAR",
        "city:MUC",
        "city:LON",
        "city:MEX",
        "city:REK",
        "city:VIE"
        "city:SPU", # 1
        "city:IST",
        "city:BKK", # 1
        "city:TYO",
        "city:BUE", # 1    
    ]

    for city in cities:
        print(city)
        conn = sqlite3.connect('flightdatamart.db')
        if city in ["city:SPU","city:BKK","city:BUE"]:
            flights = quotes.SearchKiwi(apikey = os.environ['kiwi_api_key'], fly_to = city, max_stopovers = 1)
            flights.update_flight_table(conn = conn, date_from = date_from, date_to = date_to)
            print(city, "....finished")
        else:
            flights = quotes.SearchKiwi(apikey = os.environ['kiwi_api_key'], fly_to = city, max_stopovers = 0)
            flights.update_flight_table(conn = conn, date_from = date_from, date_to = date_to)
            print(city, "....finished")

if __name__ == "__main__":
    main()