import importlib
from asl.utils.string_helper import underscore_to_camelcase
from imp import reload
from asl.utils.task_helper import instantiate, get_callable

class Router:
    def __init__(self, app):
        self._mappings = {}
        # Support for the settings with only one TASK_PACKAGE defined.
        self._task_packages = (app.config['TASK_PACKAGE'],) if 'TASK_PACKAGE' in app.config else app.config['TASK_PACKAGES']
        self._app = app
        self._task_reloading = app.config['RELOAD']

    def get_task_packages(self):
        return self._task_packages

    def set_task_packages(self, task_packages):
        self._task_packages = task_packages

    def _load_module(self, module_name):
        return importlib.import_module(module_name)
    
    def is_task_reloading(self):
        return self._task_reloading

    def set_task_reloading(self, value):
        self._task_reloading = value

    '''
    Returns the task handling the given request path.
    '''
    def route(self, path):
        self._app.logger.debug("Routing path '%s'.", path)

        # Split the path into arrays - package names in the tasks package.
        path = path.split("/")
        class_name = underscore_to_camelcase(path[-1])
        
        # finding the path in task packages
        module = None
        for task_package in self.get_task_packages():
            module_name = "{0}.{1}".format(task_package, ".".join(path))
        
            try:
                self._app.logger.debug("Trying to load module with name '%s' and class name '%s'.", module_name, class_name)
                module = self._load_module(module_name)
                break
            except ImportError:
                pass
        
        if module is None:
            raise ImportError("No module named {0} found in [{1}].".format(".".join(path), ",".join(self.get_task_packages())))

        if self.is_task_reloading():
            reload(module)

        # Create the task using the injector initialization.
        cls = getattr(module, class_name)
        task = instantiate(cls)

        self._app.logger.debug("Task object {0} created [{1}].".format(class_name, task))
        return (task, get_callable(task))
