import requests
from urllib3.util import url

url = "http://kdtx-test.itheima.net/api/captchaImage"
respoense = requests.get(url)


headers= {
    "user-agent":"Mozilla/5.0",
    "content-type":"application/json"
}

respoense=requests.get(url,headers=headers)
print("状态码",respoense.status_code)
print("响应头",respoense.headers)
print("响应内容",respoense.text[:200])
print("json数据",respoense.json())


if respoense.status_code == 200:
    try:
        data = respoense.json()
        print("json数据:",data)
        code = data["code"]
        uuid = data["uuid"]
        print(f"验证文字:{code}")
        print(f"唯一标识:{uuid}")

    except Exception as e:
        print("json解析失败",e)


else:
    print(f"请求失败,状态码:{respoense.status_code}")



#登录
url = "http://kdtx-test.itheima.net/api/login"

data = {
    "username":"admin",
    "password":"HM_2023_test",
    "code":2,
    "uuid":uuid
}

respoense_login = requests.post(url,json=data,headers=headers)

print(respoense_login.status_code)

if respoense_login.status_code == 200:
    respoense_result = respoense_login.json()
    if respoense_result.get("code") == 200:
        token = respoense_result.get("token")
        msg= respoense_result.get("msg")
        code = respoense_result.get("code")
        print("操作成功",)
        print("操作成功返回的token：",token)
        print("操作成功返回的msg：",msg)
        print("操作成功返回的code：",code)

    else:
        print("操作失败",respoense_login.status_code)


















