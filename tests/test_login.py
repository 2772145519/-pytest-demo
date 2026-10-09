import pytest
from src.testqingqiu import Apiclient

class TestLogin:

    VALID_USERNAME = 'admin'
    VALID_PASSWORD = 'HM 2023_test'

    @pytest.fixture(scope='function')
    def client(self):
        client = Apiclient()
        yield  client
        client.close()

    @pytest.fixture(scope='function')
    def captcha_info(self,client):

        respoense = client.get_captcha()
        assert respoense.status_code ==200
        data = respoense.json()
        return {"uuid":data["uuid"]}

    def test_login_success(self,client:Apiclient,captcha_info:dict):

        username = 'admin'
        password = 'HM_2023_test'
        uuid = captcha_info["uuid"]
        respoense = client.login(username,password,"2",uuid)
        assert respoense.status_code == 200
        data = respoense.json()
        assert data["code"] == 200
        assert data["msg"] == "操作成功"
        assert "token" in data
        assert data["token"] is not None and data["token"]  != ""

        print(f"登录成功,token:{data['token'][:20]}..")

    def test_login_fail1(self, client: Apiclient, captcha_info: dict):

        username = "admin"
        password = "wrong_password"
        uuid = captcha_info["uuid"]
        response = client.login(username, password, "2", uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("密码错误")

    def test_login_fail2(self, client: Apiclient, captcha_info: dict):

        username = "wrong_admin"
        password = "password"
        uuid = captcha_info["uuid"]
        response = client.login(username, password, "2", uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("用户名错误")

    def test_login_fail_kong1(self,client:Apiclient,captcha_info:dict):

        username = "admin"
        password = " "
        uuid = captcha_info["uuid"]
        response = client.login(username, password, "2", uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("密码为空")

    def test_login_fail_kong2(self,client:Apiclient,captcha_info:dict):
        username = " "
        password = "HM_2023_test"
        uuid = captcha_info["uuid"]
        response = client.login(username, password, "2", uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("用户名为空")

    def test_login_fail3(self, client: Apiclient, captcha_info: dict):

        username = "admin"
        password = "password"
        code = "42"
        uuid = captcha_info["uuid"]
        response = client.login(username, password,code, uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "验证码错误"
        print("验证码错误")

    def test_login_kong3(self, client: Apiclient, captcha_info: dict):

        username = "admin"
        password = "password"
        code = " "
        uuid = captcha_info["uuid"]
        response = client.login(username, password,code, uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "验证码错误"
        print("验证码为空")