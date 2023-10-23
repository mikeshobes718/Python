import argparse
import sys
import os

program_name = os.path.basename(__file__)

if(sys.version_info.major == 2):
    sys.exit("Error: " + program_name + " requires Python 3.")

def print_all_help(parser, subparsers):
    # parser.print_help()
    print(f'''usage: use "python {program_name} -h" for help\n\npositional arguments:
    {program_name} scenario1 -h
    {program_name} scenario2 -h
    {program_name} scenario3 -h
    ''')
    print("\nScenario 1 Arguments: -u -p")
    # subparsers.choices['scenario1'].print_help()
    print("\nScenario 2 Arguments:")
    # subparsers.choices['scenario2'].print_help()
    print("\nScenario 3 Arguments:")
    # subparsers.choices['scenario3'].print_help()
    sys.exit()

def main():
#     # parser = argparse.ArgumentParser(description='EKS Configuration Program')
    
    parser = argparse.ArgumentParser(
            usage='use "python %(prog)s -h" for help',
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False)            
    subparsers = parser.add_subparsers(dest='scenario', help='Scenarios')

    # Scenario 1
    parser_s1 = subparsers.add_parser(
        'scenario1',
        help='Scenario 1 Help',
        description='This scenario is used for setting up a production environment with specified AWS configurations.'
    )
    parser_s1.add_argument('-p', '--project', help='Project Name', required=True)
    # ... other arguments for scenario 1 ...

    # Scenario 2
    parser_s2 = subparsers.add_parser(
        'scenario2',
        help='Scenario 2 Help',
        description='This scenario is used for setting up an ADG environment with specified email contacts.'
    )
    parser_s2.add_argument('-c', '--confirm', help='Confirmation', choices=['yes', 'no'], required=True)
    # ... other arguments for scenario 2 ...

    # Scenario 3
    parser_s3 = subparsers.add_parser(
        'scenario3',
        help='Scenario 3 Help',
        description='This scenario is used for setting up an environment with health checks.'
    )
    parser_s3.add_argument('-hc', '--health-check', action='store_true', help='Enable Health Check')
    # ... other arguments for scenario 3 ...

    # parser.add_argument('-t', '--text', help='Some flag', action='store_true')
    parser.add_argument('-h',
                        '--help',
                        help=argparse.SUPPRESS,
                        action='store_true')

    args = parser.parse_args()

    # Check if a scenario was provided
    if args.scenario is None:
        # Check if -h or --help was specified
        if any(arg in ['-h', '--help'] for arg in sys.argv):
            print_all_help(parser, subparsers)
        else:
            parser.error("No scenario provided. Please specify either 'scenario1', 'scenario2', or 'scenario3'.")

    # Process arguments based on the scenario
    if args.scenario == 'scenario1':
        # ... process scenario 1 ...
        pass
    elif args.scenario == 'scenario2':
        # ... process scenario 2 ...
        pass
    elif args.scenario == 'scenario3':
        # ... process scenario 3 ...
        pass

if __name__ == '__main__':
    main()
