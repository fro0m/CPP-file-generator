import os
import re
import yaml

# config functions
def find_config_file(directory):
    while directory != os.path.dirname(directory):
        config_file = os.path.join(directory, 'generator.conf')
        if os.path.exists(config_file):
            return config_file
        directory = os.path.dirname(directory)
    return None

def read_config(file_path):
    try:
        with open(file_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

def get_config(file_path=None):
    if file_path is None:
        file_path = os.getcwd()

    config_file = find_config_file(file_path)
    if config_file:
        return read_config(config_file)
    else:
        print("No generator.conf file found in the directory tree.")
        return None

# Example usage
config = get_config()
if config:
    print("Configuration:")
    for key, value in config.items():
        print(f"{key}: {value}")

    print("\n")

def camel_to_snake(name):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()

def create_cpp_class(class_name, methods):
    if config["FileNameFormat"] == "CamelCase":
        file_name = class_name
    elif config["FileNameFormat"] == "snake_case":
        file_name = camel_to_snake(class_name)

    # Create header file content
    header_content = f"#ifndef {class_name.upper()}_H\n#define {class_name.upper()}_H\n\n"
    header_content += f"class {class_name} {{\npublic:\n"

    for method in methods:
        header_content += f"    void {method}();\n"

    header_content += "};\n\n#endif // " + f"{class_name.upper()}_H\n"

    # Create cpp file content
    header_file_ext = config["HeaderFileExtention"]
    cpp_content = f"#include \"{file_name}.{header_file_ext}\"\n\n"

    for method in methods:
        cpp_content += f"void {class_name}::{method} {{\n    // TODO: Implement {method}\n}}\n\n"

    # Write to header file
    with open(f"{file_name}.{header_file_ext}", "w") as header_file:
        header_file.write(header_content)

    # Write to cpp file
    with open(f"{file_name}.cpp", "w") as cpp_file:
        cpp_file.write(cpp_content)

    print(f"Generated {file_name}.hpp and {file_name}.cpp")

if __name__ == "__main__":
    class_name = input("Enter the class name: ")
    methods = input("Enter method names separated by commas: ").split(',')

    # Strip whitespace from method names
    methods = [method.strip() for method in methods]

    create_cpp_class(class_name, methods)
