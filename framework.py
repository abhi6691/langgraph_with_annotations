# framework.py

import inspect

# Decorators
def initialize(func):
    """Decorator for initialization functions."""
    func._is_initialize = True
    return func

def entrypoint(func):
    """Decorator for main entrypoint functions."""
    func._is_entrypoint = True
    return func

def application(cls):
    """Decorator to mark the main application class."""
    cls._is_application = True
    return cls

class LambdaHandler:
    def __init__(self, module):
        # Dynamically load the main application class
        self.app = self._load_application_class(module)
        self.initialize_methods()

    def _load_application_class(self, module):
        # Look for the class marked with @application
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if getattr(obj, "_is_application", False):
                print(f"Found application class: {name}")
                return obj()  # Instantiate the class
        raise RuntimeError("No class found with @application annotation.")

    def initialize_methods(self):
        # Run all methods marked with @initialize
        for name, method in inspect.getmembers(self.app, predicate=inspect.ismethod):
            if getattr(method, "_is_initialize", False):
                print(f"Running initialize method: {name}")
                method()

    def handle_request(self, event):
        # Look for the method marked with @entrypoint
        for name, method in inspect.getmembers(self.app, predicate=inspect.ismethod):
            if getattr(method, "_is_entrypoint", False):
                print(f"Invoking entrypoint method: {name}")
                return method(event)
        raise RuntimeError("No entrypoint method defined.")

