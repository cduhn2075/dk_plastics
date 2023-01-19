#!/usr/bin/python3
import ipaddress
import os
import json
import socket


from pymongo import MongoClient
# from data.config import config1, config2
from pymongo.errors import ConnectionFailure, OperationFailure
import pprint
import psycopg2
import psycopg2.extras
import logging
import psutil
from datetime import date
from ipaddress import ip_address, ip_network
import requests
import sublist3r
logging.basicConfig(filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO)
from pe_reports.data.config import config

# CSG credentials
API_Client_ID = os.getenv('CSGUSER')
API_Client_secret = os.environ.get('CSGSECRET')

def getToken():
    d = {'grant_type': 'client_credentials', 'client_id': f"{API_Client_ID}",
         'client_secret': f"{API_Client_secret}"}
    r = requests.post('https://api.cybersixgill.com/auth/token', data=d)
    r = r.text.split(":")
    r = r[1].lstrip('"').rsplit('"')[0]

    return r

def amiconnected():
    logging.info('Got here')
    myprocess = os.popen('w')

    pro1 =myprocess.read()


    if 'bastion' in pro1:
        logging.info('This application has a connection to the cyhy db...')
    else:
        logging.info('The bastion was not running')
        try:
            logging.info('Starting the bastion')
            os.system('ssh bastion.prod-a.cyhy.ncats.cyber.dhs.gov')
        except:
            logging.info('There was a problem starting the bastion.')

def terminatecyhyssh():
    for theprocess in psutil.process_iter():
        # logging.info(theprocess)
        if theprocess.name() == 'ssh':
            logging.info("The process was found")
            theprocess.terminate()
            logging.info('The process was terminated')
        else:
            pass


# def verifyIPv4(custIP):
#
#     try:
#         if ipaddress.ip_address(custIP) or ipaddress.ip_network(custIP):
#             return True
#
#         else:
#             return False
#
#     except ValueError as err:
#         logging.error(f'The address is incorrect, {err}')
#         return False
#
# def verifyCIDR(custIP):
#
#     try:
#         if ipaddress.ip_network(custIP):
#             return True
#
#         else:
#             return False
#
#     except ValueError as err:
#         logging.error(f'The cidr is incorrect, {err}')
#         return False




def cyhyGet1():


    myinfo = config2()
    host =myinfo['host']
    user = myinfo['user']
    password = myinfo['password']
    port = myinfo['port']
    dbname = myinfo['database']
    agencyInfo = {}
    agencyNames = []


    try:

        CONNECTION_STRING = f"mongodb://{user}:{password}@{host}:{port}/{dbname}"

        client = MongoClient(CONNECTION_STRING)

        mydb = client['cyhy']

        myfirstcoll = mydb['requests']

        # allcollections = mydb.list_collection_names()

        getAllData = myfirstcoll.find()



        for x in getAllData:


            allAgency = x['_id']
            agencyNames.append(allAgency)
            #allIPS is a list of all ip and subnets
            allIPS = x['networks']

            agencyInfo[allAgency] = allIPS

            # theAgency = x['acronym']
    except OperationFailure as e:
        logging.error(f'There was a problem connecting to the database {e}')



    return agencyInfo, agencyNames

# def getAgency(org_name):
#     """
#     Get all agency names from P&E database.
#     """
#     hostname1 = 'ABCM'
#
#     global conn, cursor
#     resultDict = {}
#     try:
#         params = config()
#
#         conn = psycopg2.connect(**params)
#
#         if conn:
#             logging.info(f'There was a connection made to the database and the query was executed ')
#
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#             query = "select organizations_uid,name from"
#             f" organizations where name='{org_name}';"
#
#             cursor.execute(f"select organizations_uid,name from"
#             f" organizations where name='{org_name}';")
#
#             result = cursor.fetchall()
#
#             for row in result:
#                 theDomain = row[0]
#                 theIP = row[1]
#
#                 resultDict[f'{theDomain}'] = f'{theIP}'
#             return resultDict
#
#     except (Exception, psycopg2.DatabaseError) as err:
#         logging.error(f'There was a problem logging into the psycopg database {err}')
#     finally:
#         if conn is not None:
#             cursor.close()
#             conn.close()
#             logging.info('The connection/query was completed and closed.')
#
#             return resultDict

def getAgency(org_name):
    """Get all agency names from P&E database."""
    global conn, cursor
    resultDict = {}
    try:
        params = config()

        conn = psycopg2.connect(**params)

        if conn:
            logging.info(
                "There was a connection made to"
                "the database and the query was executed at getAgencies. "
            )

            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            query = f"select organizations_uid,name from organizations where name='{org_name}';"

            cursor.execute(query)

            result = cursor.fetchall()

            for row in result:
                theOrgUUID = row[0]
                theOrgName = row[1]

                resultDict[f"{theOrgUUID}"] = f"{theOrgName}"
            return resultDict

    except (Exception, psycopg2.DatabaseError) as err:
        logging.error(f"There was a problem logging into the psycopg database {err}")
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            logging.info("The connection/query was completed and closed.")

            return resultDict

def getSubdomain(domain):
    allsubs = []

    subdomains = sublist3r.main(domain, 40,None,None,False,False,False,None)
    for x in subdomains:
        if x != f'www{domain}':
            sub = x.split('.')
            lenDomain = len(sub)
            if lenDomain == 3:
                sub = sub[0]
                if sub != 'www' and sub not in allsubs:
                    allsubs.append(sub)
            elif lenDomain > 3:
                for subr in range(0,(lenDomain-1)):
                    sub1 = sub[0]
                    sub2 = sub[1]
                    if sub1 != 'www' and sub1 not in allsubs and sub2 not in allsubs:
                        sub1 = sub[0]
                        sub2 = sub[1]
                        allsubs.append(sub1)
                        allsubs.append(sub2)

    return allsubs

def getSubdomain1(domain):
    allsubs = []

    subdomains = sublist3r.main(domain, 40,None,None,False,False,False,None)
    subisolated = ''
    for sub in subdomains:

        if not sub.startswith('www.') and sub != None:

            # print(sub)
            subisolated = sub.rsplit('.')[:-2]
            # subisolated = sub.rsplit('.',2)[:-2]
            # print(f'The whole sub is {sub} and '
            #       f'the isolated sub is {subisolated}')
        allsubs.append(subisolated)

    return subdomains,allsubs

def verifyIPv4(custIP):
    """Verify if parameter is a valid ipv4 ip address."""
    try:
        if ip_address(custIP) :
            return True

        else:
            return False

    except ValueError as err:
        logging.error(f"The address is incorrect, {err}")
        return False

def theaddress(domain):
    """Get actual IP address of domain

    """

    gettheAddress = ''

    try:

        gettheAddress = socket.gethostbyname(domain)



    except socket.gaierror:
        pass
        logging.info('There is a problem with the Domain that you selected')

    return gettheAddress

def getallsubdomainIPS(domain):
    alladdresses = []
    alladdressesdict = {}
    for x in getSubdomain1(domain)[0]:
        if x != None:
            domainaddress = theaddress(x)
            # print(domainaddress)
            if domainaddress not in alladdresses and domainaddress != '':
                alladdresses.append(domainaddress)
            #     alladdressesdict[domain] = domainaddress
            # # print(f'The domain is {domain} the sub is {x} and the ip is {domainaddress}')
    return alladdresses, alladdressesdict




def verifyIPv4(custIP):
    try:
        if ip_address(custIP) or ip_network(custIP):
            return True

        else:
            return False

    except ValueError as err:
        logging.error(f'The address is incorrect, {err}')
        return False


def verifyCIDR(custIP):
    try:
        if ip_network(custIP):
            return True

        else:
            return False

    except ValueError as err:
        logging.error(f'The cidr is incorrect, {err}')
        return False

def getOrganizations():
    url = "https://api.cybersixgill.com/multi-tenant/organization"

    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Authorization': f'Bearer {getToken()}',
    }

    response = requests.get(url, headers=headers).json()
    return response


def getalluserinfo():
    standardUsersorgID = '61afca6a359f2cda0ab7670b'
    viewerRoleID = '5d23342df5feaf006a8a8929'
    userInfo = getOrganizations()[1]['assigned_users']

    return userInfo

def setNewCSGOrg(newOrgName,orgAliases,orgdomainNames,orgIP,orgExecs):
    newOrganization = json.dumps({"name": f"{newOrgName}",
                                  "organization_commercial_category": "customer",
                                  "countries": ["worldwide"],
                                  "industries": ["Government"]
                                  })
    url = f"https://api.cybersixgill.com/multi-tenant/organization"

    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Authorization': f'Bearer {getToken()}',
    }

    response = requests.post(url, headers=headers, data=newOrganization).json()

    newOrgID = response['id']

    if newOrgID:
        logging.info(f'Got here there is a new new org {newOrgID}')

        setOrganizationUsers(newOrgID)
        # setOrganizationDetails(newOrgID,
        #                        orgAliases,
        #                        orgdomainNames,
        #                        orgIP,
        #                        orgExecs)

    return response


def setOrganizationUsers(org_id ):
    print(len(getalluserinfo()))
    for user in getalluserinfo():
        userrole = user['role_id']
        user_id = user['user_id']
        username = user['user_name']


        if (userrole == '5d23342df5feaf006a8a8929') and (user_id != '610017c216948d7efa077a52') or userrole == '5d23342df5feaf006a8a8927' and user_id != '610017c216948d7efa077a52' :
            print(f'The userrole {userrole} and the user_id {user_id} and the user {username}')
            url = f"https://api.cybersixgill.com/multi-tenant/organization/{org_id}/user/{user_id}?role_id={userrole}"

            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
                'Authorization': f'Bearer {getToken()}',
            }

            response = requests.post(url, headers=headers).json()
            logging.info(response)


def setOrganizationDetails(org_id,orgAliases,orgDomain,orgIP,orgExecs):

    # print(org_id)
    # print(orgAliases)
    # print(orgDomain)
    # print(orgIP)
    # print(orgExecs)
    newOrganizationDetails = json.dumps({
        "organization_aliases": {"explicit": orgAliases},
        "domain_names": {"explicit": orgDomain},
        "ip_addresses": {"explicit": orgIP},
        "executives": {"explicit": orgExecs}
    })
    url = f"https://api.cybersixgill.com/multi-tenant/" \
          f"organization/{org_id}/assets"

    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Authorization': f'Bearer {getToken()}',
    }

    response = requests.put(url, headers=headers,
                            data=newOrganizationDetails).json()
    logging.info(f'The response is {response}')

def getRootID(org_UUID):
    """Get all agency names from P&E database."""
    global conn, cursor
    resultDict = {}
    try:
        params = config()

        conn = psycopg2.connect(**params)

        if conn:
            logging.info(
                "There was a connection made to the database and the query was executed "
            )

            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query = f"select root_domain_uid, organization_name from" \
                    f" root_domains where organizations_uid='{org_UUID}';"

            cursor.execute(query)

            result = cursor.fetchall()

            for row in result:
                theRootUUID = row[0]
                theOrgName = row[1]

                resultDict[f"{theOrgName}"] = f"{theRootUUID}"
            return resultDict

    except (Exception, psycopg2.DatabaseError) as err:
        logging.error(f"There was a problem logging into the psycopg database {err}")
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            logging.info("The connection/query was completed and closed.")

            return resultDict




def main():
    import glob
    logging.info('Program starting...')
    neworgname = 'BLAH'
    aliases = ['fake','alias']
    domain = ['flightschoolcandidates.gov','tsa.gov']
    theips = ['107.85.192.20/32','107.85.192.126/32']
    theexecs = ['jerry springer', 'Walter cool']
    print(theaddress('irs.gov'))
    # print(getSubdomain1('ice.gov')[1])
    # print('is this working')
    # for dom in domain:
    #     for px in getallsubdomainIPS(dom)[0]:
    #         print(px)
    # getSubdomain1('lacity.org')


    # list(getAgencies(neworgname).keys())[0]
    # print(getAgencies('BLAH'))
    # for x in lookfile:
    #     print(x.endswith('ics.py'))
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # lookfile = glob.glob(f'{basedir}/*.py')
    # basedir1 = os.path.abspath(os.path.dirname(__file__) + "/app.py")
    # print(basedir)
    # print(lookfile)
    # params = config1()
    #
    # print(params)




    # print(getalluserinfo())
    # userrole = ''
    # user_id = ''
    # for user in getalluserinfo():
    #
    #         userrole = user['role_id']
    #         user_id = user['user_id']
    #         username = user['user_name']
    #         # userrole == '5d23342df5feaf006a8a8927' #userid for owner
    #         if (userrole == '5d23342df5feaf006a8a8929') and (user_id != '610017c216948d7efa077a52') or userrole == '5d23342df5feaf006a8a8927' and user_id != '610017c216948d7efa077a52':
    #             print(f'The userrole {userrole} and the user_id {user_id} and the user {username}')





    # setNewCSGOrg(neworgname,aliases,domain,theips,theexecs)
    # amiconnected()
    # if verifyIPv4('199.173.224.0/21') or verifyCIDR('199.173.224.12'):
    #     print('Good')



if __name__ == '__main__':
    main()
