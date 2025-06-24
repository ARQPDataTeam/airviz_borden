
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv
import logging 

def sql_engine_string_generator(qp_host, datahub_host, datahub_user, datahub_pwd, datahub_db,fsdh,logger):

    # if the local switch is off, try to run through fsdh key vault
    if fsdh:
        try:
            DB_HOST = os.getenv(datahub_host)
            DB_USER = os.getenv(datahub_user)
            DB_PASS = os.getenv(datahub_pwd)
            
            logger.info('Credentials loaded from FSDH')

        except Exception as e:
            logger.debug(f"{datahub_host}: {DB_HOST}")
            logger.debug(f"{datahub_user}: {DB_USER}")
            logger.debug(datahub_pwd)
            # declare FSDH keys exception
            error_occur = True
            logger.error(f"An error occurred: {e}")
    
    else:
        # load the .env file using the dotenv module remove this when running a powershell script to confirue system environment vars
        parent_dir=os.path.dirname(os.getcwd())
        load_dotenv(os.path.join(parent_dir, '.env')) # default is relative local directory 
        DB_HOST = os.getenv(datahub_host)
        DB_USER = os.getenv(datahub_user)
        DB_PASS = os.getenv(datahub_pwd)
        logger.info('Credentials loaded locally')
        logger.debug(f"{datahub_host}: {DB_HOST}")
        logger.debug(f"{datahub_user}: {DB_USER}")
        logger.debug(datahub_pwd)

    # set the sql engine string
    sql_engine_string=('postgresql://{}:{}@{}/{}?sslmode=require').format(DB_USER,DB_PASS,DB_HOST,datahub_db)
    return sql_engine_string
