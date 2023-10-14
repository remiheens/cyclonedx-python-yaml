import argparse
import parser

def main():
    # Créer un objet ArgumentParser
    prsr = argparse.ArgumentParser(description="Converter from yaml file to CycloneDx file")

    # Définir une option
    prsr.add_argument("-f", "--file", type=str, help="Path to YAML File to convert into CycloneDX format")

    # Analyser les arguments de la ligne de commande
    args = prsr.parse_args()

    # Utiliser les valeurs des arguments et des options    
    print(f"{args.file}")

    parser.parse(path=args.file)
    
if __name__ == "__main__":
    main()
