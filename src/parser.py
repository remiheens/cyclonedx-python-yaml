import yaml

def parse(path):
    with open(path, 'r') as file:
        data = yaml.safe_load(file)
        print(f"{data}")
