ADD_COURSE_TEST_DATA =[
    {
        "id":"TEST_COURSE_ADD_001",
        "description":"正常添加课程--成功",
        "course":{
            "name":"自动化测试实战课9565",
            "subject":"6",
            "price":900,
            "applicableperson":"2",
            "info":"从零开始学习自动化测试"

        },
        "experience":{
            "code":200,
            "msg":"操作成功"
        },
        "check_exists":True #添加后验证课程是否存在
    }

]

# ================查询课程测试数据================
QUERY_COURSE_TEST_DATA = [
    {
        "id":"TEST_COURSE_ADD_001",
        "description":"查询所有课程--成功（不传任何参数）",
        "params":{},
        "experience":{
            "code":200,
            "msg":"查询成功",
            "has_data":True
        }
    },
{
        "id":"TEST_COURSE_ADD_002",
        "description":"按课程名称查询--成功",
        "params":{
            "name":"自动化测试实战课9565"
        },
        "experience":{
            "code":200,
            "msg":"查询成功",
            "has_data":True
        }
    },
]