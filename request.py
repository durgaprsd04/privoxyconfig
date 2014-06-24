from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from email.utils import parseaddr
import csv
import gspread
import time
import rfc3987
import getpass
import csv
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
	if(file1['title'] == 'Responses'):
		docid=file1['id']

print "Enter Username and Password of User logged in earlier"
#username = raw_input("Username:")
#password = getpass.getpass()
username="username@gmail.com"
password="password"
print (time.strftime("%d/%m/%Y"))

client = gspread.login(username, password)
spreadsheet = client.open_by_key(docid)
for i, worksheet in enumerate(spreadsheet.worksheets()):
    filename = 'response' + '-worksheet' + str(i) + '.csv'
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(worksheet.get_all_values())
max=i
i=0
fp = open("user.action",'a')
print "There is",i+1,"worksheets created."
print "Additions can be seen on the later ones"
#for i in range(0,max):
with open('response-worksheet0.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	valid = True

        url=row[1]
        print url
        i=i+1
        if i>1:
        	try:
        		rfc3987.parse(url,rule="IRI")
        	except Exception as e:
        		valid = False
        	if valid:
        		fp.write(row[1].split('/')[2]+"\n")




#fp = open("response-worksheet"+str(i)+".csv",'r')
