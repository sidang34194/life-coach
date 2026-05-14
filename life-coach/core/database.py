"""Supabase 数据库操作 - 智能自动匹配版 (自动寻找能通的连接)"""  
import streamlit as st  
import requests  
import hashlib  
import time  
  
class Database:  
    def __init__(self):  
        # 尝试列表：所有可能的 URL 和 Key 组合  
        urls = [  
            "https://ydrypovzrfvmotlsaomw.supabase.co/rest/v1 ",  
            "https://zgyzjxryvlgwzqkqfkoo.supabase.co/rest/v1 " # 尝试第二个网址  
        ]  
        keys = [  
            "sb_secret_B4kQHMkT3BHSN-K-lGIISw_7dVuYO0K",  
            "sb_secret_1Bi1unY-W2GkrzhDgKfqlw_M0GjMQXB" # 尝试第二个密钥  
        ]  
          
        self.url = ""  
        self.api_key = ""  
        self.is_online = False  
        self.error_msg = "正在尝试连接..."  
          
        # 自动遍历寻找能通的连接  
        print("DEBUG: 开始自动匹配数据库连接...")  
        for u in urls:  
            for k in keys:  
                headers = {  
                    "apikey": k,  
                    "Authorization": f"Bearer {k}",  
                    "Content-Type": "application/json"  
                }  
                try:  
                    # 尝试查询 users 表  
                    res = requests.get(f"{u}/users?limit=1", headers=headers, timeout=5)  
                    # 如果返回 200 OK，或者 404 (表不存在但连上了)，都算成功  
                    if res.status_code == 200 or res.status_code == 404:  
                        self.url = u  
                        self.api_key = k  
                        self.is_online = True  
                        self.error_msg = ""  
                        print(f"✅ 匹配成功！使用 URL: {u}")  
                        return # 找到就停止  
                except:  
                    continue  
                      
        self.error_msg = "所有组合均失败。请检查 Supabase 项目是否 Active。"  
        print("❌ 匹配失败。")  
  
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
  
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        display_name = display_name or username  
        if not self.is_online:  
            return {"success": False, "error": self.error_msg}  
              
        headers = {"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json", "Prefer": "return=representation"}  
          
        try:  
            # 检查用户  
            check = requests.get(f"{self.url}/users?username=eq.{username}", headers=headers)  
            if check.status_code == 200 and len(check.json()) > 0:  
                return {"success": False, "error": "用户名已存在"}  
              
            # 注册  
            insert = requests.post(  
                f"{self.url}/users",  
                headers=headers,  
                json={"username": username, "password_hash": self.hash_password(password), "display_name": display_name}  
            )  
              
            if insert.status_code == 201:  
                return {"success": True, "user": insert.json()[0]}  
            else:  
                return {"success": False, "error": f"注册失败 (Status {insert.status_code}): {insert.text}"}  
        except Exception as e:  
            return {"success": False, "error": str(e)}  
  
    def login_user(self, username: str, password: str) -> dict:  
        if not self.is_online:  
            return {"success": False, "error": self.error_msg}  
              
        headers = {"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}  
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
        except:  
            return {"success": False, "error": "登录失败"}  
  
    def save_conversation(self, user_id, user_input, coach_reply, emotion="", topic=""):  
        if self.is_online:  
            try:  
                requests.post(  
                    f"{self.url}/conversations",  
                    headers={"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},  
                    json={"user_id": user_id, "user_input": user_input, "coach_reply": coach_reply, "emotion": emotion, "topic": topic}  
                )  
            except: pass  
  
    def get_all_users(self):  
        if self.is_online:  
            try:  
                res = requests.get(f"{self.url}/users?order=created_at.desc", headers={"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}"})  
                return res.json()  
            except: return []  
        return []  
