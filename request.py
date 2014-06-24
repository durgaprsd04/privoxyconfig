from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import csv
import gspread
import time
import rfc3987
import getpass

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    if(file1['title'] == 'Responses'):
        docid = file1['id']

print "Enter Username and Password of User logged in earlier"
username = raw_input("Username:")
password = getpass.getpass()
print (time.strftime("%d/%m/%Y"))
client = gspread.login(username, password)
spreadsheet = client.open_by_key(docid)
for i, worksheet in enumerate(spreadsheet.worksheets()):
    filename = 'response-worksheet' + str(i) + '.csv'
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(worksheet.get_all_values())
maxval = i
i = 0
fp = open("user.action", 'a')
print "There is", i+1, "worksheets created."
print "Additions can be seen on the later ones"
for i in range(0, maxval+1):
    with open('response-worksheet'+str(i)+'.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            valid = True
            url = row[1]
            try:
                rfc3987.parse(url, rule="IRI")
            except Exception as e:
                valid = False
            if valid:
                fp.write("www."+row[1].split('/')[2]+"\n")
fp.close()
fp1 = open("user.action.old", 'r')
fp2 = open("user.action", 'r')
fp1.seek(0, 2)
fp2.seek(fp1.tell(), 0)
fp3 = open("tempuser.action", 'w')
for line in fp2:
    fp3.write(line)
fp3.close()
fp3 = open("tempuser.action", 'r')

print "List of URL's going to be appended"
line = fp3.readlines()
fp3.seek(0, 0)
for i, urls in enumerate(fp3):
    print i, ":", urls
print "Enter the items to be removed separated by comas"
print "Or you could delete any urls you want in"
print "tmpuser.action file in the folder"
print "And proceed by typing yes"
fp3.close()
choice = raw_input("choices:")
choices = choice.split(',')
for ch in choices:
    try:
        del line[int(ch)-1]
    except Exception as e:
        pass
fp = open("tempuser.action", 'w')
for l in line:
    fp.write(l)
fp.close()
print "Writing changes to file....."
try:
    fp = open("/etc/privoxy/user.action", 'a')
    fp1 = open("user.action", 'r')
    for lines in fp1:
        fp.write(lines)
    fp.close()
    fp1.close()
except Exception as e:
    print "Something wicked happened"
    exit("Permission denied")
    pass
print "Done"
with open("user.action", 'r') as f1:
    with open("user.action.old", 'w') as f2:
        for u in f1:
            f2.write(u)
f1.close()
f2.close()
f1 = open("user.action", 'w')
f1.close()
# fp = open("response-worksheet"+str(i)+".csv",'r')
