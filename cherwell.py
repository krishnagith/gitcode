import requests
baseUri = "http://ic2tstcsm01.hcf.local/CherwellAPI/"

def logintoken():
    clientId = "6abf6256-2d6d-4982-a63f-b7ff52087cfd"
    userName = "CSDAPI"
    password = "Passw0rd"

    tokenUri = baseUri + "token"
    authMode = "Internal"
    tokenRequestBody = {"grant_type": "password", "client_id": clientId,
                        "username": userName, "password": password}

    r_login = requests.post('http://ic2tstcsm01.hcf.local/CherwellAPI/token', data=tokenRequestBody, verify=False)

    print(r_login.status_code)
    if r_login.status_code != requests.codes.ok:
        print("not OK")
        return "notok"
    else:
        accessToken = r_login.json()["access_token"]
        header = {'Authorization': 'Bearer ' + accessToken}
        return header

def getservicceinfo():
    serviceInfo = requests.get(baseUri + '/api/V1/serviceinfo', headers=header, verify=False)
    print(serviceInfo.json())

def getincident():
    incidentinfo = requests.get(baseUri + '/api/V1/getbusinessobjectsummary/busobname/Incident',
                                headers=header, verify=False)
    results =incidentinfo.json()
    busobid=results[0]['busObId']
    endoint='/api/V1/getbusinessobject/{}/publicid/'.format(busobid)
    print(busobid)
    incidents = requests.get(baseUri + endoint, headers=header, verify=False)
    print(incidents)


if __name__ == '__main__':
    headerbuild = logintoken()
    if headerbuild != "notok":
        header = headerbuild
    else:
        print("header build is not successful, please check login to the api service")
        exit(1)
    getincident()
