#!/usr/bin/python
import sys
import base64

from smtplib import SMTP
from email.MIMEText import MIMEText
import poplib

pop_server = 'dev.iu7.bmstu.ru'
pop_port = 10110 

smtp_server = 'dev.iu7.bmstu.ru'
smtp_port = 10025

user = 'mbox1727-00@dev.iu7.bmstu.ru'
password = 'Hzjrz'

class Email:
    def __in__(self):
        self.box = poplib.POP3(pop_server, pop_port) 
        self.box.user(user) 
        self.box.pass_(password)
        
    def __out__(self):
        self.box.quit()
        
    def fetchmail(self):
        self.__in__()
        result = []
        poplist = self.box.list()

        if poplist[0].startswith('+OK') :
            msglist = poplist[1]
            if msglist:
                #print "MSG LIST"
                #print msglist
                for msgspec in msglist:
                    msgnum = int(msgspec.split(' ')[0])
                    #print "MSG NUM %d" % msgnum
                    
                    mail = {'text': ''}
                    content = False
                    count = 0
                    for msg in self.box.retr(msgnum)[1]:
                        #print "%d: %s" % (count, msg)
                        if content:
                            mail['text'] += msg
                        if msg.startswith('Subject:'):
                            mail['subject'] = msg
                        if msg.startswith('From:'):
                            mail['from'] = msg
                        if msg == '':
                            if not content:
                                content = True
                            else:
                                mail['text'] += '\n'

                        count = count + 1

                    result.append(mail)
                    self.box.dele(msgnum)
                     
            else:
                print "No messages for %s" % user
                self.__out__()
                return None
        else:
            print "Couldn't list messages: status %s" % poplist[0] 
            self.__out__()
            return None


        self.__out__()
        return result
        
  
    def sendmail(self, content, subject, destination):
        text_subtype = 'plain'

        try:
            msg = MIMEText(content, text_subtype)
            msg['Subject'] = subject
            msg['From'] = user 

            conn = SMTP(smtp_server, smtp_port)
            conn.set_debuglevel(False)
            conn.login(user, password)
            try:
                conn.sendmail(user, destination, msg.as_string())
                print "Sent '%s' to %s" % (subject, destination)
            finally:
                conn.close()
                return "OK"

        except Exception, exc:
            sys.exit("mail failed: %s" % str(exc))
            return None

if __name__ == "__main__":
    email = Email()

    email.sendmail('content1.\n mmmm\n Best Regards.', 'subject1', user)
    email.sendmail('content2. hmm', 'subject2', user)

    result = email.fetchmail()

    print 'RESULT: '
    print result
