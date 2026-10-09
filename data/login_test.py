login_test_data = [
    {
        "id":"test001",
        "description":"正确的用户名+正确的密码+正确的验证码,登录成功",
        "username": "admin",
        "password":"HM_2023_test",
        "code_type":"correct",
        "expected_code": 200,
        "expected_msg":"操作成功",
        "check_token":True
    },
    {
        "id":"test002",
        "description":"为空的用户名+正确的密码+正确的验证码,登录失败",
        "username": " ",
        "password":"HM_2023_test",
        "code_type":"correct",
        "expected_code": 500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False
    },
    {
        "id":"test003",
        "description":"正确的用户名+为空的密码+正确的验证码,登录失败",
        "username": "admin",
        "password":" ",
        "code_type":"correct",
        "expected_code": 500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False
    },
    {
        "id":"test004",
        "description":"错误的的用户名+正确的密码+正确的验证码,登录失败",
        "username": "admin666",
        "password":"HM_2023_test",
        "code_type":"correct",
        "expected_code": 500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False
    },
    {
        "id":"test005",
        "description":"正确的用户名+错误的密码+正确的验证码,登录失败",
        "username": "admin",
        "password":"HM_2023_test666",
        "code_type":"correct",
        "expected_code": 500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False
    },
    {
        "id":"test006",
        "description":"正确的用户名+正确的密码+错误的验证码,登录失败",
        "username": "admin",
        "password":"HM_2023_test",
        "code_type":"wrong",
        "expected_code": 500,
        "expected_msg":"验证码错误",
        "check_token":False
    }
]