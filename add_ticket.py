from xmlrpc.client import ServerProxy
from xmlrpc.client import Binary
from tecs_log import tecsLog as tecs_logger
from configparser import SafeConfigParser
import ssl
import codecs
class EmailTicket:
    
    def __init__(self, email_dict,image_dict,image_type,file_dict):
        tecs_logger( ">>Creating ticket...")
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
        
        '''
        Creates ticket number and inputs the credentials
        of the ticket.
        '''
        c = email_dict['Subject']
        e = email_dict['Body']
        #d = parser.get('trac','component')
        #a = parser.get('trac','milestone')
        try:
            ticket_number = server.ticket.create(email_dict['Subject'],(email_dict['Body']),{'type': parser.get('trac','type')})
            #ticket_number = server.ticket.create()
        except Exception as e:
            print (e)
            tecs_logger ("could not create ticket")
        else:
            tecs_logger ("ticket: "+str(ticket_number))
            
        #tecs_logger (server.ticket.getActions(ticket_number))
        tecs_logger (server.ticket.getTicketFields())
        count=1
        
        for (k,v), (k2,v2) in zip(image_dict.items(),file_dict.items()):
                      
            image=v
            pic_type=image_type[count]
            file_name_gl=v2
            
            '''
            attaches the file to the ticket
            '''
            #derp=server.ticket.getAttachment(ticket_number)
            
            attach_count=len(server.ticket.listAttachments(ticket_number))
            if "." not in file_name_gl:
                
                file_name_gl=file_name_gl+"."+pic_type
            
                
            server.ticket.putAttachment(ticket_number, str(count+attach_count)+"_"+file_name_gl, 
            'Email Attachment '+str(count+attach_count), Binary(codecs.decode(image, 'base64')),True)

            if 'png' in file_name_gl or 'gif' in file_name_gl or 'jpeg' in file_name_gl or 'bmp' in file_name_gl or 'jpg' in file_name_gl or 'vcf' in file_name_gl:
                mticket = server.ticket.get(ticket_number)      
                b=mticket[3]
                
                
                b['description']+=" [[Image("+str(count+attach_count)+"_"+file_name_gl+",100%)]]"
                
                #b['status']='new'
                del b['time']
                del b['changetime']  
                 
                server.ticket.update(ticket_number,'',b,False,'TECS')

            count+=1        
            
        #server.ticket.update(ticket_number,'ticket update',{'owner':'IT','status': 'IT-REVIEW'})   
            
            