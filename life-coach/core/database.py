"""Supabase 数据库操作 - 智能双模版（自动切换在线/离线）"""  
import streamlit as st  
from supabase import create_client, Client  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 配置云端数据库  
        self.url = "https://ydrypovzrfvmotlsaomw.supabase.co "  
        self.key = "sb_secret_xdljfyVFI8fcSFolTr3sMg_6Bc4yph3"  
        self.is_online = False  
          
        # 1. 尝试连接云端  
        try:  
            self.client: Client = create_client(self.url, self.key)  
            # 简单测试连通性  
            self.client.table("users").select("id").limit(1).execute()  
            self.is_online = True  
            print("✅ 数据库连接成功！数据将永久保存。")  
        except Exception as e:  
            print(f"❌ 数据库连接失败: {e}")  
            print("⚠️ 降级为临时模式：刷新页面后数据会丢失。")  
            self.is_online = False  
            # 初始化本地临时存储  
            if "local_users" not in st.session_state:  
                st.session_state.local_users = {}  
            if "local_conversations" not in st.session_state:  
                st.session_state.local_conversations = {}  
  
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
  
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        display_name = display_name or username  
          
        # === 云端注册 ===  
        if self.is_online:  
            try:  
                check = self.client.table("users").select("id").eq("username", username).execute()  
                if check.data: return {"success": False, "error": "用户名已存在"}  
                  
                data = self.client.table("users").insert({  
                    "username": username,  
                    "password_hash": self.hash_password(password),  
                    "display_name": display_name  
                }).execute()  
                return {"success": True, "user": data.data[0]}  
            except Exception as e:  
                return {"success": False, "error": f"云端保存失败: {str(e)}"}  
          
        # === 本地临时注册（备用） ===  
        else:  
            if username in st.session_state.local_users:  
                return {"success": False, "error": "用户名已存在"}  
            new_user = {"username": username, "password_hash": self.hash_password(password), "display_name": display_name, "id": username}  
            st.session_state.local_users[username] = new_user  
            return {"success": True, "user": new_user}  
  
    def login_user(self, username: str, password: str) -> dict:  
        password_hash = self.hash_password(password)  
        if self.is_online:  
            try:  
                data = self.client.table("users").select("*").eq("username", username).eq("password_hash", password_hash).execute()  
                if data.data: return {"success": True, "user": data.data[0]}  
                return {"success": False, "error": "用户名或密码错误"}  
            except Exception as e:  
                return {"success": False, "error": "云端登录失败"}  
        else:  
            if username not in st.session_state.local_users: return {"success": False, "error": "用户名不存在"}  
            if st.session_state.local_users[username]["password_hash"] == password_hash:  
                return {"success": True, "user": st.session_state.local_users[username]}  
            return {"success": False, "error": "密码错误"}  
  
    def save_conversation(self, user_id, user_input, coach_reply, emotion="", topic=""):  
        if self.is_online:  
            try:  
                self.client.table("conversations").insert({"user_id": user_id, "user_input": user_input, "coach_reply": coach_reply, "emotion": emotion, "topic": topic}).execute()  
            except: pass  
        else:  
            st.session_state.local_conversations.setdefault(user_id, []).append({"user_input": user_input, "coach_reply": coach_reply})  
  
    def get_all_users(self):  
        if self.is_online:  
            try: return self.client.table("users").select("*").execute().data  
            except: return []  
        return list(st.session_state.local_users.values())  
      
    def get_user_conversations(self, user_id, limit=50):  
        if self.is_online:  
            try: return self.client.table("conversations").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute().data  
            except: return []  
        return st.session_state.local_conversations.get(user_id, [])  
