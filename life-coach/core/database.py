"""Supabase 数据库操作 - HTTP 直连版 (解决网络报错)"""  
import streamlit as st  
import requests  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 正确的地址和密钥  
        self.url = "https://ydrypovzrfvmotlsaomw.supabase.co/rest/v1 "  
        self.api_key = "sb_secret_xdljfyVFI8fcSFolTr3sMg_6Bc4yph3"  
        self.headers = {  
            "apikey": self.api_key,  
            "Authorization": f"Bearer {self.api_key}",  
            "Content-Type": "application/json",  
            "Prefer": "return=representation"  
        }  
          
        self.is_online = False  
        self.error_msg = ""  
          
        # 尝试直连测试  
        try:  
            # 测试连接 users 表  
            response = requests.get(f"{self.url}/users?limit=1", headers=self.headers, timeout=5)  
            if response.status_code == 200:  
                self.is_online = True  
                print("✅ 数据库直连成功！数据将永久保存。")  
            else:  
                self.error_msg = f"连接被拒绝：{response.text}"  
        except Exception as e:  
            self.error_msg = str(e)  
            print(f"❌ 数据库连接失败：{self.error_msg}")  
  
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
  
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        display_name = display_name or username  
        if not self.is_online:  
            return {"success": False, "error": "数据库离线"}  
              
        try:  
            # 1. 检查用户是否存在  
            check_res = requests.get(  
                f"{self.url}/users?username=eq.{username}",  
                headers=self.headers  
            )  
            if len(check_res.json()) > 0:  
                return {"success": False, "error": "用户名已存在"}  
              
            # 2. 注册用户  
            insert_res = requests.post(  
                f"{self.url}/users",  
                headers=self.headers,  
                json={  
                    "username": username,  
                    "password_hash": self.hash_password(password),  
                    "display_name": display_name  
                }  
            )  
              
            if insert_res.status_code == 201:  
                return {"success": True, "user": insert_res.json()[0]}  
            else:  
                return {"success": False, "error": f"注册失败：{insert_res.text}"}  
        except Exception as e:  
            return {"success": False, "error": str(e)}  
  
    def login_user(self, username: str, password: str) -> dict:  
        if not self.is_online:  
            return {"success": False, "error": "数据库离线"}  
              
        try:  
            password_hash = self.hash_password(password)  
            res = requests.get(  
                f"{self.url}/users?username=eq.{username}&password_hash=eq.{password_hash}",  
                headers=self.headers  
            )  
            data = res.json()  
            if len(data) > 0:  
                return {"success": True, "user": data[0]}  
            return {"success": False, "error": "用户名或密码错误"}  
        except Exception as e:  
            return {"success": False, "error": "登录失败"}  
  
    def save_conversation(self, user_id, user_input, coach_reply, emotion="", topic=""):  
        if self.is_online:  
            try:  
                requests.post(  
                    f"{self.url}/conversations",  
                    headers=self.headers,  
                    json={  
                        "user_id": user_id,  
                        "user_input": user_input,  
                        "coach_reply": coach_reply,  
                        "emotion": emotion,  
                        "topic": topic  
                    }  
                )  
            except: pass  
  
    def get_all_users(self):  
        if self.is_online:  
            try:  
                res = requests.get(f"{self.url}/users?order=created_at.desc", headers=self.headers)  
                return res.json()  
            except: return []  
        return []  
