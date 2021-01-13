import os
import requests
import json
from google.cloud import bigquery

class SearchKiwi:
    
    def __init__(self, apikey, fly_to, date_from, date_to, max_stopovers):
        self.base_url = "https://tequila-api.kiwi.com/v2/search"
        self.apikey = apikey
        self.fly_from = "city:CHI"
        self.fly_to = fly_to
        self.date_from = date_from
        self.date_to = date_to
        self.curr = "USD"
        self.max_stopovers = max_stopovers

    def get_search_results(self):
        headers = {'apikey': self.apikey}
        params = {'fly_from':self.fly_from, 'fly_to':self.fly_to,'date_from':self.date_from, 
            'date_to':self.date_to, 'curr':self.curr, 'max_stopovers':self.max_stopovers}
        response = requests.get(self.base_url, headers=headers, params=params)
        return(response.content)

def response_to_dict(response):
    data = json.loads(response.decode('utf-8'))
    return(data)

def update_flight_table(data, client, table_id):
    for row in data['data']:
        row_to_insert = [
        {u"id": row['id'], u"flyFrom": row['flyFrom'], u"flyTo": row['flyTo'],
         u"price": row['price'], u"airline": row['airline'], u"flight_no": row['flight_no'],
         u"technical_stops": row['technical_stops'], u"utc_departure": row['utc_departure'], 
         u"utc_arrival": row['utc_arrival'], u"upload_date": row['upload_date']}
        ]
        client.insert_rows_json(table_id, row_to_insert)