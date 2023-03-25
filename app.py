from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t", "--topic", dest="topic",
    required=True, help="the topic where we send the data. This decide the type of sensor")

args = parser.parse_args()