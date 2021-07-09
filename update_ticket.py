from xmlrpc.client import ServerProxy
from xmlrpc.client import Binary
from tecs_log import tecsLog as tecs_logger
from configparser import SafeConfigParser
import ssl
import codecs
from pip._vendor.requests.status_codes import codes
class UpTicket:
    
    def __init__(self, email_dict,image_dict,image_type,ticket_number,file_dict):
        tecs_logger (">>Updating Ticket...")
        parser = SafeConfigParser()
        parser.read('TEC.ini')
        '''
        Connects to the trac page
        '''
        try:
            server = ServerProxy(parser.get('trac', 'rpcurl'),context=ssl._create_unverified_context())
        except:
            tecs_logger ("could not find server")
        else:
            tecs_logger (server)
        counter = 1
        
        mticket = server.ticket.get(ticket_number)
        
        a = server.ticket.listAttachments(1291)
        b = server.ticket.changeLog(1291, 0)
        b=mticket[3]

        '''
        If there are no images, then display only the text.
        '''
        if not image_dict:
            server.ticket.update(ticket_number,email_dict['Body'])
        else:
            attach_count=len(server.ticket.listAttachments(ticket_number))
            
            for (k,v), (k2,v2) in zip(image_dict.items(),file_dict.items()): 
                
                image=v
                pic_type=image_type[counter]
                file_name_gl=v2
                
                '''
                if the file does not have a format, use the format from
                the pic_type dictionary
                '''
                if "." not in file_name_gl:
                    file_name_gl=file_name_gl+"."+pic_type
                    file_dict[v]=file_name_gl
                '''
                attaches the file to the ticket
                '''
                #server.ticket.putAttachment(ticket_number, str(counter+attach_count)+"_"+file_name_gl, 
                #'Email Attachment '+str(counter+attach_count), Binary(codecs.decode(image, 'base64')),False)
                counter=counter+1 
                
            count=1
            
            'returns how many attachments are in the ticket.'
            #attach_count=len(server.ticket.listAttachments(ticket_number))   
            
            'will determine if the first picture in the comment, which will have the text'
            t=False
            
            'will tell how many pictures have been displayed'
            displaycount=1
            
            '''
            display the pictures after they have been loaded and display them in
            the ticket if they are correct format. If there are attachments and text,
            then it will display just text, which is if t = true or false
            '''
            for (k,v), (k2,v2) in zip(image_dict.items(),file_dict.items()):
                image=v
                pic_type=image_type[2]
                file_name_gl=v2
                
                'Will display picture if its in an image format'
                if 'png' in pic_type or 'gif' in pic_type or 'jpeg' in pic_type or 'bmp' in pic_type or 'jpg' in pic_type:
                    
                    mticket = server.ticket.get(ticket_number)
                    
                    ticket.listAttachments(ticket_number)
                    
                    server.ticket.get()
                    b=mticket[3]
                
                    #b['status']='new'
                    del b['time']
                    del b['changetime']
                    
                    if attach_count == 0:
                        image_index = count
                    else:
                        image_index = attach_count-((counter-1)-count)
                
                    if displaycount==1:
                        server.ticket.update(ticket_number,email_dict['Body']+'\n'+" [[Image("+str(image_index)+"_"+file_name_gl+",100%)]]",b,False,'TECS')
                    else:
                        server.ticket.update(ticket_number," [[Image("+str(image_index)+"_"+file_name_gl+",100%)]]",b,False,'TECS')
                    t=True
                    displaycount+=1
                #else:
                    #v=v+1
                    
                count+=1
            if t==False:
                server.ticket.update(ticket_number,email_dict['Body'])
                   
        