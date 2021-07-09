from tecs_log import tecsLog as tecs_logger

class email_trans:
    
    def __init__(self, mail,emailcounter,emailM,emailType):
        
        '''
        returns the number of emails in the selected mailbox
        '''
        emailC=mail.select("Inbox")
        tecs_logger (">>>transferring email...")
        
        tecs_logger( mail.select("Inbox"))
        '''
        Determines which folder the email should be transferred to
        '''
        if emailType=="AddTicket":
            try:
                tecs_logger( mail.copy(str(emailcounter),'NewTicket'))
            except:
                tecs_logger (">>>Could not transfer email")
            else:
                tecs_logger (">>>email successfully transferred to NewTicket folder")
        elif emailType=="UpdateTicket":
            try:
                tecs_logger (mail.copy(str(emailcounter),'UpdateTicket'))
            except:
                tecs_logger (">>>Could not transfer email")
            else:
                tecs_logger (">>>email successfully transferred to UpdateTicket folder")
            
        elif emailType=="None":
            try:
                tecs_logger (mail.copy(str(emailcounter),'NoAction'))
            except:
                tecs_logger (">>>Could not transfer email")
            else:
                tecs_logger (">>>email successfully transferred to NoAction folder")
                      
        'removes deleted email in processing folder'
        tecs_logger (mail.store(str(emailcounter),'+FLAGS',r'(\Deleted)'))
        tecs_logger (mail.expunge())
            
            
            