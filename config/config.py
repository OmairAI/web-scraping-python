import configparser
import logging
import argparse
from logging.handlers import RotatingFileHandler
from datetime import datetime

config = None
logger = None

def initialiseConfig(pathConfig):
    global config
    config = configparser.ConfigParser()
    config.read(pathConfig)
    return config

def initialiseLog():
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    timestampDebut = datetime.now().strftime("%Y%m%d_%H%M%S")
    nomFichierLog = config["LOG"]["cheminLog"] + str(timestampDebut) + "_" + config["LOG"]["nomFichierLog"]
 
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(nomFichierLog, 'w', 100000000, 1)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

def parseArgs():
    parser = argparse.ArgumentParser(description='Web scrapping python')
    parser.add_argument("-c", "--config", required=True, help="path du fichier de configuration")
    parser.add_argument("-a", "--analyse", required=True, help="analyse les données ou non")
    parser.add_argument("-s", "--save", required=True, help="enregistre le csv ou non")
    parser.add_argument("-r", "--read", required=True, help="prend le fichier founi en df")

    args = vars(parser.parse_args())
    print(args)
    return args

def getConfig():
    global config
    return config