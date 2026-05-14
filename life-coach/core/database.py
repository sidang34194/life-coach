"""Supabase 数据库操作 - 诊断模式"""  
import streamlit as st  
import requests  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 1. 强制锁定正确的网址和密钥（防止连错项目）  
        self.url = "https://ydrypovzrfvmotlsaomw.supabase.co/rest/v1 "  
        self.api_key = "sb_secret_B4kQHMkT3BHSN-K-lGIISw_7dVuYO0K"  
          
        self.is_online = False  
        self.error_msg = "正在连接..."  
          
        try:  
            headers = {  
                "apikey": self.api_key,  
                "Authorization": f"Bearer {self.api_key}",  
                "Content-Type": "application/json"  
            }  
            # 测试连接：尝试读取 users 表的前 1 行  
            res = requests.get(f"{self.url}/users?limit=1", headers=headers, timeout=5)  
              
            # 如果返回 200 (成功) 或 206 (部分内容)，说明表存在且连上了  
            if res.status_code == 200 or res.status_code == 206:  
                self.is_online = True  
                self.error_msg = ""  
                print(f"✅ 数据库连接成功！URL: {self.url}")  
            elif res.status_code == 404:  
                self.error_msg = "⚠️ 连上了，但找不到 users 表！请检查是否连错了项目（应该是 ydryp... 那个）。"  
            else:  
                self.error_msg = f"连接状态异常: {res.status_code}"  
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
                # 🔍 诊断：显示具体的报错原因（比如是哪个表不存在）  
                return {"success": False, "error": f"注册失败 (Status {insert.status_code}): {insert.text}"}  
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
