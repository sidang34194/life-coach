"""Supabase 数据库操作 - 自动探测版"""  
import streamlit as st  
import requests  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 准备两个项目的组合（URL + 对应的 Key）  
        configs = [  
            ("https://ydrypovzrfvmotlsaomw.supabase.co/rest/v1 ", "sb_secret_B4kQHMkT3BHSN-K-lGIISw_7dVuYO0K"),  
            ("https://zgyzjxryvlgwzqkqfkoo.supabase.co/rest/v1 ", "sb_secret_1Bi1unY-W2GkrzhDgKfqlw_M0GjMQXB")  
        ]  
          
        self.url = ""  
        self.api_key = ""  
        self.is_online = False  
        self.error_msg = "正在探测..."  
          
        print("DEBUG: 开始探测数据库...")  
          
        # 循环尝试，直到找到一个有 users 表的数据库  
        for u, k in configs:  
            headers = {  
                "apikey": k,  
                "Authorization": f"Bearer {k}",  
                "Content-Type": "application/json"  
            }  
            try:  
                # 尝试查询 users 表  
                res = requests.get(f"{u}/users?limit=1", headers=headers, timeout=5)  
                  
                # 如果返回 200 (成功)，说明表存在！  
                if res.status_code == 200:  
                    self.url = u  
                    self.api_key = k  
                    self.is_online = True  
                    self.error_msg = ""  
                    print(f"✅ 探测成功！找到表在：{u}")  
                    return # 找到就停止  
                  
                # 如果返回 404，说明连上了但没表，继续试下一个  
                elif res.status_code == 404:  
                    print(f"⚠️ 连接 {u} 成功，但没找到表。尝试下一个...")  
                    continue  
                      
            except Exception as e:  
                print(f"❌ 连接 {u} 失败：{str(e)}")  
                  
        # 如果循环结束还没找到  
        self.error_msg = "所有项目均未找到 users 表！请在 Supabase 里确认建表是否成功。"  
        print("❌ 探测失败。")  
  
    # ... (下面的方法保持不变) ...  
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
  
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        display_name = display_name or username  
        if not self.is_online:  
            return {"success": False, "error": self.error_msg}  
              
        headers = {"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json", "Prefer": "return=representation"}  
        try:  
            check = requests.get(f"{self.url}/users?username=eq.{username}", headers=headers)  
            if check.status_code == 200 and len(check.json()) > 0:  
                return {"success": False, "error": "用户名已存在"}  
            insert = requests.post(f"{self.url}/users", headers=headers, json={"username": username, "password_hash": self.hash_password(password), "display_name": display_name})  
            if insert.status_code == 201:  
                return {"success": True, "user": insert.json()[0]}  
            return {"success": False, "error": f"注册失败：{insert.text}"}  
        except Exception as e:  
            return {"success": False, "error": str(e)}  
  
    def login_user(self, username: str, password: str) -> dict:  
        if not self.is_online: return {"success": False, "error": self.error_msg}  
        try:  
            password_hash = self.hash_password(password)  
            res = requests.get(f"{self.url}/users?username=eq.{username}&password_hash=eq.{password_hash}", headers={"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}"})  
            if len(res.json()) > 0: return {"success": True, "user": res.json()[0]}  
            return {"success": False, "error": "用户名或密码错误"}  
        except: return {"success": False, "error": "登录失败"}  
  
    def save_conversation(self, user_id, user_input, coach_reply, emotion="", topic=""):  
        if self.is_online:  
            try: requests.post(f"{self.url}/conversations", headers={"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}"}, json={"user_id": user_id, "user_input": user_input, "coach_reply": coach_reply})  
            except: pass  
  
    def get_all_users(self):  
        if self.is_online:  
            try: return requests.get(f"{self.url}/users", headers={"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}"}).json()  
            except: return []  
        return []  
