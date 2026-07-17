# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description: RedfishFunc Class
#
#   @author: zhong
#   @Date:
#=========================================================================
'''

from requests.auth import HTTPBasicAuth




def getChassisID(client):
    JSON = {}
    response = client.request("GET", "redfish/v1/Chassis",
                              auth=HTTPBasicAuth(client.username, client.passcode))
    if response is None:
        JSON['code'] = 1
        JSON['data'] = 'response is none'
    elif response.status_code == 200:
        try:
            result = response.json()
            JSON['code'] = 0
            JSON['data'] = result.get('Members')
        except Exception as e:
            JSON['code'] = 1
            JSON['data'] = e
    else:
        try:
            res = response.json()
            JSON['code'] = 2
            JSON['data'] = 'request failed, response content: ' + str(
                res["error"]["message"]) + ' the status code is ' + str(response.status_code) + "."
        except:
            JSON['code'] = 1
            JSON['data'] = 'request failed, response status code is ' + str(response.status_code)
    return JSON


def getPCIEDevices(client, chassis_id):
    JSON = {}
    response = client.request("GET", "%s/PCIeDevices" % str(chassis_id)[1:],
                              auth=HTTPBasicAuth(client.username, client.passcode))
    if response is None:
        JSON['code'] = 1
        JSON['data'] = 'response is none'
    elif response.status_code == 200:
        try:
            result = response.json()
            JSON['code'] = 0
            JSON['data'] = result.get('Members')
        except Exception as e:
            JSON['code'] = 1
            JSON['data'] = e
    else:
        try:
            res = response.json()
            JSON['code'] = 2
            JSON['data'] = 'request failed, response content: ' + str(
                res["error"]["message"]) + ' the status code is ' + str(response.status_code) + "."
        except:
            JSON['code'] = 1
            JSON['data'] = 'request failed, response status code is ' + str(response.status_code)
    return JSON


def getPCIEInfo(client, url):
    JSON = {}
    response = client.request("GET", url, auth=HTTPBasicAuth(client.username, client.passcode))
    if response is None:
        JSON['code'] = 1
        JSON['data'] = 'response is none'
    elif response.status_code == 200:
        try:
            result = response.json()
            JSON['code'] = 0
            JSON['data'] = result
        except Exception as e:
            JSON['code'] = 1
            JSON['data'] = e
    else:
        try:
            res = response.json()
            JSON['code'] = 2
            JSON['data'] = 'request failed, response content: ' + str(
                res["error"]["message"]) + ' the status code is ' + str(response.status_code) + "."
        except:
            JSON['code'] = 1
            JSON['data'] = 'request failed, response status code is ' + str(response.status_code)
    return JSON


def login(client):
    data = {
        "UserName": str(client.username),
        "Password": str(client.passcode),
        "SessionTimeOut": "600"
    }
    headers = {'Content-Type': 'application/json'}
    header = {}
    # print('responds')
    responds = client.request('POST', 'redfish/v1/SessionService/Sessions', headers=headers, json=data, data=None)
    login_id = ''
    try:
        if responds is not None:
            if responds.status_code == 201:  # 登录成功
                XCSRFToken = responds.headers['X-Auth-Token']
                header = {
                    "X-Auth-Token": XCSRFToken,
                }
                login_id = responds.json()['Id']
    except Exception as e:
        login_id = "login error, " + str(e)
    return header, login_id


def logout(client, login_id, login_header):
    token = login_header.get('X-Auth-Token')
    headers = {"X-Auth-Token": token}
    # headers = {'Content-Type': 'application/json'}
    responds = client.request("DELETE", "redfish/v1/SessionService/Sessions/" + str(login_id), headers=headers)
    # print(responds)




def remoteFWUpdate(client, data):
    JSON = {}
    response = client.request("POST", "redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate", json=data,
                              auth=HTTPBasicAuth(client.username, client.passcode))
    if response is None:
        JSON['code'] = 1
        JSON['data'] = 'response is none'
    elif response.status_code == 204 or response.status_code == 200:
        JSON['code'] = 0
        JSON['data'] = ""
    else:
        try:
            res = response.json()
            JSON['code'] = 2
            JSON['data'] = 'request failed, response content: ' + str(res["error"]["message"]) + ' the status code is ' + str(response.status_code) + "."
        except:
            JSON['code'] = 1
            JSON['data'] = 'request failed, response status code is ' + str(response.status_code)
    return JSON
