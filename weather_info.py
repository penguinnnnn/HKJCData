import csv
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


begin_year = 1975
end_year = 2021
file_name = 'weather.csv'
overwrite = True


def get_date(begin, end):
    ret = []
    begin = datetime.datetime.strptime(begin, '%Y%m%d')
    end = datetime.datetime.strptime(end, '%Y%m%d')
    while begin <= end:
        date = begin.strftime('%Y%m%d')
        ret.append(date)
        begin += datetime.timedelta(days=1)
    return ret


browser = webdriver.Chrome()
timeout = 100

header = {'DATE': 'date', 'TEMP': 'mean_temperature', 'MAX_TEMP': 'max_temperature', 'MIN_TEMP': 'min_temperature',
          'MSLP': 'pressure', 'DEW_PT': 'dew_point_temperature', 'WET_BULB': 'wet_bulb_temperature', 'RH': 'humidity',
          'CLD': 'cloud', 'RF': 'rainfall', 'GRASS': 'grass_temperature', 'SUNSHINE': 'sunshine', 'GLOBAL': 'radiation',
          'EVAPO': 'evaporation', 'PREV_DIR': 'wind_direction', 'MEAN_WIND': 'wind_speed', 'LIGHT_GROUND': 'lightning',
          'VIS_HKA': 'visibility'}

if overwrite:
    with open(file_name, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[header[k] for k in header.keys()])
        writer.writeheader()

start = time.time()

for year_index, year in enumerate(range(begin_year, end_year + 1)):
    
    dates_index = get_date('%d0101' % year, '%d1231' % year)
    info = {d: {} for d in dates_index}
    
    for ele in header.keys():
        
        if ele == 'DATE':
            for d in dates_index:
                info[d][header[ele]] = d
            continue
    
        url = 'https://www.hko.gov.hk/en/cis/dailyElement.htm?ele=%s&y=%d' % (ele, year)
        p = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/div[4]/div[1]/div[3]/table'))
        while True:
            try:
                browser.get(url)
                WebDriverWait(browser, timeout).until(p)
            except TimeoutException:
                browser.close()
                browser = webdriver.Chrome()
            else:
                break
        page = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[4]/div[1]/div[3]/table')
        
        check_year = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[4]/div[1]/h1').text
        if str(year) not in check_year:
            continue
        
        dates = page.find_elements(By.XPATH, 'tr')
        for date in range(1, len(dates)):
            months = dates[date].find_elements(By.XPATH, 'td')
            for month in range(1, len(months)):
                index = '%d%02d%02d' % (year, month, date)
                if index in dates_index:
                    info[index][header[ele]] = months[month].text
        
    with open(file_name, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=[header[k] for k in header.keys()])
        for d in dates_index:
            writer.writerow(info[d])

    end = time.time()
    print('%s. Processed %d/%d. Average %.2fs/year. %.2fs to go.' % \
          (year, (year_index + 1), end_year - begin_year + 1, (end - start) / (year_index + 1),
           (end - start) / (year_index + 1) * (end_year - begin_year - year_index)))

browser.close()

