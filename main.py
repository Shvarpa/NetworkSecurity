import argparse
from cloner import Cloner
from shutil import copyfile

parser = argparse.ArgumentParser(description='Site cloner for fishing.')
parser.add_argument('site', type=str, help="site login page URL")
parser.add_argument('--folder', default="fish", help='folder where to store site')
parser.add_argument('--email', required=True, help="email storeing fished info")
parser.add_argument('--password', required=True, help="password for email")


args = parser.parse_args()

cloner = Cloner(args.site,args.folder)
cloner.clone()

copyfile("./server.py","./"+args.folder+"/server.py")

with open(f"./{args.folder}/.env", "w") as file:
    file.write(f"EMAIL={args.email}\nPASSWORD={args.password}")