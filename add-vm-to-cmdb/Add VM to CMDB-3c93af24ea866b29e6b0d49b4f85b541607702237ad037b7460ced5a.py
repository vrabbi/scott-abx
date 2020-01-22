import json
import requests
def handler(context, inputs):
    baseUri = "https://" + inputs["vra-FQDNorIP"]
    vra_user = inputs["vra-user"]
    vra_password = inputs["vra-password"]
    url = baseUri + "/csp/gateway/am/api/login?access_token"
    headers = {"Accept":"application/json","Content-Type":"application/json"}
    payload = {"username": vra_user,"password": vra_password}
    results = requests.post(url,json=payload,headers=headers,verify=False)
    casToken = results.json()["refresh_token"]
    print(casToken)
    url = baseUri + "/iaas/login"
    headers = {"Accept":"application/json","Content-Type":"application/json"}
    payload = {"refreshToken":casToken}
    results = requests.post(url,json=payload,headers=headers,verify=False)
    bearer = "Bearer "
    bearer = bearer + results.json()["token"]
    deploymentId = inputs['deploymentId']
    resourceId = inputs['resourceIds'][0]
    print("deploymentId: "+ deploymentId)
    print("resourceId:" + resourceId)
    machineUri = baseUri + "/iaas/machines/" + resourceId
    headers = {"Accept":"application/json","Content-Type":"application/json", "Authorization":bearer }
    resultMachine = requests.get(machineUri,headers=headers,verify=False)
    memGB = str(int(json.loads(resultMachine.text)["customProperties"]["memoryInMB"])  / 1024)
    cpuCount = json.loads(resultMachine.text)["customProperties"]["cpuCount"]
    print("machine: " + resultMachine.text)
    print( "serviceNowCPUCount: "+ cpuCount)
    print( "serviceNowMemoryInGB: "+ memGB)
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
    name = inputs["resourceNames"][0]
    storageGB = inputs["customProperties"]["provisionGB"]
    os = json.loads(resultMachine.text)["customProperties"]["softwareName"]
    idoit_VRA_VM_TypeID = inputs["i-doit-VRA-VM-TypeID"]
    payload = {"jsonrpc":"2.0","method":"cmdb.object.create","params":{"type":idoit_VRA_VM_TypeID,"title":name,"description":"STORAGE: " + storageGB + "GB    OS: " + os + "    CPU: " + cpuCount + "    RAM: " + memGB + "GB","apikey":idoit_apiKey},"id":1}
    print(json.dumps(payload, indent = 2))
    results = requests.post(url,json=payload,headers=headers)
    objID = int(results.json()["result"]["id"])
    ipAddress = inputs["addresses"][0][0]
    payload = {"jsonrpc":"2.0","method":"cmdb.category.create","params":{"objID":objID,"data": {"ipv4_address":str(ipAddress),"hostname":name},"category":"C__CATG__IP","apikey":idoit_apiKey},"id":1}
    print(json.dumps(payload, indent = 2))
    results = requests.post(url,json=payload,headers=headers)
    print(results.text)
    payload = {"jsonrpc":"2.0","method":"cmdb.category.create","params":{"objID":objID,"data": {"cores":int(cpuCount)},"category":"C__CATG__CPU","apikey":idoit_apiKey},"id":1}
    print(json.dumps(payload, indent = 2))
    results = requests.post(url,json=payload,headers=headers)
    print(results.text)
    payload = {"jsonrpc":"2.0","method":"cmdb.category.create","params":{"objID":objID,"data": {"capacity":float(memGB),"quantity":1},"category":"C__CATG__MEMORY","apikey":idoit_apiKey},"id":1}
    print(json.dumps(payload, indent = 2))
    results = requests.post(url,json=payload,headers=headers)
    print(results.text)
    outputs = {}
    outputs['customProperties'] = inputs['customProperties']
    outputs['customProperties']['cmdbObjectID'] = objID
    return outputs