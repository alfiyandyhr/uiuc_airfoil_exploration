# Downloads all airfoils from the UIUC database
# (https://m-selig.ae.illinois.edu/ads/coord_database.html)
# written by @alfiyandyhr

from bs4 import BeautifulSoup
import re

try:
	import urllib.request as urllib2
except:
	import urllib2

# Base filepath
base_filept = 'https://m-selig.ae.illinois.edu/ads/'

# Open the webpage
html_page = urllib2.urlopen('https://m-selig.ae.illinois.edu/ads/coord_database.html')
soup = BeautifulSoup(html_page, 'lxml')

# Loop over airfoil .dat files and save each
ind = 1
airfoil_names = []
for link in soup.find_all('a', attrs={'href': re.compile('\.dat', re.IGNORECASE)}):
	airfoil_names.append(link.get('href').rsplit('/',1)[-1])
	urllib2.urlretrieve(base_filept+link.get('href'), 'data/'+link.get('href').rsplit('/',1)[-1])
	print(f'Saving airfoil {ind} ...')
	ind = ind + 1

with open('airfoil_names.txt', 'w') as f:
	for ind in range(len(airfoil_names)):
		f.write(f'{airfoil_names[ind]}\n')