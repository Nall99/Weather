import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import requests

def get_weather_data(location):
	url = f"https://www.google.com/search?q=weather+{location.replace(' ','')}"
	session = requests.Session()
	session.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
	html = session.get(url)

	soup = bs(html.text, 'html.parser')
	name = soup.find('span', attrs= {'class': 'BBwThe'}).text
	time = soup.find('div', attrs= {'id': 'wob_dts'}).text
	weather = soup.find('span', attrs= {'id': 'wob_dc'}).text
	temp = soup.find('span', attrs= {'id': 'wob_tm'}).text

	return name, time, weather, temp

sg.theme('reddit')
info_col = sg.Column([
	[sg.Text('',key = 'location', font = 'Calibri 30', background_color='#FF0000', pad = 0, visible= False)],
	[sg.Text('',key = 'time', font = 'Calibri 16', background_color= '#000000', text_color="#FFFFFF", pad = 0, visible= False)],
	[sg.Text('',key = 'temp', font = 'Calibri 16', background_color= '#FFFFFF', pad = (0,10), text_color= '#000000', justification = 'center', visible = False)]
])
layout = [
	[sg.Input(expand_x= True, key='input'),sg.Button('Enter')],
	[info_col]
]

window = sg.Window('Weather', layout)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break

	if event == 'Enter':
		name, time, weather, temp = get_weather_data(values['input'])
		window['location'].update(name,visible = True)
		window['temp'].update(f'{temp} \u2103 ({weather})',visible = True)
		window['time'].update(time.split(' ')[0],visible = True)

window.close()
