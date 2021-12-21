import csv
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


begin_date = '19790922'
end_date = '20211231'
file_name = 'race_info.csv'
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


dates = get_date(begin_date, end_date)
browser = webdriver.Chrome()
timeout = 100

header = ['race_date', 'race_place', 'race_id_of_day', 'race_id_of_season', 'horse_class', 'race_distance',
          'race_name', 'race_price', 'going', 'course']
for i in range(1, 21):
    header += ['horse_%s_place' % i, 'horse_%s_name' % i, 'horse_%s_id' % i, 'horse_%s_jockey' % i, 'horse_%s_trainer' % i,
               'horse_%s_act_wt' % i, 'horse_%s_dec_wt' % i, 'horse_%s_dr' % i, 'horse_%s_lbw' % i, 'horse_%s_pos' % i,
               'horse_%s_time' % i, 'horse_%s_odds' % i]

if overwrite:
    with open(file_name, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

count = 0
start = time.time()
for date_index, date in enumerate(dates):
    
    url = 'https://racing.hkjc.com/racing/info/meeting/Results/English/Local/%s' % (date)
    element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]'))
    while True:
        try:
            browser.get(url)
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            browser.close()
            browser = webdriver.Chrome()
        else:
            break
    page = browser.find_element_by_xpath('/html/body/div[1]')
    
    find_result = page.find_elements(By.XPATH, 'div[1]/div[2]/div[1]')
    if len(find_result) > 0:
        if find_result[0].text == 'No information.':
            continue
    
    find_result = page.find_elements(By.XPATH, 'div[3]/p[1]/span[1]')
    if len(find_result) == 0:
        continue
    if find_result[0].text.find('Sha Tin') > 0:
        race_place = 'ST'
    elif find_result[0].text.find('Happy') > 0:
        race_place = 'HV'
    elif find_result[0].text.find('Conghua') > 0:
        race_place = 'CH'
    else:
        raise NotImplementedError
    
    if find_result[0].text.split('/')[2][:4] + find_result[0].text.split('/')[1] + \
       find_result[0].text.split('/')[0][-2:] != date:
        continue
    
    number_of_race = len(page.find_elements(By.XPATH, 'div[2]/table/tbody/tr[1]/td')) - 2
    for i in range(1, number_of_race + 1):
        
        url = 'https://racing.hkjc.com/racing/info/meeting/Results/English/Local/%s/%s/%d' % (date, race_place, i)
        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[5]'))
        while True:
            try:
                browser.get(url)
                WebDriverWait(browser, timeout).until(element_present)
            except TimeoutException:
                browser.close()
                browser = webdriver.Chrome()
            else:
                break
        page = browser.find_element_by_xpath('/html/body/div[1]')

        if page.find_element(By.XPATH, 'div[4]').text.split()[0] in ['Information', 'This']:
            continue
        
        single_info = {}
        single_info['race_date'] = date
        single_info['race_place'] = race_place
        find_result = page.find_element(By.XPATH, 'div[4]/table[1]/thead[1]/tr[1]/td[1]').text.split()
        single_info['race_id_of_day'] = find_result[1]
        single_info['race_id_of_season'] = find_result[2][1:-1]
        if single_info['race_id_of_season'] == '0':
            continue
        
        find_results = page.find_elements(By.XPATH, 'div[4]/table[1]/tbody/tr')
        find_result = find_results[1].find_element(By.XPATH, 'td[1]').text.split(' - ')
        single_info['horse_class'] = find_result[0]
        single_info['race_distance'] = find_result[1][:-1]
        single_info['race_name'] = find_results[2].find_element(By.XPATH, 'td[1]').text
        single_info['race_price'] = find_results[3].find_element(By.XPATH, 'td[1]').text
        
        single_info['going'] = find_results[1].find_element(By.XPATH, 'td[3]').text
        single_info['course'] = find_results[2].find_element(By.XPATH, 'td[3]').text
        
        horse_record = page.find_elements(By.XPATH, 'div[5]/table/tbody/tr')
        record_info = [abbr.text for abbr in page.find_elements(By.XPATH, 'div[5]/table/thead/tr/td')]
        record_info_index = {abbr: index for index, abbr in enumerate(record_info)}
        substitute = len(horse_record) + 1
        for j in range(len(horse_record)):
            
            find_result = horse_record[j].find_elements(By.XPATH, 'td')
            horse_no = find_result[1].text
            if horse_no == '':
                horse_no = str(substitute)
                substitute += 1
            
            single_info['horse_%s_place' % horse_no] = find_result[0].text
            single_info['horse_%s_name' % horse_no] = find_result[2].text.split('(')[0]
            single_info['horse_%s_id' % horse_no] = find_result[2].text.split('(')[-1][:-1]
            if 'Jockey' in record_info:
                single_info['horse_%s_jockey' % horse_no] = find_result[record_info_index['Jockey']].text
            if 'Trainer' in record_info:
                single_info['horse_%s_trainer' % horse_no] = find_result[record_info_index['Trainer']].text
            if 'Act. Wt.' in record_info:
                single_info['horse_%s_act_wt' % horse_no] = find_result[record_info_index['Act. Wt.']].text
            if 'Declar. Horse Wt.' in record_info:
                single_info['horse_%s_dec_wt' % horse_no] = find_result[record_info_index['Declar. Horse Wt.']].text
            if 'Dr.' in record_info:
                single_info['horse_%s_dr' % horse_no] = find_result[record_info_index['Dr.']].text
            if 'LBW' in record_info:
                single_info['horse_%s_lbw' % horse_no] = find_result[record_info_index['LBW']].text
                if single_info['horse_%s_lbw' % horse_no] == '-':
                    single_info['horse_%s_lbw' % horse_no] = '0'
            if 'Running\nPosition' in record_info:
                single_info['horse_%s_pos' % horse_no] = find_result[record_info_index['Running\nPosition']].text
            if 'Finish Time' in record_info:
                single_info['horse_%s_time' % horse_no] = find_result[record_info_index['Finish Time']].text
            if 'Win Odds' in record_info:
                single_info['horse_%s_odds' % horse_no] = find_result[record_info_index['Win Odds']].text
        
        with open(file_name, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writerow(single_info)
    
    count += 1
    end = time.time()
    print('%s. Processed %d/%d. Average %.2fs/date. %.2fs to go.' % \
          (date, count, count / (date_index + 1) * len(dates), (end - start) / count,
           (end - start) * (len(dates) - date_index - 1) / (date_index + 1)))

browser.close()

