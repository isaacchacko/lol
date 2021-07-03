# tells you what runes to run
# champ
# lane
# 4 primary runes
# 2 secondary runes
# 3 circles

# imports
import requests
from bs4 import BeautifulSoup
import lxml

# functions

def filterGrayscale(start_list):
	end_list = []
	for item in start_list:
		if 'grayscale' not in str(item):
			end_list.append(item)
	return end_list

def filterNames(start_list):
	names = []
	for item in start_list:
		item = str(item).split('alt="')[1]
		item = item.split('" class=')[0]
		names.append(item)
	return names

def findRuneBounds(rune_images):
	primary_catagory = str(rune_images[5]).split("#ffc659'&gt;")[1].split("&lt;/b&gt")[0]
	if primary_catagory == 'Precision':
		primary_bounds = (6, 19)
	if primary_catagory == 'Resolve':
		primary_bounds = (6, 18)
	if primary_catagory == 'Sorcery':
		primary_bounds = (6, 18)
	if primary_catagory == 'Domination':
		primary_bounds = (6, 20)
	if primary_catagory == 'Inspiration':
		primary_bounds = (6, 18)

	secondary_catagory = primary_bounds[1]
	secondary_catagory_start = secondary_catagory + 1
	secondary_catagory = str(rune_images[secondary_catagory]).split("#ffc659'&gt;")[1].split("&lt;/b&gt")[0]	
	if secondary_catagory == 'Precision':
		secondary_bounds = (secondary_catagory_start, secondary_catagory_start + 9)
	if secondary_catagory == 'Resolve':
		secondary_bounds = (secondary_catagory_start, secondary_catagory_start + 9)
	if secondary_catagory == 'Sorcery':
		secondary_bounds = (secondary_catagory_start, secondary_catagory_start + 9)
	if secondary_catagory == 'Domination':
		secondary_bounds = (secondary_catagory_start, secondary_catagory_start + 10)
	if secondary_catagory == 'Inspiration':
		secondary_bounds = (secondary_catagory_start, secondary_catagory_start + 9)

	return primary_bounds, secondary_bounds

def getRunes(images, bounds):
	primary_bounds, secondary_bounds = bounds

	primary_runes = all_rune_images[primary_bounds[0]:primary_bounds[1]]

	primary_runes = filterGrayscale(primary_runes)
	primary_runes = filterNames(primary_runes)
	
	secondary_runes = all_rune_images[secondary_bounds[0]:secondary_bounds[1]]

	secondary_runes = filterGrayscale(secondary_runes)
	secondary_runes = filterNames(secondary_runes)

	return primary_runes, secondary_runes

champion = input('Who are you playing as?\n')

lane_names = {'T': 'top', 'J': 'jungle', 'M':'mid', 'S':'support', 'B':'bot'}
lane = input('What lane are you playing? T, J, M, S, B\n')
if lane not in lane_names.keys():
	input("You didn't input a valid lane. Refresh the program.")

# champion = 'ahri'
lane = lane_names[lane]

url = 'https://www.op.gg/champion/' + champion + '/statistics/' + lane

print('Grabbing your runes... please wait')

page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

all_rune_images = soup.findAll('img', class_ = 'tip')

primary_runes, secondary_runes = getRunes(all_rune_images, findRuneBounds(all_rune_images))

print(f'\nShowing Runes for "{champion}" in "{lane}".\n\nPrimary Runes:')

for rune in primary_runes:
	print(rune)

print('\nSecondary Runes:')

for rune in secondary_runes:
	print(rune)

input('\n\nPress enter to exit.')