#Analyze match data from quiet mode

f = open('output.txt', 'r')
bot_wins = 0
number_of_fights = 0
for line in f:
    if "1 1" in line:
        bot_wins += 1
    if ".hlt" in line:
        number_of_fights += 1
print(bot_wins, " / ", number_of_fights)
print("bot wins %.2f percent of the time" % (bot_wins/number_of_fights*100))
