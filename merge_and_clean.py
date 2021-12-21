import csv

race_files = ['data/raw/race_info_75s.csv', 'data/raw/race_info_80s.csv', 'data/raw/race_info_85s.csv',
              'data/raw/race_info_90s.csv', 'data/raw/race_info_95s.csv', 'data/raw/race_info_00s.csv',
              'data/raw/race_info_05s.csv', 'data/raw/race_info_10s.csv', 'data/raw/race_info_15s.csv',
              'data/raw/race_info_20s.csv']
weather_file = 'data/raw/weather.csv'

going_map = {'FIRM': 0, 'GOOD TO FIRM': 1, 'GOOD': 2, 'GOOD TO YIELDING': 3, 'YIELDING': 4, 'YIELDING TO SOFT': 5,
             'SOFT TO YIELDING': 6, 'SOFT': 6, 'HEAVY': 8, 'WET FAST': 0, 'FAST': 1, 'SLOW': 4, 'WET SLOW': 6,
             'NORMAL WATERING': 8, 'RAIN AFFECTED': 8}

class_map = {'Class 1': 1, 'Class 2': 2, 'Class 3': 3, 'Class 4': 4, 'Class 5': 5, 'Class 6': 6, 'Class 7': 7, 'Group One': 1, 'Hong Kong Group One': 1, 'Class 2 (Bonus Prize Money)': 2, 'GROUP-2': 2, 'Group Two': 2, 'Hong Kong Group Two': 2, 'Class 3 (Bonus Prize Money)': 3, 'Class 3 (Special Condition)': 3, 'GROUP-3': 3, 'Group Three': 3, 'Hong Kong Group Three': 3, 'Class 4 (Bonus Prize Money)': 4, 'Class 4 (Special Condition)': 4, 'Class 4 (Restricted)': 4, 'GROUP-4': 4, 'Race Class 6': 6, 'CLASS 7' : 7, 'CLASSES 1 & 2': 1.5, 'CLASSES 2 & 3': 2.5, 'CLASSES 3 & 4': 3.5, 'CLASSES 4 & 5': 4.5, 'CLASSES 5 & 6': 5.5, 'CLASSES 6 & 7': 6.5, }

race_info = []
for f in race_files:
    with open(f) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            race_info.append(row)

count = int(race_info[0]['race_id_of_season'])
for race in race_info[1:]:
    if int(race['race_id_of_season']) != count + 1 and int(race['race_id_of_season']) != 1:
        print('%s No. %s' % (race['race_date'], race['race_id_of_day']))
    count = int(race['race_id_of_season'])

count = 0
for i, race in enumerate(race_info):
    race['going'] = str(going_map[race['going']])
    if race['horse_class'] in class_map.keys():
        race['horse_class'] = class_map[race['horse_class']]
    elif 'PRIVATE PURCHASE' in race['horse_class'] or 'IMPORTS' in race['horse_class']:
        race['horse_class'] = str(0)
    elif race['horse_class'] in ['Restricted Race', 'OPEN', 'MAIDEN', 'Premier Class', '1992 SG or PPG']:
        race['horse_class'] = str(0)
    elif 'Griffin' in race['horse_class'] or 'GRIFFINS' in race['horse_class']:
        race['horse_class'] = str(0)
    else: count += 1
print('%d/%d' % (count, len(race_info)))

classes = [race['horse_class'] for race in race_info]
classes = list(set(classes))
print(classes)

# odds_dataset = []
# for race in race_info:
#     X = []
#     Y = 0
#     for i in range(1, 21):
#         if race['horse_%s_odds' % i] in ['', '---']:
#             continue
#         X.append(race['horse_%s_odds' % i])
#         if race['horse_%s_place' % i] == '1':
#             Y = i - 1
#     odds_dataset.append('%s\t%d' % (' '.join(X), Y))
# with open('data/odds.txt', 'w') as f:
#     f.write('\n'.join(odds_dataset))

# going = [race['going'] for race in race_info]
# going = list(set(going))
# print(going)

# course = [race['course'] for race in race_info]
# course = list(set(course))
# print(course)

# weather_info = {}
# with open(weather_file) as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         weather_info[row['date']] = row

# for race in race_info:
    
