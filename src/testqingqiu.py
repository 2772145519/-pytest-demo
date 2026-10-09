import requests

class Apiclient(object):
    base_url = "https://kdtx-test.itheima.net"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "user-agent":"Mozilla/5.0",
            "content-type":"application/json"
        }

    def set_token(self, token):

        self.token = token  # 存 token
        self.headers["Authorization"] = f"Bearer {self.token}"

    def get_captcha(self):
        url = self.base_url+'/api/captchaImage'
        respoense = self.session.get(url,headers=self.headers)
        return  respoense

    def login(self, username, password,code,uuid):

        url = self.base_url+'/api/login'

        data={
            "username":username,
            "password":password,
            "code": code,
            "uuid": uuid
        }

        respoense = self.session.post(url,json=data,headers=self.headers)
        return respoense

    def add_course(self,name,subject,price,applicableperson,info=""):
        url = self.base_url + '/api/clues/course'
        data = {
            "name": name,
            "subject":subject,
            "price":price,
            "applicableperson":applicableperson,
            "info":info,
        }

        respoense = self.session.post(url,json=data,headers=self.headers)
        return respoense

    def get_course_list(self,name="",subject="",price="",applicableperson="",info=""):
        url = self.base_url + '/api/clues/course/list'
        params = {}
        if name:
            params["name"] = name
        if subject:
            params["subject"] = subject
        if price:
            params["price"] = price
        if applicableperson:
            params["applicableperson"] = applicableperson
        if info:
            params["info"] = info

        respoense = self.session.get(url,params=params,headers=self.headers)
        return respoense

    def get_course_by_id(self,course_id):

        url = self.base_url + f'/api/clues/course/{course_id}'
        respoense = self.session.get(url,headers=self.headers)
        return respoense

    def delete_course(self, course_id):
        url = self.base_url + f'/api/clues/course/{course_id}'  # 删除课程的接口地址
        response = self.session.delete(url, headers=self.headers)  # 用 DELETE 方法
        return response

    def update_course(self, course_id, name="", subject="", price=None, applicable_person="", info=""):

        url = self.base_url + '/api/clues/course'  # 修改课程的接口地址
        data = {
            "id": course_id,
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson": applicable_person,
            "info": info,
        }
        # 修改用 PUT 方法，参数放 body（json=）
        response = self.session.put(url, json=data, headers=self.headers)
        return response

    def add_lead(self, name, id, sex):
        url = f"{self.base_url}/api/clues/clue"
        data = {
            "name": name,
            "id": id,
            "sex": sex
        }
        response = self.session.post(url, json=data, headers=self.headers)
        return response

    def check_lead_list(self, name=None, id=None, sex=None):
        url = f"{self.base_url}/api/clues/clue/list"
        data = {
            "name": name,
            "id": id,
            "sex": sex
        }
        response = self.session.get(url, json=data, headers=self.headers)
        return response

    def add_contract(self, contract_no, phone, name, subject, course_id, file_name, channel="", activity_id=None):
        url = self.base_url + '/api/contract'
        data = {
            "contractNo": contract_no,
            "phone": phone,
            "name": name,
            "subject": subject,
            "courseId": course_id,
            "fileName": file_name,
            "channel": channel,
            "activityId": activity_id,
        }
        response = self.session.post(url, json=data, headers=self.headers)
        return response

    def get_contract_list(self, name="", phone="", contract_no="", subject="", course_id=None, channel="",
                          activity_id=None, file_name=""):
        url = self.base_url + '/api/contract/list'  # 查询合同列表接口地址
        params = {}
        if name:
            params["name"] = name
        if phone:
            params["phone"] = phone
        if contract_no:
            params["contractNo"] = contract_no
        if subject:
            params["subject"] = subject
        if course_id is not None:
            params["courseId"] = course_id
        if channel:
            params["channel"] = channel
        if activity_id is not None:
            params["activityId"] = activity_id
        if file_name:
            params["fileName"] = file_name
        response = self.session.get(url, params=params, headers=self.headers)
        return response

    def upload_file(self, file_path):
        import os
        url = self.base_url + '/api/common/upload'
        file_name = os.path.basename(file_path)
        print(">>> 实际请求的 upload url =", url)


        headers = {
            "Authorization": self.headers["Authorization"],
             # "User-Agent": self.headers["User-Agent"],
        }
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f)}
            response = self.session.put(url, files=files, headers=headers)
        return response

    def close(self):
        """关闭会话，释放连接资源。"""
        self.session.close()

