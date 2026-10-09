from random import random

import pytest  # 导入测试框架
from src.testqingqiu import Apiclient

@pytest.fixture(scope="function")
def client():

    client = Apiclient()
    yield client
    client.close()

@pytest.fixture(scope="function")
def captcha_info(client):


    response = client.get_captcha()
    assert response.status_code == 200
    data = response.json()
    return {
        "code": "2",
        "uuid": data["uuid"],
    }

@pytest.fixture(scope="function")
def logged_in_client(client, captcha_info):

    code = captcha_info["code"]
    uuid = captcha_info["uuid"]

    response = client.login("admin", "HM_2023_test", code, uuid)
    assert response.status_code == 200
    data = response.json()

    assert data["code"] == 200, f"登陆失败：{data.get('msg')}"
    client.set_token(data["token"])
    print(f"\n自动登陆成功，token:{client.token[:30]}...")

    return client

@pytest.fixture(scope="function")
def created_course_id(logged_in_client):
    import time
    course_name = f"测试课程_{int(time.time())}"


    response = logged_in_client.add_course(
        name=course_name,
        subject="6",
        price=888,
        applicableperson="2",
        info="由fixture创建的测试课程"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200, f"创建课程失败{data.get('msg')}"

    list_response = logged_in_client.get_course_list(name=course_name)
    list_data = list_response.json()

    if list_data.get("rows") and len(list_data["rows"]) > 0:
        course_id = list_data["rows"][0]["id"]
        print(f"\n创建测试课程成功，ID：{course_id}")
        return course_id
    else:
        pytest.fail("无法获取创建课程ID")

@pytest.fixture(scope="function")
def create_lead(login_client):
    name = "王五"
    response = login_client.add_lead(
        name=name,
        id = random.randint(4,10),
        sex="1"
    )
    data = response.json()
    assert data["code"] == 200

    l_response = login_client.check_lead_list(name=name)
    l_data = l_response.json()
    print(name,l_response,l_data)

    if l_data.get("rows") and len(l_data["rows"]) > 0:
        id = l_data["rows"][0]['id']
        return id
    else:
        print("解析失败")