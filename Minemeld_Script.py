import os
os.chdir("./Datos")
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
    if row:
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


#Carrega de les ip del minemeld
with open('ipsMinemeld.txt') as fp:
   line = fp.readline() #primera linea de minemeld buida
   line = fp.readline()
   cnt = 1
   while line:
       
       if line in ipBanned_llista:
           findip = ipBanned_llista.index(line)

           ipBanned[findip][1] = today.strftime("%d/%m/%Y")
       else:
            ipBanned.append([line.rstrip(' \n'),today.strftime("%d/%m/%Y"),timeBan])
       line = fp.readline()
       cnt += 1


with open('ips.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for ip in ipBanned:
        spamwriter.writerow(ip)


from os import remove
remove('ipsMinemeld.txt')

print ("Llista ips actualitzada")

import paramiko

connexio = paramiko.Transport(ipASR,22)
connexio.connect(username = usuariASR, password = passASR)

canal = connexio.open_session()
canal.exec_command('enable')
canal.exec_command('conf t')

canal.exec_command('no access-list 100')
for ip in ipBanned_llista:
    comanda = "access-list 100 deny host " + ip
    canal.exec_command(comanda)
salida = canal.makefile('rb', -1).readlines()
if salida:
    print (salida)
else:
    print (canal.makefile_stderr('rb', -1).readlines())
connexio.close()
