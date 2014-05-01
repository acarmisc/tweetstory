import ConfigParser
import os
import logging


def _logger(name):
    #FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    FORMAT = '%(asctime)-15s %(message)s'
    #FIXME: log level must be moved to config
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    logger = logging.getLogger(name)
    # use like this:
    # d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    # logger.warning('Protocol problem: %s', 'connection reset', extra=d)

    return logger


def getConfig():
    config = ConfigParser.RawConfigParser()

    if config.read('config.ini'):
        db_url = config.get('mongodb', 'db_url')
        db_name = config.get('mongodb', 'db_name')
    else:
        db_url = os.environ['OPENSHIFT_MONGODB_DB_URL']
        db_name = os.environ['OPENSHIFT_APP_NAME']

    print "=============="
    print db_name

    t_api_key = os.environ['t_api_key']
    t_api_secret = os.environ['t_api_secret']
    t_acc_token = os.environ['t_acc_token']
    t_acc_secret = os.environ['t_acc_secret']

    data = {'db_url': db_url,
            'db_name': db_name,
            'twitter': {
                't_api_key': t_api_key,
                't_api_secret': t_api_secret,
                't_acc_token': t_acc_token,
                't_acc_secret': t_acc_secret
            }}

    return data
