import importlib
import os
from framework import LambdaHandler

def find_application_module():
    # List all Python files in the current directory
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename != "lambda_function.py" and filename != "framework.py":
            module_name = filename[:-3]  # Remove the .py extension

            # Dynamically import the module
            module = importlib.import_module(module_name)
            
            # Check if the module contains a class with @application
            for name, obj in vars(module).items():
                if isinstance(obj, type) and getattr(obj, "_is_application", False):
                    print(f"Found application class in module: {module_name}.{name}")
                    return module  # Return the module containing the application class

    raise RuntimeError("No module with @application class found.")

def lambda_handler(event, context):
    # Find and load the application module
    app_module = find_application_module()
    # Initialize LambdaHandler with the dynamically found module
    handler = LambdaHandler(app_module)
    return handler.handle_request(event)

