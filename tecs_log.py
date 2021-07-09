import logging,os
from time import strftime

class tecsLog():
    def __init__(self,log_msg):

        '''
        creates log file for TECS and prints log to console
        '''
        #LOG_FILENAME="%s.log" %strftime("%m-%d-%Y_%H.%M.%S")
        LOG_FILENAME="%s.log" %strftime("%m-%d-%Y")
        logDir="log"
        logPath = os.path.join(logDir, LOG_FILENAME)
        logging.basicConfig(filename=logPath, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
        logging.info(log_msg)
        print (log_msg)