"""Supabase 数据库操作 - 强制连接版"""  
import streamlit as st  
from supabase import create_client, Client  
import hashlib  
  
class Database:  
    def __init__(self):  
        self.url = "https://ydrypovzrfvmotlsaomw.supabase.co "  
        self.key = "sb_secret_xdljfyVFI8fcSFolTr3sMg_6Bc4yph3"  
        self.is_online = False  
        self.error_msg = ""  
          
        try:  
            print("DEBUG: 正在连接 Supabase...")  
            self.client: Client = create_client(self.url, self.key)  
            # 强制测试连接  
            res = self.client.table("users").select("id").limit(1).execute()  
            self.is_online = True  
            print("✅ Supabase 连接成功！")  
        except Exception as e:  
            self.is_online = False  
            self.error_msg = str(e)  
            print(f"❌ Supabase 连接失败: {self.error_msg}")  
  
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
  
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        display_name = display_name or username  
        if self.is_online:  
            try:  
                # 检查是否存在  
                check = self.client.table("users").select("id").eq("username", username).execute()  
                if check.data: return {"success": False, "error": "用户名已存在"}  
                  
                # 插入  
                data = self.client.table("users").insert({  
                    "username": username,  
                    "password_hash": self.hash_password(password),  
                    "display_name": display_name  
                }).execute()  
                return {"success": True, "user": data.data[0]}  
            except Exception as e:  
                return {"success": False, "error": f"注册失败：{str(e)}"}  
        else:  
            return {"success": False, "error": "数据库离线，无法注册"}  
  
    def login_user(self, username: str, password: str) -> dict:  
        password_hash = self.hash_password(password)  
        if self.is_online:  
            try:  
                data = self.client.table("users").select("*").eq("username", username).eq("password_hash", password_hash).execute()  
                if data.data: return {"success": True, "user": data.data[0]}  
                return {"success": False, "error": "用户名或密码错误"}  
            except Exception as e:  
                return {"success": False, "error": "登录失败：数据库离线或 Key 无效"}  
        return {"success": False, "error": "数据库离线，无法登录"}  
  
    def save_conversation(self, user_id, user_input, coach_reply, emotion="", topic=""):  
        if self.is_online:  
            try:  
                self.client.table("conversations").insert({  
                    "user_id": user_id,  
                    "user_input": user_input,  
                    "coach_reply": coach_reply,  
                    "emotion": emotion,  
                    "topic": topic  
                }).execute()  
            except Exception as e:  
                print(f"保存失败：{e}")  
  
    def get_all_users(self):  
        if self.is_online:  
            try: return self.client.table("users").select("*").execute().data  
            except: return []  
        return []  
