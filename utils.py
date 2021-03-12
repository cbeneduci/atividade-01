import logging

def setLogs(logname, loglevel = logging.INFO):
    from logging.handlers import TimedRotatingFileHandler
    import os

    # Cria diretorio de LOG caso não exista
    os.makedirs('logs', exist_ok=True)

    # Cria classe de ajuste de cor dos logs no terminal
    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.WARNING:
                record.msg = '\033[93m%s\033[0m' % record.msg
            elif record.levelno == logging.ERROR:
                record.msg = '\033[91m%s\033[0m' % record.msg
            elif record.levelno == logging.INFO:
                record.msg = '\033[94m%s\033[0m' % record.msg
            elif record.levelno == logging.DEBUG:
                record.msg = '\033[95m%s\033[0m' % record.msg
            return logging.Formatter.format(self, record)

    
    #pega o root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level=loglevel)
    
    # Formato do Log
    format = "%(asctime)s| %(levelname)s | %(funcName)s | %(threadName)s | %(message)s"
    formatter = logging.Formatter(format)

    # Todos os dias a meia noite gira o arquivo iniciando o dia em um novo arquivo de log
    logfile = TimedRotatingFileHandler(f'Logs/{logname}', when="midnight", interval=1)
    # formato da data do arquivo
    logfile.suffix = "%Y%m%d"
    # adiciona o mesmo formato do log de tela no log do arquivo
    logfile.setFormatter(formatter)
    # adiciona o Handler no log default
    root_logger.addHandler(logfile)
    
    # Cria o log do terminal
    # Adiciona cor no log
    format = ColoredFormatter(format, datefmt="%Y-%m-%d %H:%M:%S")

    # Cria handler do log colorido
    logterminal = logging.StreamHandler()
    logterminal.setFormatter(format)

    # Adiciona handler no log
    root_logger.addHandler(logterminal)