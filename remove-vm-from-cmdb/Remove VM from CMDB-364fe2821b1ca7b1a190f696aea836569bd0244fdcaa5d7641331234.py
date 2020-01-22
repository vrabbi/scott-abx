import json
import requests
def handler(context, inputs):
    url = "http://" + inputs["i-doit-FQDNorIP"] + "/src/jsonrpc.php"
    idoit_apiKey = inputs["i-doit-apiKey"]
    idoit_user = inputs["i-doit-user"]
    idoit_password = inputs["i-doit-password"]
    payload = {"version": "2.0","method": "idoit.login","params": {"apikey": idoit_apiKey,"language": "en"},"id": 1}
    headers = {"Accept":"application/json","Content-Type":"application/json","X-RPC-Auth-Username": idoit_user,"X-RPC-Auth-Password": idoit_password}
    results = requests.post(url,json=payload,headers=headers)
    sessionID = results.json()["result"]["session-id"]
    print(sessionID)
    headers = {"Accept":"application/json","Content-Type":"application/json","X-RPC-Auth-Session": sessionID}
    objID = inputs["customProperties"]["cmdbObjectID"]
    payload = {"version": "2.0","method": "cmdb.object.delete","params": {"id": objID,"status": "C__RECORD_STATUS__ARCHIVED","apikey": idoit_apiKey,"language": "en"},"id": 1}
    results = requests.post(url,json=payload,headers=headers)
    '''
    print(results.text)
    '''