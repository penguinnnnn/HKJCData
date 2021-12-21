import random
import numpy as np
import matplotlib.pyplot as plt


fix_bet = 10

with open('data/odds.txt') as f:
    odds_data = f.read().splitlines()

X = [[float(i) for i in d.split('\t')[0].split()] for d in odds_data]
Y = [int(d.split('\t')[1]) for d in odds_data]

plt.style.use('ggplot')
plt.figure(figsize=(16, 8))
plt.title('Betting Strategy')
plt.xlabel('Race ID')
plt.ylabel('Gain')


capital = 0
plot = [0]
for x, y in zip(X, Y):
    choice = np.argmax(np.array(x))
    if choice == y:
        capital += x[choice] * fix_bet
    capital -= fix_bet
    plot.append(capital)
index = [i for i in range(len(plot))]
plt.plot(index, plot, '-', color='r', label='Highest')


# capital = 0
# plot = [0]
# for x, y in zip(X, Y):
#     c = np.array(x)
#     c[np.argmax(c)] = np.min(c)
#     choice = np.argmax(c)
#     if choice == y:
#         capital += x[choice] * fix_bet
#     capital -= fix_bet
#     plot.append(capital)
# index = [i for i in range(len(plot))]
# plt.plot(index, plot, '-', color='g', label='2nd Highest')


# capital = 0
# plot = [0]
# for x, y in zip(X, Y):
#     c = np.array(x)
#     choice1 = np.argmax(c)
#     c[np.argmax(c)] = np.min(c)
#     choice2 = np.argmax(c)
#     if choice1 == y:
#         capital += x[choice1] * fix_bet * 0.5
#     if choice2 == y:
#         capital += x[choice2] * fix_bet * 0.5
#     capital -= fix_bet
#     plot.append(capital)
# index = [i for i in range(len(plot))]
# plt.plot(index, plot, '-', color='b', label='Two Highest')


# capital = 0
# plot = [0]
# for x, y in zip(X, Y):
#     c = np.array(x)
#     c[np.argmax(c)] = np.min(c)
#     c[np.argmax(c)] = np.min(c)
#     choice = np.argmax(c)
#     if choice == y:
#         capital += x[choice] * fix_bet
#     capital -= fix_bet
#     plot.append(capital)
# index = [i for i in range(len(plot))]
# plt.plot(index, plot, '-', color='c', label='3rd Highest')


# capital = 0
# plot = [0]
# for x, y in zip(X, Y):
#     c = np.array(x)
#     c[np.argmin(c)] = np.max(c)
#     c[np.argmin(c)] = np.max(c)
#     choice = np.argmin(c)
#     if choice == y:
#         capital += x[choice] * fix_bet
#     capital -= fix_bet
#     plot.append(capital)
# index = [i for i in range(len(plot))]
# plt.plot(index, plot, '-', color='b', label='3rd Lowest')


# capital = 0
# plot = [0]
# for x, y in zip(X, Y):
#     c = np.array(x)
#     choice1 = np.argmin(c)
#     c[np.argmin(c)] = np.max(c)
#     choice2 = np.argmin(c)
#     if choice1 == y:
#         capital += x[choice1] * fix_bet * 0.5
#     if choice2 == y:
#         capital += x[choice2] * fix_bet * 0.5
#     capital -= fix_bet
#     plot.append(capital)
# index = [i for i in range(len(plot))]
# plt.plot(index, plot, '-', color='r', label='Two Lowest')


# capital = 0
# plot = [0]
# for x, y in zip(X, Y):
#     c = np.array(x)
#     c[np.argmin(c)] = np.max(c)
#     choice = np.argmin(c)
#     if choice == y:
#         capital += x[choice] * fix_bet
#     capital -= fix_bet
#     plot.append(capital)
# index = [i for i in range(len(plot))]
# plt.plot(index, plot, '-', color='g', label='2nd Lowest')


capital = 0
plot = [0]
for x, y in zip(X, Y):
    choice = np.argmin(np.array(x))
    if choice == y:
        capital += x[choice] * fix_bet
    capital -= fix_bet
    plot.append(capital)
index = [i for i in range(len(plot))]
plt.plot(index, plot, '-', color='g', label='Lowest')


random_run = []
avg_count = []
for run_index in range(100):
    print('Run random %d' % (run_index + 1))
    capital = 0
    plot = [0]
    count = 0
    for x, y in zip(X, Y):
        choice = random.randint(0, len(x) - 1)
        if choice == y:
            count += 1
            capital += x[choice] * fix_bet
        capital -= fix_bet
        plot.append(capital)
    random_run.append(plot)
    avg_count.append(count)

random_run = np.array(random_run)
random_run = np.average(random_run, axis=0)
index = [i for i in range(len(random_run))]
plt.plot(index, random_run, '-', color='b', label='Random')
print(np.average(np.array(avg_count)))


# sampling_run = []
# for run_index in range(10):
#     print('Run sampling %d' % (run_index + 1))
#     capital = 0
#     plot = [0]
#     for x, y in zip(X, Y):
#         prob = 1 / np.array(x)
#         prob = prob / np.sum(prob)
#         prob_bin = [np.sum(prob[:i + 1]) for i in range(len(prob))]
#         choice = random.random()
#         for i in range(len(prob_bin)):
#             if prob_bin[i] > choice:
#                 choice = i
#                 break
#         if choice == y:
#             capital += x[choice] * fix_bet
#         capital -= fix_bet
#         plot.append(capital)
#     sampling_run.append(plot)

# sampling_run = np.array(sampling_run)
# sampling_run = np.average(sampling_run, axis=0)
# index = [i for i in range(len(sampling_run))]
# plt.plot(index, sampling_run, '-', color='g', label='Sampling')


plt.legend()
plt.savefig('results/my.png')

