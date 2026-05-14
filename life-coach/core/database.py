"""Supabase 数据库操作 - 双重保险版"""  
import streamlit as st  
from supabase import create_client, Client  
import hashlib  
  
class Database:  
    def __init__(self):  
        # 1. 配置云端数据库（使用你确认过的 ydryp 地址）  
        self.url = "https://ydrypovzrfvmotlsaomw.supabase.co "  
        self.key = "sb_secret_xdljfyVFI8fcSFolTr3sMg_6Bc4yph3"  
        self.is_online = False  
          
        # 2. 尝试连接云端  
        try:  
            self.client: Client = create_client(self.url, self.key)  
            # 快速测试一下连通性  
            self.client.table("users").select("id").limit(1).execute()  
            self.is_online = True  
            print("✅ 数据库连接成功！数据将永久保存。")  
        except Exception as e:  
            print(f"❌ 数据库连接失败: {e}")  
            print("️ 自动降级为临时模式：刷新页面后数据会丢失。")  
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
          
        # === 云端保存 ===  
        if self.is_online:  
            try:  
                # 先检查是否存在  
                check = self.client.table("users").select("id").eq("username", username).execute()  
                if check.data:  
                    return {"success": False, "error": "用户名已存在"}  
                  
                # 插入新用户  
                data = self.client.table("users").insert({  
                    "username": username,  
                    "password_hash": self.hash_password(password),  
                    "display_name": display_name  
                }).execute()  
                return {"success": True, "user": data.data[0]}  
            except Exception as e:  
                return {"success": False, "error": f"云端保存失败: {str(e)}"}  
          
        # === 本地临时保存（备用） ===  
        else:  
            if username in st.session_state.local_users:  
                return {"success": False, "error": "用户名已存在"}  
            new_user = {  
                "username": username,  
                "password_hash": self.hash_password(password),  
                "display_name": display_name,  
                "id": username  
            }  
            st.session_state.local_users[username] = new_user  
            return {"success": True, "user": new_user}  
  
    def login_user(self, username: str, password: str) -> dict:  
        password_hash = self.hash_password(password)  
          
        # === 云端登录 ===  
        if self.is_online:  
            try:  
                data = self.client.table("users").select("*").eq("username", username).eq("password_hash", password_hash).execute()  
                if data.data:  
                    return {"success": True, "user": data.data[0]}  
                return {"success": False, "error": "用户名或密码错误"}  
            except Exception as e:  
                return {"success": False, "error": f"云端登录失败: {str(e)}"}  
          
        # === 本地临时登录（备用） ===  
        else:  
            if username not in st.session_state.local_users:  
                return {"success": False, "error": "用户名不存在"}  
            user = st.session_state.local_users[username]  
            if user["password_hash"] == password_hash:  
                return {"success": True, "user": user}  
            return {"success": False, "error": "密码错误"}  
  
    def save_conversation(self, user_id: str, user_input: str, coach_reply: str, emotion: str = "", topic: str = ""):  
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
                print(f"保存对话失败: {e}")  
        else:  
            # 本地保存  
            if user_id not in st.session_state.local_conversations:  
                st.session_state.local_conversations[user_id] = []  
            st.session_state.local_conversations[user_id].append({  
                "user_input": user_input,  
                "coach_reply": coach_reply,  
                "emotion": emotion,  
                "topic": topic  
            })  
  
    def get_user_conversations(self, user_id: str, limit: int = 50) -> list:  
        if self.is_online:  
            try:  
                data = self.client.table("conversations").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()  
                return data.data  
            except:  
                return []  
        else:  
            if user_id in st.session_state.local_conversations:  
                return st.session_state.local_conversations[user_id]  
            return []  
  
    def get_all_users(self) -> list:  
        if self.is_online:  
            try:  
                data = self.client.table("users").select("*").order("created_at", desc=True).execute()  
                return data.data  
            except:  
                return []  
        else:  
            return list(st.session_state.local_users.values())  
  
    def get_all_conversations(self, limit: int = 100) -> list:  
        if self.is_online:  
            try:  
                data = self.client.table("conversations").select("*, users(display_name, username)").order("created_at", desc=True).limit(limit).execute()  
                return data.data  
            except:  
                return []  
        else:  
            all_conv = []  
            for uid, convs in st.session_state.local_conversations.items():  
                for c in convs:  
                    c["users"] = {"display_name": st.session_state.local_users.get(uid, {}).get("display_name", uid)}  
                    all_conv.append(c)  
            return all_conv[-limit:]  
  
    def get_user_stats(self, user_id: str) -> dict:  
        convs = self.get_user_conversations(user_id)  
        emotions = {}  
        topics = {}  
        for c in convs:  
            if c.get("emotion"): emotions[c["emotion"]] = emotions.get(c["emotion"], 0) + 1  
            if c.get("topic"): topics[c["topic"]] = topics.get(c["topic"], 0) + 1  
        return {"total_conversations": len(convs), "emotions": emotions, "topics": topics}  
