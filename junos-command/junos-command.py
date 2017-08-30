#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ncclient import manager
import sys, getpass, yaml, argparse


def commandlineparse():
    global args
    parser = argparse.ArgumentParser(
        description=
        'Run a command on many Juniper Junos OS devices via Netconf.',
        epilog=
        'i.e. junos-command.py --zone firewalls --command "show chassis hardware"'
    )
    parser.add_argument(
        '-z',
        '--zone',
        required=True,
        help='category of network devices to run command against.')
    parser.add_argument(
        '-c', '--command', required=True, help='command in quotes.')
    parser.add_argument(
        '-o', '--output', required=False, help='file to output results.')
    args = parser.parse_args()


def welcomemsg(yaml, commandline, output):
    #Print banner and ask for username and password
    global username
    global password
    print '\nUsing YAML key: ' + yamlkey
    print 'Executing Command: ' + commandline
    if output is not None:
        print 'Outputing results to: ' + output
    username = raw_input("\nNetwork device username: ")
    password = getpass.getpass(prompt, stream=None)
    print "\n\n"


def yamlread(yamlkey, commandline, outputfile):
    headerleftchar = '++++++++++++++++'
    headerrightchar = ' +++++++++++++++'
    try:
        #Open output file if selected
        if outputfile is not None: f = open(outputfile, 'w')
    except IOError:
        print 'Error opening %s for writing output', outputfile
    try:
        stream = open("config.yaml", 'r')
    except IOError:
        print 'config.yaml is missing, this file contains the list of network devices.\n\nSample format:\n\nrouters\n - 192.168.0.1\n - 192.168.1.2\n\nfirewalls\n - 172.16.1.1\n - 172.16.1.2'
        createconfig = query_yes_no(
            "Would you like to create a template config.yaml?")
        if createconfig == True:
            print "\nCreating template config.yaml in your current directory."
            try:
                y = open('config.yaml', 'w')
                y.write(
                    'routers:\n - a.b.c.d\n - a.b.c.d\n\nfirewalls:\n - a.b.c.d\n -a.b.c.d'
                )
                y.close()
                print '\n\nconfig.yaml has been created, please modify it to include your network devices.'
                sys.exit()
            except IOError:
                print 'Could not create config.yaml, there could be a permission issue'
        else:
            print "Exiting."
            if outputfile is not None: f.close()
            sys.exit()
    hostlist = yaml.load(stream)

    try:
        for x in hostlist[yamlkey.lower()]:
            topline = headerleftchar + x + ' Start ' + headerrightchar
            print topline
            try:
                cmdresult = connect(x, '22', commandline, username, password)
                print cmdresult
            except Exception, e:
                print e
            bottomline = headerleftchar + x + ' End ' + headerrightchar + '\n'
            print bottomline
            if outputfile is not None:
                f.write(topline + '\n')
                f.write(cmdresult)
                f.write('\n' + bottomline + '\n')
            stream.close()
    except KeyError:
        print 'Check your config.yaml file as your zone does not exist.'
        if outputfile is not None: f.close()
        sys.exit()
    if outputfile is not None: f.close()


def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def connect(host, port, cmdline, user, password):
    conn = manager.connect(
        host,
        port=port,
        username=user,
        password=password,
        timeout=10,
        hostkey_verify=False)
    result = conn.command(command=cmdline, format='text')
    resultstr = result.tostring
    resultstr = resultstr.splitlines()
    for a in range(0, 2):
        resultstr.pop(0)
        resultstr.pop(-1)
    for line in resultstr:
        outputresult += line
    outputresult = '\n'.join(resultstr)
    return outputresult


if __name__ == '__main__':
    commandlineparse()
    welcomemsg(args.zone, args.command, args.output)
    yamlread(args.zone.lower(), args.command, args.output)
