import pytest
from data.add_clue_test import ADD_clue_DATA

class Testlead:
    @pytest.mark.parametrize("case",ADD_clue_DATA)
    def test_add_lead(self,logged_in_client,case):
        id = case["id"]
        name = case["name"]
        sex = case["sex"]

        response = logged_in_client.add_lead(
            id=id,
            name=name,
            sex=sex
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

        c_response = logged_in_client.check_lead_list(id=id,name=name,sex=sex)
        c_data = c_response.json()
        assert c_data["code"] == 200

