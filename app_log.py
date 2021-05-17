import logging
import logging.config
import logging.handlers
from teams_logger import Office365CardFormatter

teams_webhook_url: str = ''

config = {
    'version' : 1,
    'disable_existing_loggers' : False,
    'formatters' : {
        'simple' : {
            'format' : '%(asctime)s - %(name)s - %(levelname)s: \n\t%(messsage)s'
        },
        'teamscard' : {
            '()' : Office365CardFormatter,
            'facts' : ['asctime', 'name', 'levelname', 'lineno'],
        },
    },
    'handlers' : {
        'console' : {
            'class' : 'logging.StreamHandler',
            'level' : 'INFO',
            'formatter' : 'simple',
            'stream' : 'ext://sys.stdout',
        },
        'logfile' : {
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'info.log',
            'mode' : 'a',
            'level' : 'INFO',
            'formatter' : 'simple',
            'maxBytes': 1_048_576,
            'backupCount': 10,
        },
        'msteams' : {
            'level' : logging.INFO,
            'class' : 'teams_logger.TeamsQueueHandler',
            'url' : teams_webhook_url,
            'formatter' : 'teamscard',
        },
        'email' : {
            'level' : logging.ERROR,
            'class': 'logging.handlers.SMTPHandler',
            'mailhost' : 'smtp-mail.outlook.com',
            'fromaddr': 'sysdev@grz.gov.zm',
            'toaddrs': ['dev@domain.com', 'qa@domain.com'],
            'subject': 'Error on website you administer',
        },
    },
    'loggers' : {
        'root' : {
            'handlers' : ['msteams', 'logfile', 'console', 'email'],
            'level' : logging.DEBUG,
        }
    },
}

def make_logger() -> logging.Logger:
    logging.config.dictConfig(config)
    log = logging.getLogger()
    return log