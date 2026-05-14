"""Supabase 数据库操作 - 最终确认版"""  
from supabase import create_client, Client  
import streamlit as st  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 使用你刚才浏览器验证过的正确地址  
        self.url = "https://ydrypovzrfvmotlsaomw.supabase.co "  
        # 使用对应的密钥  
        self.key = "sb_secret_xdljfyVFI8fcSFolTr3sMg_6Bc4yph3"  
          
        if not self.url or not self.key:  
            raise ValueError("Supabase 配置未设置")  
          
        print(f"DEBUG: 正在连接 -> {self.url}")  
        self.client: Client = create_client(self.url, self.key)  
      
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
      
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        password_hash = self.hash_password(password)  
        try:  
            data = self.client.table("users").insert({  
                "username": username,  
                "password_hash": password_hash,  
                "display_name": display_name or username  
            }).execute()  
            return {"success": True, "user": data.data[0]}  
        except Exception as e:  
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():  
                return {"success": False, "error": "用户名已存在"}  
            return {"success": False, "error": str(e)}  
      
    def login_user(self, username: str, password: str) -> dict:  
        password_hash = self.hash_password(password)  
        try:  
            data = self.client.table("users").select("*").eq("username", username).eq("password_hash", password_hash).execute()  
            if data.data:  
                return {"success": True, "user": data.data[0]}  
            return {"success": False, "error": "用户名或密码错误"}  
        except Exception as e:  
            return {"success": False, "error": str(e)}  
      
    def save_conversation(self, user_id: str, user_input: str, coach_reply: str, emotion: str = "", topic: str = ""):  
        try:  
            self.client.table("conversations").insert({  
                "user_id": user_id,  
                "user_input": user_input,  
                "coach_reply": coach_reply,  
                "emotion": emotion,  
                "topic": topic  
            }).execute()  
        except Exception as e:  
            print(f"保存对话失败: {e}")  
      
    def get_user_conversations(self, user_id: str, limit: int = 50) -> list:  
        try:  
            data = self.client.table("conversations").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()  
            return data.data  
        except Exception as e:  
            return []  
      
    def get_all_users(self) -> list:  
        try:  
            data = self.client.table("users").select("*").order("created_at", desc=True).execute()  
            return data.data  
        except Exception as e:  
            return []  
      
    def get_all_conversations(self, limit: int = 100) -> list:  
        try:  
            data = self.client.table("conversations").select("*, users(display_name, username)").order("created_at", desc=True).limit(limit).execute()  
            return data.data  
        except Exception as e:  
            return []  
      
    def get_user_stats(self, user_id: str) -> dict:  
        try:  
            convs = self.client.table("conversations").select("id, emotion, topic").eq("user_id", user_id).execute()  
            data = convs.data  
            emotions = {}  
            topics = {}  
            for c in data:  
                if c.get("emotion"):  
                    emotions[c["emotion"]] = emotions.get(c["emotion"], 0) + 1  
                if c.get("topic"):  
                    topics[c["topic"]] = topics.get(c["topic"], 0) + 1  
            return {"total_conversations": len(data), "emotions": emotions, "topics": topics}  
        except Exception as e:  
            return {"total_conversations": 0, "emotions": {}, "topics": {}}  
