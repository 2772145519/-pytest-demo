import time
import pytest


class TestContract:
    """合同管理 测试类。"""

    @pytest.mark.smoke
    def test_add_and_query_contract(self, logged_in_client, created_course_id):
        """新增合同 + 查询新增的合同。"""
        # created_course_id 夹具已创建好一门课，拿它的 id（合同必须挂在一门课上）
        course_id = created_course_id

        # 1) 准备合同数据（合同编号、手机号用时间戳保证唯一，避免重复）
        contract_no = f"HT{int(time.time())}"
        phone = f"138{str(int(time.time()))[-8:]}"  # 拼成 11 位手机号

        print(f"\n 合同编号={contract_no}，手机号={phone}，课程id={course_id}")

        # 2) 新增合同（调用封装好的 add_contract 方法）
        response = logged_in_client.add_contract(
            contract_no=contract_no,
            phone=phone,
            name="测试客户",
            subject="6",            # 意向学科
            course_id=course_id,    # 课程 id（必填）
            file_name="/profile/upload/test.png",  # 文件名称（必填，占位）
            channel="0",            # 渠道来源：0=线上活动
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200, f"新增合同失败：{data.get('msg')}"
        print("   新增合同成功")

        # 3) 按手机号查询，验证合同真的新增成功（调用封装好的 get_contract_list 方法）
        list_response = logged_in_client.get_contract_list(phone=phone)
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert list_data["code"] == 200
        assert list_data.get("total", 0) >= 1, "新增的合同没查到"
        found = list_data["rows"][0]
        assert found["contractNo"] == contract_no, f"合同编号不对：{found['contractNo']} != {contract_no}"
        print(f"   查询到合同：合同编号={found['contractNo']}，客户={found['name']}")