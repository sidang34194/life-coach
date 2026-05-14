"""Supabase 数据库操作 - 修复语法错误版"""  
import streamlit as st  
import requests  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 固定使用你刚才成功连通的地址和密钥  
        self.url = "https://ydrypovzrfvmotlsaomw.supabase.co/rest/v1 "  
        self.api_key = "sb_secret_B4kQHMkT3BHSN-K-lGIISw_7dVuYO0K"  
          
        self.is_online = False  
        self.error_msg = "正在连接..."  
          
        try:  
            # 简单测试连接  
            headers = {  
                "apikey": self.api_key,  
                "Authorization": f"Bearer {self.api_key}",  
                "Content-Type": "application/json"  
            }  
            # 尝试获取 users 表（即使表不存在，只要连接通了就算成功）  
            res = requests.get(f"{self.url}/users?limit=1", headers=headers, timeout=5)  
              
            # 只要不是 500/503 服务器错误，就算连上了  
            if res.status_code < 500:  
                self.is_online = True  
                self.error_msg = ""  
                print(f"✅ 数据库连接成功！URL: {self.url}")  
            else:  
                self.error_msg = f"服务器错误：{res.status_code}"  
        except Exception as e:  
            self.error_msg = str(e)  
            print(f"❌ 数据库连接失败：{self.error_msg}")  
  
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
  
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        display_name = display_name or username  
        if not self.is_online:  
            return {"success": False, "error": self.error_msg}  
              
        headers = {  
            "apikey": self.api_key,   
            "Authorization": f"Bearer {self.api_key}",   
            "Content-Type": "application/json",   
            "Prefer": "return=representation"  
        }  
          
        try:  
            # 1. 检查用户是否存在  
            check = requests.get(  
                f"{self.url}/users?username=eq.{username}",   
                headers=headers  
            )  
            if check.status_code == 200 and len(check.json()) > 0:  
                return {"success": False, "error": "用户名已存在"}  
              
            # 2. 注册新用户  
            insert = requests.post(  
                f"{self.url}/users",  
                headers=headers,  
                json={  
                    "username": username,   
                    "password_hash": self.hash_password(password),   
                    "display_name": display_name  
                }  
            )  
              
            if insert.status_code == 201:  
                return {"success": True, "user": insert.json()[0]}  
            else:  
                return {"success": False, "error": f"注册失败 (Status {insert.status_code})"}  
        except Exception as e:  
            return {"success": False, "error": str(e)}  
  
    def login_user(self, username: str, password: str) -> dict:  
        if not self.is_online:  
            return {"success": False, "error": self.error_msg}  
              
        headers = {  
            "apikey": self.api_key,   
            "Authorization": f"Bearer {self.api_key}",   
            "Content-Type": "application/json"  
        }  
        try:  
            password_hash = self.hash_password(password)  
            res = requests.get(  
                f"{self.url}/users?username=eq.{username}&password_hash=eq.{password_hash}",  
                headers=headers  
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
                    headers={  
                        "apikey": self.api_key,   
                        "Authorization": f"Bearer {self.api_key}",   
                        "Content-Type": "application/json"  
                    },  
                    json={  
                        "user_id": user_id,   
                        "user_input": user_input,   
                        "coach_reply": coach_reply,   
                        "emotion": emotion,   
                        "topic": topic  
                    }  
                )  
            except Exception:  
                pass  
  
    def get_all_users(self):  
        if self.is_online:  
            try:  
                res = requests.get(  
                    f"{self.url}/users?order=created_at.desc",   
                    headers={  
                        "apikey": self.api_key,   
                        "Authorization": f"Bearer {self.api_key}"  
                    }  
                )  
                return res.json()  
            except Exception:  
                return []  
        return []  
