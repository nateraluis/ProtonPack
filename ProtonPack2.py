"""

Proton Pack V.2

"""

import tweepy
import botometer
import json
import time
import matplotlib.pyplot as plt
import pandas as pd


#Load the keys
with open('config/APIkey.txt') as APIkey:
    mashape_key = APIkey.read()

with open('config/mykey.json') as key:
    twitter_key = json.load(key)


botometer_api_url = 'https://botometer-pro.p.mashape.com'
bom = botometer.Botometer(botometer_api_url=botometer_api_url,
                          wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_key)

print('  ||   Proton Pack   ||\nReady to catch some bots!\n')
accountsFileTxt = input('Please type the name of the .txt file to analyse: ')
nameBots = input('Name the CSV file with the scores: ')
print('\nThank You! I will start catching those bots, see you later ;)')


accounts_file = open(accountsFileTxt, "r")
accounts = accounts_file.read().split(',')


accountsDone = 0
total_account = len(accounts)
startTime = time.time()
to_df = {}
for account in accounts:
    accountsDone +=1
    try:
        result = bom.check_account('@{}'.format(account),full_user_object=False)
        user = result['user']
        scores = result['scores']
        categories = result['categories']
        user.update(scores)
        user.update(categories)
        temp_data = {account:user}
        to_df.update(temp_data)
        print('@{} bot score: {}'.format(account, scores))
        print('Accounts: {}, elapsed time: {} s, Average time per account: {} s.'.format(accountsDone, round(time.time()-startTime,3), round((time.time()-startTime)/accountsDone,3)))
        print('Accounts to go: {}, estimate time: {} min'.format(total_account-accountsDone, round((((time.time() - startTime)/accountsDone) * (total_account - accountsDone) / 60),3) ))
        print('------ \n')

    except Exception as e:
        print ("An exception occurred with user @{}: {}".format(account, e))
        print('Accounts: {}, elapsed time: {} s, Average time per account: {} s.'.format(accountsDone, round(time.time()-startTime,3), round((time.time()-startTime)/accountsDone,3)))
        print('Accounts to go: {}, estimate time: {} min'.format(total_account-accountsDone, round((((time.time() - startTime)/accountsDone) * (total_account - accountsDone) / 60),3) ))
        print('------ \n')


df = pd.DataFrame.from_dict(to_df, orient='index')
df.sort_values('universal', ascending=False, inplace=True)
df.to_csv('salidas/CSV/{}.csv'.format(nameBots))


plt.hist(df['universal'])
plt.xlabel('% posibilidad bot')
plt.ylabel('# Cuentas')
plt.title('Distribución de cuentas')
plt.savefig('salidas/Hist/{}_DistribuciónCuentasBots.jpg'.format(nameBots),dpi=300);
