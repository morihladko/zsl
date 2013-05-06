from asl.application.service_application import service_application
from flask import Config
import logging
from logging.handlers import SysLogHandler
import asl.vendor
asl.vendor.do_init()
from injector import singleton
from asl.application.initializers import injection_module

app = service_application

class LoggerInitializer:

    def initialize(self, binder):
        config = binder.injector.get(Config)
        binder.bind(
            logging.Logger,
            to=app.logger,
            scope=singleton
        )

        if 'LOG_HANDLER' not in config:
            config['LOG_HANDLER'] = 'file'

        if config['LOG_HANDLER'] == "syslog":
            handler = SysLogHandler(**config['SYSLOG_PARAMS'])
        elif config['LOG_HANDLER'] == "file":
            handler = logging.FileHandler(config['LOG_FILE'])
        elif config['LONG_HANDLER'] == None or config['LONG_HANDLER'] == 'none':
            return

        handler.setLevel(config['LOG_LEVEL'])
        app.logger.addHandler(handler)

        db_logger = logging.getLogger('sqlalchemy.engine')
        db_logger.setLevel(config['DATABASE_LOG_LEVEL'])
        db_logger.addHandler(handler)

@injection_module
def logger_initializer_module(binder):
    LoggerInitializer().initialize(binder)
