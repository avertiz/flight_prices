import os
import requests
import json
import sqlite3
import time
import copy
from datetime import datetime, timedelta

class SearchKiwi:
    
    def __init__(self, apikey, fly_to, max_stopovers):
        self.base_url = "https://tequila-api.kiwi.com/v2/search"
        self.apikey = apikey
        self.fly_from = "city:CHI"
        self.fly_to = fly_to
        self.curr = "USD"
        self.max_stopovers = max_stopovers

    @staticmethod
    def response_to_dict(response):
        data = json.loads(response.decode('utf-8'))
        return(data)

    def get_search_results(self, date_from, date_to):
        headers = {'apikey': self.apikey}
        params = {'fly_from':self.fly_from, 'fly_to':self.fly_to,'date_from':date_from, 
            'date_to':date_to, 'curr':self.curr, 'max_stopovers':self.max_stopovers}
        response = requests.get(self.base_url, headers=headers, params=params)
        data = SearchKiwi.response_to_dict(response = response.content)
        return(data)

    def update_flight_table(self, conn, date_from, date_to):        
        date_from = datetime.strptime(date_from, "%d/%m/%Y")
        date_to = datetime.strptime(date_to, "%d/%m/%Y")
        date_to_copy = copy.copy(date_to)
        cursor = conn.cursor()     
        while date_from < date_to_copy:
            date_to = date_from + timedelta(days=30)            
            print(date_from, date_to)
            time.sleep(.61)
            data = self.get_search_results(date_from = date_from.strftime("%d/%m/%Y"), date_to = date_to.strftime("%d/%m/%Y"))
            if len(data['data']) == 0:
                date_from = date_from + timedelta(days=30)
            for row in data['data']:
                if date_from < datetime.strptime(row['utc_departure'], "%Y-%m-%dT%H:%M:%S.%fZ"):
                    date_from = datetime.strptime(row['utc_departure'], "%Y-%m-%dT%H:%M:%S.%fZ")
                insert_query =  """INSERT INTO flights
                                (id, flyFrom, flyTo, price, airline, flight_no, technical_stops, utc_departure, utc_arrival, upload_date)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """
                cursor.execute(insert_query, (row['id'],
                                            row['flyFrom'],
                                            row['flyTo'],
                                            float(row['price']),
                                            row['route'][0]['airline'],
                                            row['route'][0]['flight_no'],
                                            int(row['technical_stops']),
                                            datetime.strptime(row['utc_departure'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                                            datetime.strptime(row['utc_arrival'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                                            datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                                            )
                )
                conn.commit()
            date_from = date_from + timedelta(days=1)
        conn.close()