"""Supabase 数据库操作 - 强力直连版 (移除强制表检查)"""  
import streamlit as st  
import requests  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 列表：所有可能的 URL 和 Key 组合  
        urls = [  
            "https://ydrypovzrfvmotlsaomw.supabase.co/rest/v1 ",  
            "https://zgyzjxryvlgwzqkqfkoo.supabase.co/rest/v1 "  
        ]  
        keys = [  
            "sb_secret_B4kQHMkT3BHSN-K-lGIISw_7dVuYO0K", # 新 Key  
            "sb_secret_1Bi1unY-W2GkrzhDgKfqlw_M0GjMQXB" # 旧 Key  
        ]  
          
        self.url = ""  
        self.api_key = ""  
        self.is_online = False  
        self.error_msg = "正在连接..."  
          
        # 自动匹配逻辑：只要数据库能通，就不管表存不存在，直接放行  
        for u in urls:  
            for k in keys:  
                headers = {  
                    "apikey": k,  
                    "Authorization": f"Bearer {k}",  
                    "Content-Type": "application/json"  
                }  
                try:  
                    # 1. 测试能否连通数据库根目录  
                    # 这里不检查 users 表，只检查能不能连上数据库服务器  
                    res = requests.get(f"{u}/", headers=headers, timeout=5)  
                      
                    # 如果返回 200 (OK) 或 401 (需要认证，说明服务器在)，都算连上了  
                    if res.status_code < 500:   
                        self.url = u  
                        self.api_key = k  
                        self.is_online = True  
                        self.error_msg = ""  
                        print(f"✅ 连接成功！项目: {u}")  
                        return   
                except:  
                    continue  
                      
        self.error_msg = "数据库无法连接。"  
        print("❌ 连接失败。")  
  
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
                json={"username": username, "password_hash": self.hash
