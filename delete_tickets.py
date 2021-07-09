import xmlrpclib


class EmailTicket:
    
        print  ">>Deleting ticket..."
        '''
        **********NOTE: SHOULD BE USED WITH CAUTION*********
        '''
       
        server = xmlrpclib.ServerProxy("https://user:password@trac.company.com/trac/login/rpc")
        
        i=1021
        
        try:
            while i>=i:
                server.ticket.delete(i)
                print "deleted ticket", i
                i+=1
        except:
            print "done."