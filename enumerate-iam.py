#!/usr/bin/env python
import argparse
import sys

from boto3 import Session
from enumerate_iam.main import enumerate_iam

def main():
    parser = argparse.ArgumentParser(description='Enumerate IAM permissions')

    parser.add_argument('--profile', help='AWS profile name if not providing other credentials. Default aws profile will be used if found.')
    parser.add_argument('--access-key', help='AWS access key')
    parser.add_argument('--secret-key', help='AWS secret key')
    parser.add_argument('--session-token', help='STS session token')
    parser.add_argument('--region', help='AWS region for API requests', default='us-east-1')

    args = parser.parse_args()
    if not (args.access_key and args.secret_key and args.session_token):
        if (args.profile):
            credentials = Session(profile_name = args.profile).get_credentials()
        else:
            credentials = Session().get_credentials()
        
        args.access_key = credentials.access_key
        args.secret_key = credentials.secret_key
        args.session_token = credentials.token
        
    if not (args.access_key and args.secret_key and args.session_token):
        sys.stderr.write('[!]: No credentials imported.  You must at least have a default aws profile configured or\n')
        sys.stderr.write('     provide access key, secret key, and session token.\n\n')
        parser.print_help()
        sys.exit(2)
    
    enumerate_iam(args.access_key,
                  args.secret_key,
                  args.session_token,
                  args.region)


if __name__ == '__main__':
    main()
