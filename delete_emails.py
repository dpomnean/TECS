import imaplib
import email
from datetime import datetime
from configparser import SafeConfigParser

class ThePurge():

    global box 
    parser = SafeConfigParser()
    parser.read('TEC.ini')  
    
    box = imaplib.IMAP4(parser.get('email_settings', 'mailserver'))
    
    box.login(parser.get('email_settings', 'mailuser'),parser.get('email_settings', 'mailpassword'))
    
    '''
    Will delete emails in inbox, newticket,noaction and
    in updatetick folders.
    '''
    
    '''
    if stat time is <2 weeks then delete else skip
    '''
    
    '''
    will go through each mailbox, to find the emails
    and go through each one
    '''
    def emailDel(self):
        '''
        checks inbox
        '''
        emailC=box.select("Inbox")
        box.expunge()
        emailcounter=int(emailC[1][0])
        data = box.search(None, "ALL")
        count=0
        while emailcounter>count:
            self.findDate("Inbox",data,box,count)
            count+=1
        print "Inbox purged."
        emailcounter=0

        '''
        checks NewTicket
        '''
        emailC=box.select('NewTicket')
        box.expunge()
        emailcounter=int(emailC[1][0])
        data = box.search(None, "ALL")
        count=0
        while emailcounter>count:
            self.findDate("NewTicket",data,box,count)
            count+=1
        print "NewTicket purged."
        emailcounter=0

        '''
        checks NoAction
        '''
        emailC=box.select('NoAction')
        box.expunge()
        emailcounter=int(emailC[1][0])
        data = box.search(None, "ALL")
        count=0
        while emailcounter>count:
            self.findDate("NoAction",data,box,count)
            count+=1
        print "NoAction purged."
        emailcounter=0

        '''
        checks UpdateTicket
        '''
        emailC=box.select('UpdateTicket')
        box.expunge()
        emailcounter=int(emailC[1][0])
        data = box.search(None, "ALL")
        count=0
        while emailcounter>count:
            self.findDate("UpdateTicket",data,box,count)
            count+=1
        print "UpdateTicket purged."
        emailcounter=0

    '''
    Delete the email if the email is older than 2 weeks(14 days)
    from todays date.
    '''
    def findDate(self,mailbox,data,box,count):

        try:
            raw_email = data[0][1]
        except:
            raw_email = data[0]
            
        result, data = box.uid('search', None, "ALL")
        result, data = box.fetch(str(count+1), '(RFC822)')
        
        raw_email = data[0][1]
            
        emailM=email.message_from_string(raw_email)
        emaildate=datetime.fromtimestamp(rfc822.mktime_tz(rfc822.parsedate_tz(emailM['Date'])))
        
        temp=datetime.now().date()-emaildate.date()
        
        print ">>>age of email in days: ",temp.days
        
        if (temp.days>=14):
            print box.store(count+1, '+FLAGS', '\\Deleted')
        else:
            print ">>>email not older than 2 weeks"
        
p=ThePurge()        
p.emailDel()
print ">>> Purge completed."