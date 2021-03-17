import requests
import pandas as pd

import urllib3

urllib3.disable_warnings()
endpoint = 'https://ic2mfttstmgr01:8443/automation-api'


def logintoken():
    user = 's_kreddy'
    password = 'DAw1whD!252!'

    r_login = requests.post(endpoint + '/session/login', json={"username": user, "password": password}, verify=False)
    print(r_login.content)

    print(r_login.status_code)
    if r_login.status_code != requests.codes.ok:
        print("not OK")
        return "notok"
    else:
        token = r_login.json()['token']
        header = {'Authorization': 'Bearer ' + token}
        return header


def userCreate(user):
    r_userCreate = requests.post(endpoint + '/config/mft/externaluser',
                                 json=user, headers=header, verify=False)
    print(r_userCreate.json())


def virtualfolder(folder):
    r_userCreate = requests.post(endpoint + '/config/mft/virtualfolder',
                                 json=folder, headers=header, verify=False)
    print(r_userCreate.json())


def inputdata():
    filein = "Partialusers.xlsx"
    data = pd.read_excel(filein)
    datadict = data.to_dict(orient='record')

    return datadict


def processmapping():
    userslist = inputdata()

    for user in userslist:
        json_user = {}
        json_user["name"] = user["PROVIDER_NUMBER"]
        json_user["email"] = user["EMAIL_ADDRESS"]
        json_user["company"] = "Provider Portal"
        json_user["password"] = user["PASSWORD"]
        userCreate(json_user)

    for user in userslist:
        json_folder = {}
        json_folder["name"] = user["PROVIDER_NUMBER"]
        json_folder["authorizedExternalUsersAndGroups"] = [user["PROVIDER_NUMBER"]]
        json_folder["authorizedInternalUsers"] = ["*"]
        json_folder["blockedFilePattern"] = "*.exe"
        virtualfolder(json_folder)

def getusers():
    searchuser = requests.get(endpoint + '/config/mft/externalusers?company=Eyecare', headers=header,
                              verify=False)
    print(searchuser.json())

def deleteuser():
    # / config / mft / externaluser / {username}
    userslist = inputdata()
    for user in userslist:
        json_user = user["PROVIDER_NUMBER"]
        enduser = '/config/mft/externaluser/{}'.format(json_user)
        endfolder = '/config/mft/virtualfolder/{}'.format(json_user)
        deletestatus = requests.delete(endpoint + enduser, headers=header, verify=False)
        deletestatusfolder = requests.delete(endpoint + endfolder, headers=header, verify=False)
        print(deletestatus.json(), deletestatusfolder.json())

if __name__ == '__main__':
    headerbuild = logintoken()
    if headerbuild != "notok":
        header = headerbuild
    else:
        print("header build is not successful, please check login to the api service")
        exit(1)
    logintoken()




