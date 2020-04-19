import pandas as pd
import time
import sys

from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup


url = 'https://esriksa-emapstc.maps.arcgis.com/apps/opsdashboard/index.html#/6cd8cdcc73ab43939709e12c19b64a19'
sys.stdout.write('\r1%  ')
sys.stdout.flush()

driver = webdriver.Chrome('./chromedriver')

sys.stdout.write('\r5%  ')
sys.stdout.flush()

driver.get(url)

for i in range(0, 9):
    time.sleep(0.6) # Waiting for the page to fully load
    sys.stdout.write('\r{}%  '.format(i*10 + 10))
    sys.stdout.flush()


soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# The commented lines used to work when last updated status was displayed on the website 

# update_time = soup.find_all('g', class_="responsive-text-label")[5].svg.text.strip('\n')
# update_time = datetime.strptime(update_time, '%m/%d/%Y, %I:%M %p')

feature_list = soup.find_all('nav', class_='feature-list')

# Date Format is "day-month" e.g "Apr 5"
update_time = datetime.strftime(datetime.now() - timedelta(1), '%b %d')

'''
# Used to work before, but the HTML changed on april 9
all_stat = []
for feature in feature_list:
    stat = {}
    for p in feature.find_all('p'):
        strong = p.find_all('strong')
        try:
            print(strong[0].text)
            stat[strong[0].text.strip(': ').strip('\u200e')] = int(strong[1].text)
        except IndexError:
            print(strong[0].text)
    all_stat.append(stat)
'''

all_stat = []

for feature in feature_list:
    stat = {}
    for p in feature.find_all('p'):
        strong = p.find_all('strong')
        s = strong[0].text.split(' :')
        s[0] = s[0].strip().replace(',', '')
        stat[s[1].strip('\u200e')] = int(s[0])

    all_stat.append(stat)


# ## Writing the new update into Dataframes
total_df = pd.DataFrame.from_dict(all_stat[0], orient='index').reset_index()
total_df.columns = ['City', 'Total Cases']
active_df = pd.DataFrame.from_dict(all_stat[1], orient='index', columns=['Active Cases']).reset_index()
active_df.columns = ['City', 'Active Cases']
recovered_df = pd.DataFrame.from_dict(all_stat[2], orient='index', columns=['Recovered Cases']).reset_index()
recovered_df.columns = ['City', 'Recovered Cases']


# Merging the new updates into one Dataframe
new_update = pd.merge(pd.merge(total_df, active_df, how='outer'), recovered_df, how='outer')
new_update['date'] = update_time
new_update = new_update.fillna(0)

# ## Reading the old data files and appending the new changes
daily_changes = pd.read_excel('last_update.xlsx', sheet_name='Daily Changes', parse_dates=['date'])
daily_changes = daily_changes.append(new_update, ignore_index=True)

writer = pd.ExcelWriter('last_update.xlsx')
daily_changes.to_excel(writer, 'Daily Changes', index=False)

# ## Merging Total Cases,	Active Cases, and Recovered Cases in Individual sheets
total_df = pd.DataFrame.from_dict(all_stat[0], orient='index').reset_index()
total_df.columns = ['City', 'Total Cases {}'.format(update_time)]
active_df = pd.DataFrame.from_dict(all_stat[1], orient='index', columns=['Active Cases']).reset_index()
active_df.columns = ['City', 'Active Cases {}'.format(update_time)]
recovered_df = pd.DataFrame.from_dict(all_stat[2], orient='index', columns=['Recovered Cases']).reset_index()
recovered_df.columns = ['City', 'Recovered Cases {}'.format(update_time)]
new_update = pd.merge(pd.merge(total_df, active_df, how='outer'), recovered_df, how='outer')
new_update = new_update.fillna(0)
new_update['Death Cases {}'.format(update_time)] = new_update['Total Cases {}'.format(update_time)] - (new_update['Recovered Cases {}'.format(update_time)] + new_update['Active Cases {}'.format(update_time)])

death_df = new_update[['City', 'Death Cases {}'.format(update_time)]]

total_df.columns = ['City', '{}'.format(update_time)]
active_df.columns = ['City', '{}'.format(update_time)]
recovered_df.columns = ['City', '{}'.format(update_time)]
death_df.columns = ['City', '{}'.format(update_time)]

# Reading the previous update
last_all_cases = pd.read_excel('last_update.xlsx', sheet_name='Infected')
last_active_cases = pd.read_excel('last_update.xlsx', sheet_name='Active Cases')
last_recovered_cases = pd.read_excel('last_update.xlsx', sheet_name='Recovered')
last_death_cases = pd.read_excel('last_update.xlsx', sheet_name='Deaths')

update_all_cases = pd.merge(last_all_cases, total_df, how='outer', on='City')
update_active_cases = pd.merge(last_active_cases, active_df, how='outer', on='City')
update_recovered_cases = pd.merge(last_recovered_cases, recovered_df, how='outer', on='City')
update_death_cases = pd.merge(last_death_cases, death_df, how='outer', on='City')

update_all_cases = update_all_cases.fillna(0)
update_active_cases = update_active_cases.fillna(0)
update_recovered_cases = update_recovered_cases.fillna(0)
update_death_cases = update_death_cases.fillna(0)

update_all_cases.to_excel(writer, 'Infected', index=False)
update_active_cases.to_excel(writer, 'Active Cases', index=False)
update_recovered_cases.to_excel(writer, 'Recovered', index=False)
update_death_cases.to_excel(writer, 'Deaths', index=False)


last_all_cases_changes = pd.read_excel('last_update.xlsx', sheet_name='Infected Daily')
last_active_cases_changes = pd.read_excel('last_update.xlsx', sheet_name='Active Cases Changes')
last_recovered_cases_changes = pd.read_excel('last_update.xlsx', sheet_name='Recovered Daily')
last_death_cases_changes = pd.read_excel('last_update.xlsx', sheet_name='Death Daily')

update_all_cases['{}'.format(update_time)] = update_all_cases[update_all_cases.columns[-1]] - update_all_cases[update_all_cases.columns[-2]]
update_active_cases['{}'.format(update_time)] = update_active_cases[update_active_cases.columns[-1]] - update_active_cases[update_active_cases.columns[-2]]
update_recovered_cases['{}'.format(update_time)] = update_recovered_cases[update_recovered_cases.columns[-1]] - update_recovered_cases[update_recovered_cases.columns[-2]]
update_death_cases['{}'.format(update_time)] = update_death_cases[update_death_cases.columns[-1]] - update_death_cases[update_death_cases.columns[-2]]

update_all_cases_changes = pd.merge(last_all_cases_changes, update_all_cases[['{}'.format(update_time), 'City']], how='outer', on='City')
update_active_cases_changes = pd.merge(last_active_cases_changes, update_active_cases[['{}'.format(update_time), 'City']], how='outer', on='City')
update_recovered_cases_changes = pd.merge(last_recovered_cases_changes, update_recovered_cases[['{}'.format(update_time), 'City']], how='outer', on='City')
update_death_cases_changes = pd.merge(last_death_cases_changes, update_death_cases[['{}'.format(update_time), 'City']], how='outer', on='City')

update_all_cases_changes.to_excel(writer, 'Infected Daily', index=False)
update_active_cases_changes.to_excel(writer, 'Active Cases Changes', index=False)
update_recovered_cases_changes.to_excel(writer, 'Recovered Daily', index=False)
update_death_cases_changes.to_excel(writer, 'Death Daily', index=False)

writer.save()

sys.stdout.write('\r100% ')
sys.stdout.flush()
sys.stdout.write('\n')
sys.stdout.write('Finished Scraping, the file last_update.xlsx has been updated.')
sys.stdout.flush()
