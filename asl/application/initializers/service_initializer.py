'''
Created on 24.1.2013

@author: Martin Babka
'''

import asl.vendor
from injector import singleton
import logging
from asl.application.initializers import injection_module
from asl.utils.string_helper import camelcase_to_underscore
asl.vendor.do_init()
from asl.application import service_application

class ServiceInitializer(object):
    '''
    Initializer handling the service injection.
    '''

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        service_injection_config = service_application.config['SERVICE_INJECTION']
        services = service_injection_config['list']
        service_package = service_injection_config['package']

        for cls_name in services:
            module_name = camelcase_to_underscore(cls_name)
            package_name = "{0}.{1}".format(service_package, module_name)
            module = getattr(__import__(package_name).service, module_name)
            cls = getattr(module, cls_name)

            binder.bind(
                cls,
                to = binder.injector.create_object(cls),
                scope = singleton
            )
            logger = binder.injector.get(logging.Logger)
            logger.debug("Created {0} binding.".format(cls))


@injection_module
def application_initializer_module(binder):
    ServiceInitializer().initialize(binder)