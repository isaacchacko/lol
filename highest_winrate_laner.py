import requests
from bs4 import BeautifulSoup
import lxml
import json


url = 'http://www.op.gg/champion/statistics'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

# ADC, JUNGLE, MID, SUPPORT, TOP
lane = 'SUPPORT'
bot_laners = str(soup.findAll('div', class_ = f'champion-index__champion-item--{lane}')).split('data-champion-key="')

bot_laner_names = []

for laner in bot_laners:
	if '" data-champion-name="' in laner:
		bot_laner_names.append(laner.split('" data-champion-name="')[0])


bot_lane_winrates = {}

for laner in bot_laner_names:
	print(f'currently finding the winrate for {laner}...')
	if lane == 'JUNGLE': lane = 'jg'
	if lane == 'ADC': lane = 'adc'
	if lane == 'MID': lane = 'mid'
	if lane == 'TOP': lane = 'top'
	if lane == 'SUPPORT':lane = 'support'
	url = f'http://www.op.gg/champion/{laner}/statistics/{lane}'

	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'lxml')

	bot_lane_winrates[laner] = float(str(soup.find('div', class_ = 'champion-stats-trend-rate').text).replace('%','').strip())

print()
print('WINRATES IN BOTLANE (HIGHEST TO LOWEST):')
while len(bot_lane_winrates) != 0:
	highest = list(bot_lane_winrates.keys())[0]

	for laner, winrate in bot_lane_winrates.items():
		if winrate > bot_lane_winrates[highest]:
			highest = laner

	print(highest)
	print(str(bot_lane_winrates[highest]) + '%')
	print()
	bot_lane_winrates.pop(highest)