
import os
os.chdir("C:\\Datos")
os.getcwd()
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
#Carrega de configuracio
ipMinemeld = config['config']['Ip_Minemeld']
ipASR = config['config']['Ip_ASR']
usuariASR = config['config']['User_ASR']
passASR = config['config']['Password_ASR']
timeBan = config['config']['timeBan']

print ("Config Carregada")
#Carrega de les ips anteriors
import csv
f= open("ips.csv")
reader = csv.reader(f,  delimiter=',')
ipBanned = []
ipBanned_llista = []
for row in reader:
    ipBanned.append([row[0], row[1], row[2]])
    ipBanned_llista.append(row[0])
print ("Ips Carregades")

#Eliminacio de ips caducades
from datetime import date
from datetime import datetime
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%d/%m/%Y")
    d2 = datetime.strptime(d2, "%d/%m/%Y")
    return abs((d2 - d1).days)
today = date.today()
index = 0 
for ip in ipBanned:
    if days_between(today.strftime("%d/%m/%Y") ,ip[1]) > int(timeBan):
        ipBanned.pop(index)
    index += 1


#Descarrega de ip de minemeld
import wget
import ssl

## Codi per ignorar el certificat invalid de minemeld
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

url = "https://" + ipMinemeld + "/feeds/malcode5-Output-STIC"
wget.download(url, 'ipsMinemeld.txt')

print ("Ips descarregades")
