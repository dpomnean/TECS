import imaplib
import email
import base64
from configparser import SafeConfigParser
from add_ticket import EmailTicket as at
from email_transfer import email_trans as et
from update_ticket import UpTicket as ut
from tecs_log import tecsLog as tecs_logger
import quopri
from _codecs import decode
import time
start_time = time.time()

MAXLINE = 50000000

if hasattr(imaplib, "_MAXLINE") and getattr(imaplib, "_MAXLINE") < MAXLINE:
    setattr(imaplib, "_MAXLINE", MAXLINE)

image_dict=dict()
image_type= dict()
email_dict = dict()
file_dict=dict()

class TECS():
    '''
    parser for Trac Email Creation System using the imap4 client library
    '''
    tecs_logger("Starting TECS...")

    '''
    connect to the server
    '''
    
    parser = SafeConfigParser()
    parser.read('TEC.ini')  
   
    print (parser.get('email_settings', 'mailserver'))
    mail=imaplib.IMAP4(parser.get('email_settings', 'mailserver'))
    mail.login(parser.get('email_settings', 'mailuser'),parser.get('email_settings', 'mailpassword'))

    tecs_logger('>>>parser.py')
   
    
    '''
    Gets the number of emails in the mailbox.
    '''
    
    emailC,t=mail.select("Inbox")
    mail.expunge()
    emailC=mail.select("Inbox")
    emailCount=int(emailC[1][0])
    emailcounter=emailCount
       
    '''
    Will loop through, find the attachments and text,
    and put the email info in a ticket.
    ''' 
    while emailcounter>0:
        
        emailCount=int(emailC[1][0])
        if emailCount == 0:
            break;
        
        '''
        Fetches the first email in the mailbox
        '''
        result, data = mail.search(None, "ALL")
        ids = data [0]
        id_list=ids.split()
        latest_email=id_list[-1]
        id = latest_email.decode("utf-8")
        
        origional_string = mail.fetch(id,"RFC822")
        
        print ("")
    
        '''
        Finds the raw email text of the email
        '''
        try:
            raw_email = data[0][1]
        except:
            raw_email = data[0]
            
        '''
        returns unique id incase any of the emails get deleted
        '''
        result, data = mail.uid('search', None, "ALL")
        
        
        origional_string = mail.fetch(str(emailcounter), '(RFC822)')
        result, data = mail.fetch(str(emailcounter), '(RFC822)')
        
        raw_email = data[0][1].decode("utf-8")
        
        'tecs_logger(origional_string)'

        emailM=email.message_from_string(raw_email)
        date=emailM['Date']
        tecs_logger(emailM['Content-Type'])
 
        bodytext = ""

        '''
        This will find only the text in the email
        '''
        maintype = emailM.get_content_maintype()
        for part in emailM.walk():
            c_type = part.get_content_type()
            c_disp = part.get('Content-Disposition')
        
            if c_type == 'text/plain' and c_disp == None:
                bodytext = bodytext + part.get_payload()
                #d = base64.b64decode(bodytext)
                #bodytext = bodytext.encode('utf_8')
                decoded = quopri.decodestring(bodytext)
                bodytext = decoded.decode("utf-8",'ignore')
            else:
                continue
    
        tecs_logger( '-----------------------------------------------------------')
        
        
        count = 1
        body=''

        '''
        This will find the attachment in the emails
        '''
        if "####" in emailM['Subject']:
            for part in emailM.walk():
    
                file_name_gl=None
                mptype = part.get_content_maintype()
                file_name_gl=part.get_filename()
                content= part.get("Content-Disposition")
            
                '''
                Determines the type of the payload
                '''    
                if mptype=="multipart":
                    continue
                elif mptype=="text" and ".txt" not in str(file_name_gl):
                    if not file_name_gl: continue
                
                elif mptype=="image" or mptype=="application" or ".txt" in str(file_name_gl):
                    content_id=part.get('Content-ID')
                    if str(content)=="None":
                        content="png"
                    if file_name_gl==None:
                        file_name_gl="Screenshot.png"
                    file_dict[count-1]=file_name_gl
                    #if file_name_gl or mptype=="application":
                    # file_name_gl='image_'+str(count)+'.'+part.get_content_subtype()
                    image_type[count]=str(file_name_gl).split('.')[1]
                    '''
                    changing the file type if the file type is in the filename. 
                    will remove instances with oct-stream, application, and excel
                    '''  
                    '''                     
                    if 'png' in content:
                        image_type[count]='png'
                    elif 'xls' in content:
                        image_type[count]='xlsx'
                    elif 'pdf' in content:
                        image_type[count]='pdf'
                    elif 'txt' in content:
                        image_type[count]='txt'
                    elif 'doc' in content:
                        image_type[count]='doc'
                    else:
                        image_type[count]=part.get_content_subtype()
                    '''
                    tecs_logger( file_name_gl)
                    count+=1
            
                    body = part.get_payload(decode = True)   
                    body = base64.encodestring(body)
                    image_dict[count-2] = body
                    
        else:
            tecs_logger(">>>This email does not contain the proper email syntax...")
            
        subject=emailM['Subject']
        
        '''
        Will remove "####new" and any capitalization
        of 'new' so only the subject will be the header
        '''
        
        header_subject = ""
        
        if "NEW" in emailM['Subject'].split(' ')[0].upper():
            subject = emailM['Subject'].split(' ')[0].upper()
            header_subject = emailM['Subject'][7:]
        else:
            subject = emailM['Subject'].split(' ')[0]
            subject = subject.strip('#').split()[0]
        #string = emailM['Subject'][4:]
        #string=string.upper()
        #header_string=emailM['Subject'][0:4]+string
        #subject=subject.replace(("####"+ emailM['Subject'][4:7]),"NEW")
        
        #if "NEW" in emailM['Subject']:                                
        #    subject=subject.replace("NEW","") 
            
        '''    
        print out the information for verification
        '''
        tecs_logger (("there should be", count-1, " attachment(s)"))
        tecs_logger (("To: " , emailM['To']))
        tecs_logger (("From: " , email.utils.parseaddr(emailM['From'])))
        tecs_logger (("Subject: ", header_subject))
        tecs_logger (("Body: ", bodytext))
        tecs_logger (("--End Body--"))
        tecs_logger (emailM.items)
        
        email_dict.update({'To':emailM['To']})
        email_dict.update({'From':email.utils.parseaddr(emailM['From'])})
        email_dict.update({'Subject': header_subject})        
        email_dict.update({'Body': bodytext})

        '''
        if the header contains new, it will call the add ticket module.
        if the header contains a ticket number, it will update the ticket.
        '''
        if '####NEW' in subject:
            try:
                at(email_dict,image_dict,image_type,file_dict)
            except Exception as e: 
                print (e)
                tecs_logger(">>>Error has been thrown for newTicket")
                emailcounter-=1
            emailType="AddTicket"
        
        elif "####NEW" not in subject:
            #upTick=emailM['Subject']
            #upTick=upTick.upper()
            #upTick=upTick.strip('#').split()[0]
            #upTick=filter(lambda n:n not in '#`~!@$%^&*()_=+[{]}\|''";:/?.>,<ZXCVBNMLKJHGFDSAQWERTYUIOP ',upTick)
            upTick=int(subject)
            
            try:
                ut(email_dict,image_dict,image_type,upTick,file_dict)
                emailType="UpdateTicket"
            #except:
            except Exception as e: 
                print (e)
                tecs_logger (">>>Error has been thrown for updating...")
                emailType="None"
                
        else:
            emailType="None"
            
        '''
        will transfer the ticket if no errors occurred with processing a ticket
        '''
        et(mail,emailcounter,emailM,emailType)
        emailType=""   
        emailcounter-=1
        
        '''
        Clears all contents of the dictionaries so they can be used
        for the next email
        '''
        image_dict.clear()
        image_type.clear()
        email_dict.clear()
        file_dict.clear()
        tecs_logger(">>>Dictionaries cleared...")
        tecs_logger(">>>processing next email...")
        
e=TECS()
tecs_logger( ">>>Trac Email Creation Complete...")
tecs_logger("--- %s seconds ---" % (time.time() - start_time))


