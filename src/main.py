import argparse
import yaml
from BomBuilder import BomBuilder 

def main():

    prsr = argparse.ArgumentParser(description="Converter from yaml file to CycloneDx file")
    prsr.add_argument("-f", "--file", type=str, help="Path to YAML File to convert into CycloneDX format")
    prsr.add_argument("-o", "--output", type=str, help="Path to outputfile")

    args = prsr.parse_args()

    with open(args.file, 'r') as file:
        data = yaml.safe_load(file)
        
    bom_builder = BomBuilder(yaml=data)
    bom_builder.build_from_yaml()
    bom_builder.save_to_file(output=args.output)
    
if __name__ == "__main__":
    main()
