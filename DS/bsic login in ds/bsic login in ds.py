import sys
import os
import logging
import uuid
import shutil
import time

############################################################
Base = 'C:/Users/kazis/Desktop/NOTES MSC P1/Prac/DS/VKHCG'
############################################################
sCompanies = ['01-Vermeulen', '02-Krennwallner', '03-Hillman', '04-Clark']
sLayers = ['01-Retrieve', '02-Assess', '03-Process', '04-Transform', '05-Organise', '06-Report']
sLevels = ['debug', 'info', 'warning', 'error']

for sCompany in sCompanies:
    for sLayer in sLayers:
        sFileDir = os.path.join(Base, sCompany, sLayer, 'Logging')

        # If the directory exists, remove it and create it again
        if os.path.exists(sFileDir):
            shutil.rmtree(sFileDir)
        time.sleep(2)
        if not os.path.exists(sFileDir):
            os.makedirs(sFileDir)

        # Create a unique key for the log file
        skey = str(uuid.uuid4())
        sLogFile = os.path.join(sFileDir, f'Logging_{skey}.log')

        # Set up logging to a file
        print('Set up:', sLogFile)
        logging.basicConfig(level=logging.DEBUG, 
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M', 
                            filename=sLogFile, 
                            filemode='w')

        # Define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        
        # Set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)

        # Add the handler to the root logger
        logging.getLogger('').addHandler(console)

        # Now, we can log to the root logger, or any other logger.
        logging.info('Practical Data Science is fun!')

        for sLevel in sLevels:
            # Set the application name dynamically
            sApp = f'Application-{sCompany}-{sLayer}-{sLevel}'
            logger = logging.getLogger(sApp)

            if sLevel == 'debug':
                logger.debug('Practical Data Science logged a debugging message.')
            elif sLevel == 'info':
                logger.info('Practical Data Science logged information message.')
            elif sLevel == 'warning':
                logger.warning('Practical Data Science logged a warning message.')
            elif sLevel == 'error':
                logger.error('Practical Data Science logged an error message.')

