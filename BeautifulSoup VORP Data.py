# Extract VORP data from bball reference using Beautiful Soup

from bs4 import BeautifulSoup
from urllib.request import urlopen
import openpyxl
import re
import warnings

warnings.filterwarnings("ignore")
# bball reference URLS
# VORP_url = 'http://www.basketball-reference.com/leagues/NBA_2016_advanced.html'
# playerID_url = 'http://www.basketball-reference.com/players/b/banksma01.html'

# Gather data between these seasons
begDate = 2011
endDate = 2016

# Load data to this workbook. Change the location/name to whever you put the file
wb = openpyxl.load_workbook(
    'C:\\Users\Jasper\Documents\Basketball Blog Material\Posts\Jasper - Web Scraping\VORP Data.xlsx')
# We will dump our data into the sheet called 'VORP'
VORP = wb.get_sheet_by_name('VORP')


# grab all links within the "full_table" section
def get_VORP(season):
    # Get advanced stats for all players for the given season and store them in Excel
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(season) + '_advanced.html'
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find_all('tr', {'class': 'full_table'})
    tdcount = len(rows[1].findAll('td'))
    aCount = len(rows[1].findAll('a'))
    rowCount = 1

    # for every table row, get each TD
    for row in range(0, len(rows) - 1):
        rowCount += 1
        columnCount = 3
        VORP.cell(row=rowCount, column=1).value = season
        for td in range(1, tdcount):  # no need to start from 0 because 0 is Rk
            VORP.cell(row=rowCount, column=columnCount).value = rows[row].findAll('td')[td].text
            columnCount += 1

    # this part is for finding the player ID in a 'href'. Use regex to eliminate the noise. From '/players/a/acyqu01.html', just return acyqu01
    p = re.compile('\/([^\/\?]+)\.')
    rowCount = 1

    for row in range(0, len(rows) - 1):
        rowCount += 1
        columnCount = 2
        balls = rows[row].findAll('a')[0].get('href')
        VORP.cell(row=rowCount, column=columnCount).value = re.search(p, balls).group(1)

    wb.save('C:\\Users\Jasper\Documents\Basketball Blog Material\Posts\Jasper - Web Scraping\VORP Data.xlsx')


#for year in range(begDate, endDate):
#    get_VORP(year)

get_VORP(endDate)


# TODO: For every distinct playerID in Excel sheet, pull his draft and salary information from bball reference for that specific season and copy to Excel
