'''
:mod:`asl.utils.cache_helper`

.. moduleauthor:: Martin Babka
'''
from asl.application.service_application import service_application
from asl.utils.injection_helper import inject
from asl.cache.id_helper import IdHelper, create_key_object_prefix,\
    app_model_decoder_fn, app_model_encoder_fn
from asl.db.model.app_model_json_encoder import AppModelJSONEncoder
import json
import abc
from asl.task.job_context import JobContext

class CacheDecorator:
    @inject(id_helper = IdHelper)
    def __init__(self, id_helper):
        self._id_helper = id_helper
        service_application.logger.debug("Initializing CacheDecorator.")

    def decorate(self, key_params, timeout, fn):
        self._key_params = key_params
        self._fn = fn
        self._timeout = timeout

        return self.get_wrapped_fn()

    def is_caching(self, *args):
        jc = JobContext.get_current_context()
        if 'cache' not in jc.job.data:
            cs = True # TODO: Default
        else:
            cs = bool(jc.job.data['cache'])

        service_application.logger.debug("Cache status: '%s'.", cs)
        return cs

    @abc.abstractmethod
    def get_wrapped_fn(self):
        pass

    def get_data_key(self, *args):
        prefix = create_key_object_prefix(args[0])
        key = create_key_for_data(prefix, args[1], self._key_params)
        return key

    def get_decoder(self):
        return app_model_decoder_fn

    def get_encoder(self):
        return app_model_encoder_fn

class CacheOutputDecorator(CacheDecorator):
    def get_wrapped_fn(self):
        def wrapped_fn(*args):
            if not self.is_caching(*args):
                return self._fn(*args)

            key = self.get_data_key(*args)
            service_application.logger.debug("Initializing CacheOutputDecorator - key %s.", key)

            if self._id_helper.check_key(key):
                service_application.logger.debug("Retrieved from cache.")
                return self._id_helper.get_key(key)
            else:
                ret_val = self._fn(*args)
                self._id_helper.set_key(key, ret_val, self._timeout)
                service_application.logger.debug("Newly fetched into the cache.")
                return ret_val

        return wrapped_fn

def cache_output(key_params, timeout = 'default'):
    def decorator_fn(fn):
        return CacheOutputDecorator().decorate(key_params, timeout, fn)

    return decorator_fn

class CacheModelDecorator(CacheDecorator):
    def get_wrapped_fn(self):
        def wrapped_fn(*args):
            if not self.is_caching(*args):
                return self._fn(*args)

            key = self.get_data_key(*args)
            service_application.logger.debug("Initializing CacheModelDecorator - key %s.", key)

            if self._id_helper.check_key(key):
                model_key = self._id_helper.get_key(key)
                service_application.logger.debug("Retrieved from cache %s.", model_key)
                
                if self._id_helper.check_key(model_key):
                    return self.get_decoder()(model_key, self._id_helper.get_key(model_key))

            model = self._fn(*args)
            encoded_model = json.dumps(model, cls = AppModelJSONEncoder)
            model_key = self._id_helper.create_key(model)
            self._id_helper.set_key(key, model_key, self._timeout)
            self._id_helper.set_key(model_key, encoded_model, self._timeout)
            service_application.logger.debug("Newly fetched into the cache.")
            return model

        return wrapped_fn

def cache_model(key_params, timeout = 'default'):
    '''
    Caching decorator for app models in task.perform
    '''
    def decorator_fn(fn):
        return CacheModelDecorator().decorate(key_params, timeout, fn)

    return decorator_fn

class CachePageDecorator(CacheDecorator):
    def get_wrapped_fn(self):
        def wrapped_fn(*args):
            if not self.is_caching(*args):
                return self._fn(*args)

            page_key = self.get_data_key(*args)
            service_application.logger.debug("Initializing CachePageDecorator - key %s.", page_key)

            if self._id_helper.check_page(page_key):
                service_application.logger.debug("Retrieved from cache %s.", page_key)
                return self._id_helper.gather_page(page_key, self.get_decoder())

            page = self._fn(*args)
            self._id_helper.fill_page(page_key, page, self._timeout, self.get_encoder())
            service_application.logger.debug("Newly fetched into the cache.")
            return page

        return wrapped_fn

def cache_page(key_params, timeout = 'default'):
    '''
    Cache a page (slice) of a list of AppModels
    '''
    def decorator_fn(fn):
        d = CachePageDecorator()
        return d.decorate(key_params, timeout, fn)

    return decorator_fn

# alias
cache_list = cache_page

def cache_filtered_page(filter_param = 'filter', pagination_param = 'pagination', sorter_param = 'sorter', timeout = 'default'):
    def decorator_fn(fn):
        d = CachePageDecorator()
        return d.decorate([filter_param, sorter_param, pagination_param], timeout, fn)

    return decorator_fn

def create_key_for_data(prefix, data, key_params):
    '''
    From ``data`` params in task create corresponding key with help of ``key_params`` (defined in decorator) 
    '''
    d = data.get_data()
    values = []
    for k in key_params:
        if k in d and type(d[k]) is list:
            values.append("{0}:{1}".format(k, " -".join(d[k])))
        else:
            value = d[k] if k in d else ''
            values.append("{0}:{1}".format(k, value))
            
    return "{0}-{1}".format(prefix, "-".join(values))
