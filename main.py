from smtplib import SMTP
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import threading
from time import sleep, thread_time
import time
import signal

def handler(signum, frame):
        raise Exception(TimeoutError)
############## Check mail function #################
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
# Define a function for
# for validating an Email
def check_mail(email):
    # pass the regular expression
    # and the string in search() method
    if(re.match(regex, email)):
        return True
    else:
        return False
############## /Check mail function #################
def scan_result():
                #clear command line 
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')
                #print status
                print("Generating white_list.txt \n" + str(int((len(success_mails) + len(fail_mails))/(len(mails))* 100))+" % \n" + str(counter) + " mails tried \n" +"\033[1;32;40m"+"sent : " + str(len(success_mails)) + " mails \n" + '\033[91m' + "fails : " +str(len(fail_mails)) + " mails \n"  +'\033[0m' + "total : " + str(len(mails)) + " mails" )

def send_scan_mail(mail,fail_mails,success_mails,white_list,generate_white_list_log):
                host = mail['host']
                port = mail['port']
                username = mail['username']
                password = mail['password']
                mailto = test_mail
                message = "Test mail " + username
                try:
                    #send mail
                    msg = MIMEMultipart()
                    body_part = MIMEText('mail_body', 'plain')
                    msg['Subject'] = 'mail_subject'
                    msg['From'] = username
                    msg['To'] = mailto
                    mail_server = smtplib.SMTP(host,port)
                    mail_server.starttls()
                    mail_server.login(username,password)
                    mail_server.sendmail(username,mailto,msg.as_string())
                    # print( "mail sent with " + mail['username'] + " address")
                    mail_server.close()
                    #if mail sent successfully
                    success_mails.append(mail)
                    mail['status'] = 'success'
                except Exception as e:
                    # print('\033[91m' + str(e) + " address"+'\033[0m' )
                    #if mail failed
                    fail_mails.append(mail)
                    mail['status'] = 'failed'
                    mail['fail_reason'] = str(e)
                finally:
                    #log mail 
                    generate_white_list_log.write("\n"+str(mail))
                    # white_list.write("\n"+str(mail))
                    #if mail success add it to white_list.txt
                    if mail['status'] == 'success':
                            white_list.write(str(mail['host'])+":"+str(mail['port'])+","+str(mail['username'])+","+str(mail['password'])+"\n")
                scan_result()   




# Create or find generate_white_list_log.txt file
generate_white_list_log = open("generate_white_list_log.txt", "w")
# Create or find generate_white_list_log.txt file
send_mail_log = open("send_mail_log.txt", "w")
# arrays for total mail, success mails, failed mails
success_mails = []
fail_mails = []
mails = []
sender_mails = []
receiver_mails = []
# show message
print("Welcome\n")
# choose step 
step = input("1-Scan my sender list and generate white list \n2-I have white list, lets send mails\nChoose (Enter = 1)? ")
# if user type 1 or press enter
if step == "" or step == '1':
    # find or create white_list.txt
    white_list = open("white_list.txt", "w")
    # make sure user has imported sender_list.txt
    some = input("\nput your list in `sender_list.txt` file then press enter to continue:")
    # mail for testing list
    test_mail = input("\ntest mail address : ")
    #if user inputed true mail address
    if(check_mail(test_mail)):
        try:
            # open sender_list.txt
            file = open("sender_list.txt", "r").read()
            file = file.split("\n")
            # create mails array
            for row in file:
                try:
                    row = row.split(",")
                    row[0] = row[0].split(":")
                    if "(SSL)" in row[0][1]:
                        row[0][1] = row[0][1].removesuffix("(SSL)")
                    mail = {
                        'host' : row[0][0],
                        'port' : row[0][1],
                        'username' : row[1],
                        'password' : row[2],
                        'status' : '',
                        'fail_reason' : ''
                    }
                    mails.append(mail)
                except:
                    continue
            counter = 0  
            # sending test mail  
            task = [] 
            for mail in mails:
                counter = counter + 1
                task = threading.Thread(target=send_scan_mail,args=[mail,fail_mails,success_mails,white_list,generate_white_list_log])
                task.start()
            #finally log the total
            generate_white_list_log.write("\n" + "sent: " + str(len(success_mails)) + " - fails : " + str(len(fail_mails)))
        except Exception as e:
            print(e)
            #if sender_list.txt doesn't exist
            print("\n`sender_list.txt` doesn't exist!!!")
    else:
        #if email doesn't valid
        print("email is not valid...")

elif step == '2':
    use_proxy = input("\ndo you want to use proxy(Y/N)?")
    if use_proxy == 'y' or use_proxy == "Y":
        make_sure = input("\nmake sure you have `proxy_list.txt` file then press any key to continue...")
        try:
            proxy_list = open("proxy_list.txt", "r").read()
            proxy_list = proxy_list.split("\n")
            proxy_list = proxy_list[0]
            proxy_list = proxy_list.split(":")
            proxy_host = proxy_list[0]
            proxy_port = proxy_list[1]
            proxy = proxy_host+":"+proxy_port
            os.environ['http_proxy'] = proxy 
            os.environ['HTTP_PROXY'] = proxy
            os.environ['https_proxy'] = proxy
            os.environ['HTTPS_PROXY'] = proxy
        except:
            print("something wen't wrong during use proxy")
    #if user inserted 2 
    white_list_note = input('\nmake sure you have white_list.txt')
    try:
        #open white_list.txt
        whilte_list = open("white_list.txt", "r").read()
        white_list = whilte_list.split("\n")
        for row in white_list:
            #create mails list to send mails
            try:
                row = row.split(",")
                row[0] = row[0].split(":")
                if "(SSL)" in row[0][1]:
                    row[0][1] = row[0][1].removesuffix("(SSL)")
                mail = {
                        'host' : row[0][0],
                        'port' : row[0][1],
                        'username' : row[1],
                        'password' : row[2],
                        'status' : '',
                        'fail_reason' : '',
                        'receiver' : ''
                    }
                sender_mails.append(mail)
            except: 
                continue     
        try:
            #open white_list.txt
            whilte_list = open("receiver_list.txt", "r").read()
            white_list = whilte_list.split("\n")
            for row in white_list:
                #create mails list to send mails
                try:
                    row = row.split(",")
                    mail = row[0]
                    receiver_mails.append(mail)
                except: 
                    continue 
            counter = 0
            mail_subject = input("\nMails subject : ")
            mail_body = input("\nMails message : ")
            file_name = input("\nIf you have file enter file name: ")
            for receiver in receiver_mails:
                for mail in sender_mails:
                    counter = counter + 1
                    host = mail['host']
                    port = mail['port']
                    username = mail['username']
                    password = mail['password']
                    mail['receiver'] = receiver        
                    mailto = receiver
                    message = "Test mail " + username
                    try:
                        #send mail
                        # Create a multipart message
                        msg = MIMEMultipart()
                        body_part = MIMEText(mail_body, 'plain')
                        msg['Subject'] = mail_subject
                        msg['From'] = username
                        msg['To'] = mailto
                        # Add body to email
                        msg.attach(body_part)
                        if file_name != "":
                            # open and read the file in binary
                            with open(file_name,'rb') as file:
                            # Attach the file with filename to the email
                                msg.attach(MIMEApplication(file.read(), Name=str(file_name)))
                        mail_server = smtplib.SMTP(host,port)
                        mail_server.starttls()
                        mail_server.login(username,password)
                        send = mail_server.sendmail(username,mailto,msg.as_string())
                        # print( "mail sent with " + mail['username'] + " address")
                        mail_server.quit()
                        #if mail sent successfully
                        success_mails.append(mail)
                        mail['status'] = 'success'
                    except Exception as e:
                        # print('\033[91m' + str(e) + " address"+'\033[0m' )
                        #if mail failed
                        fail_mails.append(mail)
                        mail['status'] = 'failed'
                        mail['fail_reason'] = str(e)
                    finally:
                        #log mail 
                        send_mail_log.write("\n"+str(mail))
                        #clear command line 
                        if os.name == 'nt':
                            os.system('cls')
                        else:
                            os.system('clear')
                        #print status
                        print("Sending mails \n" + str(int((len(success_mails))/(len(receiver_mails))* 100))+" % \n" + str(counter) + " mails tried \n" +"\033[1;32;40m"+"sent : " + str(len(success_mails)) + " mails \n" + '\033[91m' + "fails : " +str(len(fail_mails)) + " mails \n"  +'\033[0m' + "total receivers : " + str(len(receiver_mails)) + " mails" )
                    if(mail['status'] == 'success'):
                        break
            #finally log the total
            send_mail_log.write("\n" + "sent: " + str(len(success_mails)) + " - fails : " + str(len(fail_mails)))

        except Exception as e:
            print(str(e))
            # print("\nreceiver_list.txt doesn't exist!!!")
    except:
        print("\n`white_list.txt` doesn't exist!!!\nplease generate that before sending mail!!!")

