import quotes
import os
import sqlite3

sanfran = quotes.SearchKiwi(apikey = os.environ['kiwi_api_key'], fly_to = "city:SFO", max_stopovers = 0)
conn = sqlite3.connect('flightdatamart.db')
sanfran.update_flight_table(conn = conn, date_from = "15/01/2021", date_to = "14/01/2022")