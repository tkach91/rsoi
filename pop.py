#!/usr/bin/python

import poplib
import base64

import PIL.Image

class Email:
    def __init__(self, server, port, user, password):
        self.box = poplib.POP3_SSL(server, port) 
        self.box.user(user) 
        self.box.pass_(password)

    def __del__(self):
        self.box.quit()

    def fetch(self):
        result = { 'text': ''}
        poplist = self.box.list()
        if poplist[0].startswith('+OK') :
            msglist = poplist[1]
            if msglist:
                for msgspec in msglist:
                    msgnum = int(msgspec.split(' ')[0])

                    content = False
                    count = 0
                    for msg in self.box.retr(msgnum)[1]:
                        #print "%d: %s" % (count, msg)
                        if content:
                            result['text'] += msg
                        if msg.startswith('Subject:'):
                            result['subject'] = msg
                        if msg.startswith('From:'):
                            result['from'] = msg
                        if msg == '':
                            if not content:
                                content = True
                            else:
                                result['text'] += '\n'


                        count = count + 1

                    self.box.dele(msgnum)
                     
            else:
                print "No messages for ", user
        else:
            print "Couldn't list messages: status ", poplist[0] 

        return result
        
      
if __name__ == "__main__":
    user = 'rsoi100@yandex.ru'
    password = 'number2128506'

    email = Email('pop.yandex.ru', 995, user, password)
    result = email.fetch()
    #print result
    #print result['text']
    
    encoded = base64.b64decode(result['text'])
    print encoded
    f = open('fetched.gif', 'wb')
    f.write(encoded)

