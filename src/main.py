import argparse
from YamlConverter import YamlConverter 

def main():

    prsr = argparse.ArgumentParser(description="Converter from yaml file to CycloneDx file")
    prsr.add_argument("-f", "--file", type=str, help="Path to YAML File to convert into CycloneDX format")
    prsr.add_argument("-o", "--output", type=str, help="Path to outputfile")

    args = prsr.parse_args()
    print(f"{args.file}")

    yamlConverter = YamlConverter()
    yamlConverter.convert(path=args.file, output=args.output)
    
if __name__ == "__main__":
    main()
