import pytest

from src.testqingqiu import Apiclient
from data.login_test import login_test_data

class Test_login_data_Driven:

    correct_captcha = "2"

    @pytest.fixture(scope="function")
    def login_client(self):
        login_client = Apiclient()
        yield login_client
        login_client.close()

    @pytest.fixture(scope="function")
    def captcha_client(self,login_client):
        response = login_client.get_captcha()
        assert response.status_code == 200
        data = response.json()
        return {"uuid":data["uuid"]}


    @pytest.mark.parametrize("login_test",login_test_data)
    def test_login_data_driven(self, login_client, captcha_client, login_test):
        test_id = login_test["id"]
        description = login_test["description"]
        username = login_test["username"]
        password = login_test["password"]
        code_type = login_test["code_type"]
        expected_code = login_test["expected_code"]
        expected_msg = login_test.get("expected_msg")
        check_token = login_test.get("check_token",False)

        code = self.correct_captcha if code_type == "correct" else "9999"
        uuid = captcha_client["uuid"]
        print(f"\n执行用例:{test_id}-{description}")
        response = login_client.login(
            username=username,
            password=password,
            uuid=uuid,
            code=code,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"]  == expected_code,\
        f"用例{test_id}失败:期望 msg={expected_msg},实际 msg = {data['msg']}"
        if expected_msg:
            assert expected_msg in data["msg"], \
                f"用例{test_id}失败: 期望 msg包含={expected_msg}, 实际 msg={data['msg']}"

            # 【修改这里】使用 check_token 变量来判断是否校验 token
        if check_token:
            assert "token" in data
            assert data["token"] is not None and data["token"] != ""
            print(f"token:{data['token'][:30]}...")
        else:
            # 反向用例通常不需要断言没有 token，因为之前已经断言了msg。
            # 如果严格点，可以断言 token 不存在或为空（视后端返回而定）
            pass

        print(f"用例{test_id}通过")










