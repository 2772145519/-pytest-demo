import pytest
from data.add_course_test import ADD_COURSE_TEST_DATA,QUERY_COURSE_TEST_DATA

class TestCourseAdd:
    @pytest.mark.parametrize("test_case", ADD_COURSE_TEST_DATA)
    def test_add_course_data_driven(self, logged_in_client, test_case):


        test_id = test_case["id"]
        description = test_case["description"]
        course = test_case["course"]
        experience = test_case["experience"]    
        check_exists = test_case.get("check_exists", False)

        print(f"\n{'=' * 60}")
        print(f"执行测试用例：{test_id}-{description}")
        print(f"请求参数：{course}")

        response = logged_in_client.add_course(
            name=course["name"],
            subject=course["subject"],
            price=course["price"],
            applicableperson=course["applicableperson"],
            info=course.get("info", ""),
        )

        assert response.status_code == 200  # HTTP 状态码 200
        data = response.json()             # 把响应体解析成字典
        print(f"响应数据：{data}")

        # 断言业务状态码和提示信息，和期望一致
        assert data["code"] == experience["code"], \
            f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
        if "msg" in experience:  # 期望里写了 msg 才校验
            assert data["msg"] == experience["msg"], \
                f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        print(f"✅ 断言通过: code={data['code']}, msg={data['msg']}")

        # ---- 第 4 步：如果需要，验证课程是否真的添加成功 ----
        if check_exists and experience["code"] == 200:
            # 用课程名称去查列表，确认能查到刚添加的课程
            list_response = logged_in_client.get_course_list(name=course["name"])
            list_data = list_response.json()


            assert list_data["code"] == 200  # 查询接口业务成功
            # 列表接口返回 {"total":N, "rows":[...]}，rows 是课程数组
            print(list_response.status_code)
            assert len(list_data.get("rows", [])) > 0, \
                f"课程 '{course['name']}' 未在列表中找到"

            # 验证查到的第一条课程信息是否正确
            found_course = list_data["rows"][0]
            assert found_course["name"] == course["name"], \
                f"课程名称不匹配: {found_course['name']} != {course['name']}"
            assert found_course["price"] == course["price"], \
                f"课程价格不匹配: {found_course['price']} != {course['price']}"

            course_id = found_course["id"]
            print(f"✅ 验证通过: 课程已存在，ID={course_id}")
        print(f"✅ 用例 {test_id} 通过!")



class TestCourseAdd2:
    # ... 你原有的 test_add_course_data_driven 保持不变 ...

    @pytest.mark.parametrize("test_case", QUERY_COURSE_TEST_DATA)
    def test_query_course_data_driven(self, logged_in_client, test_case):
        test_id = test_case["id"]
        description = test_case["description"]
        params = test_case["params"]          # 查询参数字典，可能为空 {}
        experience = test_case["experience"]  # 期望结果

        print(f"\n{'=' * 60}")
        print(f"执行测试用例：{test_id}-{description}")
        print(f"查询参数：{params}")

        # 直接把参数字典展开传给接口，params={} 时就是不传任何条件
        response = logged_in_client.get_course_list(**params)

        assert response.status_code == 200, \
            f"用例 {test_id} 失败: HTTP 状态码={response.status_code}"

        data = response.json()
        print(f"响应数据：{data}")

        # 业务状态码断言
        assert data["code"] == experience["code"], \
            f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"

        # 提示信息断言（如果期望里有 msg 才校验）
        if "msg" in experience:
            assert data["msg"] == experience["msg"], \
                f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        # 是否有数据断言
        if experience.get("has_data"):
            rows = data.get("rows", [])
            assert len(rows) > 0, f"用例 {test_id} 失败: 期望查询到数据，实际 rows 为空"

            # 如果传了 name 参数，顺便校验查出来的课程名是否匹配
            if "name" in params:
                for row in rows:
                    assert row["name"] == params["name"], \
                        f"用例 {test_id} 失败: 期望课程名={params['name']}，实际={row['name']}"

            print(f"✅ 查询到 {len(rows)} 条数据")

        print(f"✅ 用例 {test_id} 通过!")


