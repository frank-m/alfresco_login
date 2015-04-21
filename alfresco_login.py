#!/usr/bin/python
import requests, sys, getopt, os

def usage():
	print sys.argv[0] + " -u <user> -p <password> [-s] -H <host>"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:sH:")
    except getopt.GetoptError:
        usage()
        return 3
    
    user = password = host = use_ssl = None

    for o, a in opts:
        if o == "-u":
            user = a 
        elif o == "-p":
            password = a
        elif o == "-H":
            host = a
        elif o == "-s":
            use_ssl = True

    if user == None or password == None or host == None:
        usage()
        return 1

    if use_ssl == True:
        alfresco_url = "https://" + host + "/alfresco/service/api/login?u=" + user + '&pw=' + password
    else:
        alfresco_url = "http://" + host + "/alfresco/service/api/login?u=" + user + '&pw=' + password

    try:
        r = requests.get(alfresco_url, timeout=5)
    except Exception, err:
        print 'CRITICAL - A connection failure has occurred'
        return 2

#    print r.text # Uncomment to debug response

    if 'Login failed' in r.text:
        print 'CRITICAL - Login failed because of wrong username/password'
        return 2
    elif not '<ticket>TICKET_' in r.text:
        print 'CRITICAL - Login failed no ticket found in response.'
        return 2
    elif '<ticket>TICKET_' in r.text:
        print 'OK - Succesfully logged in to alfresco'
        return 0

if __name__ == "__main__":
    sys.exit(main())
