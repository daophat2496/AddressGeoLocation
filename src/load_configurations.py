import os
import configparser

def loadConfigurations () :
    configs = {}
    config = configparser.ConfigParser()
    config.read('../config.ini')
    if os.getenv('DB_URL') == None :
        configs["db_url"] = config['Appify']['db_url']
    else :
        configs["db_url"] = os.getenv('DB_URL')

    if os.getenv('DB_DBNAME') == None :
        configs["db_dbname"] = config['Appify']['db_dbname']
    else :
        configs["db_dbname"] = os.getenv('DB_DBNAME')

    if os.getenv('DB_USERNAME') == None :
        configs["db_username"] = config['Appify']['db_username']
    else :
        configs["db_username"] = os.getenv('DB_USERNAME')

    if os.getenv('DB_PASSWORD') == None :
        configs["db_password"] = config['Appify']['db_password']
    else :
        configs["db_password"] = os.getenv('DB_PASSWORD')

    if os.getenv('BATCH_SIZE') == None :
        configs["batch_size"] = config['Setting']['batch_size']
    else :
        configs["batch_size"] = os.getenv('BATCH_SIZE')

    if os.getenv('GOOGLE_API_KEY') == None :
        configs["google_api_key"] = config['Setting']['google_api_key']
    else :
        configs["google_api_key"] = os.getenv('GOOGLE_API_KEY')

    print(configs)

    return configs