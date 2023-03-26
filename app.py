from argparse import ArgumentParser
from client import Client

def main():
    parser = ArgumentParser()
    parser.add_argument("-a", "--all", dest="all", default=False, action='store_true', help="Encrypt all files using master key (MK).")
    parser.add_argument("-e", "--each", dest="each", default=False, action='store_true', help="Encrypt each file using a data encryption key (DEK) protected with master key (MK) and password.")

    args = vars(parser.parse_args())
    print(args)
    client = Client(args)
    

if __name__ == "__main__":
    main()