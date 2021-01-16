import pandas as pd
import sqlite3
import plotly.express as px

conn = sqlite3.connect('flightdatamart.db')
query = """SELECT v.City,
            ROUND(MIN(f.price),2) AS Price,
            date(f.utc_departure) AS Departure_Date
        FROM flights f
            JOIN
            vw_airport_city_country v ON f.flyTo = v.Airport
        WHERE 1 = 1 AND 
            v.City = 'San Francisco' AND 
            date(f.upload_date) = '2021-01-16'
        GROUP BY v.City,
                date(f.utc_departure)"""

df = pd.read_sql_query(query, conn)
conn.close()
fig = px.line(df, x='Departure_Date', y="Price")
fig.show()