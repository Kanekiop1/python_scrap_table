import pandas as pd  # library for data analysis
import requests  # library to handle requests
from bs4 import BeautifulSoup  # library to parse HTML documents
from datetime import datetime


pd.set_option("display.max_rows", None, "display.max_columns", None)
# get the response in the form of html
wikiurl = "https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index"
table_class = "wikitable sortable jquery-tablesorter"
response = requests.get(wikiurl)
print(response.status_code)

# parse data from the html into a beautifulsoup object
soup = BeautifulSoup(response.text, 'html.parser')
indiatable = soup.find('table', {'class': "wikitable"})

df = pd.read_html(str(indiatable))
# convert list to dataframe
df = pd.DataFrame(df[0])


print(df.columns)

# Podpunkt 2

data = pd.DataFrame(df.drop(["Rank"], axis=1))

data.set_axis(['Country', 'HDI', 'Col_3'], axis=1,inplace=True)
data.pop('Col_3')
data['Population'] = 0.0
data['Area'] = 0.0
data['Gini'] = 0.0
data['Neighbours'] = 0.0
print(data.columns)
print(data)


for idx, row in data.iterrows():
    a = str.lower(data['Country'][idx])

    head, sep, tail = a.partition(' ')


    print(f"https://restcountries.eu/rest/v2/name/{head}")
    response = requests.get(f"https://restcountries.eu/rest/v2/name/{head}")
    # sprawdzamy czy odpowiedz jest rowna 200, jesli nie to znaczy, ze podany url jest bledny
    if response.status_code == 200:

        data2 = pd.read_json(f"https://restcountries.eu/rest/v2/name/{head}")

        data['Population'][idx]= float(data2['population'][0])
        data['Area'][idx] = float(data2['area'][0])
        data['Gini'][idx] = float(data2['gini'][0])
        index = pd.Index(data2['borders'][0])
        data['Neighbours'][idx] = sum(index.value_counts())
    else:
        continue

data.fillna(value=0,inplace=True)
print(data)
data.to_csv('dane.csv',index=False)

dane2 = pd.read_csv('dane.csv')
dane2.to_csv('dane.csv',index=False)

# korelacja HDI miedzy reszta
print(dane2.corrwith(dane2['HDI']))

df = pd.DataFrame( dane2.corrwith(dane2['HDI']),columns=['HDI score'])
now = datetime.now()
date_time = now.strftime("%Y-%m-%d")
dest_filename = ('%s.xlsx' % date_time)
df.to_csv(r'%s.txt' % date_time)
print(df)
