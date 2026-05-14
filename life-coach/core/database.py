"""本地数据库模式 - 解决网络连接问题"""  
import hashlib  
import streamlit as st  
  
class Database:  
    def __init__(self):  
        # 使用内存字典模拟数据库，不再联网，避免 [Errno -2]  
        if "local_users" not in st.session_state:  
            st.session_state.local_users = {}  
        if "local_conversations" not in st.session_state:  
            st.session_state.local_conversations = {}  
              
        self.users = st.session_state.local_users  
        self.conversations = st.session_state.local_conversations  
        print("DEBUG: 使用本地内存模式，注册将瞬间完成")  
  
    def hash_password(self, password: str) -> str:  
        return hashlib.sha256(password.encode()).hexdigest()  
      
    def register_user(self, username: str, password: str, display_name: str = None) -> dict:  
        if username in self.users:  
            return {"success": False, "error": "用户名已存在"}  
          
        new_user = {  
            "username": username,  
            "password_hash": self.hash_password(password),  
            "display_name": display_name or username,  
            "id": username # 本地模式用用户名作为 ID  
        }  
        self.users[username] = new_user  
        return {"success": True, "user": new_user}  
      
    def login_user(self, username: str, password: str) -> dict:  
        if username not in self.users:  
            return {"success": False, "error": "用户名不存在"}  
              
        user = self.users[username]  
        if user["password_hash"] == self.hash_password(password):  
            return {"success": True, "user": user}  
        return {"success": False, "error": "密码错误"}  
      
    def save_conversation(self, user_id: str, user_input: str, coach_reply: str, emotion: str = "", topic: str = ""):  
        # 简单存入列表  
        if user_id not in self.conversations:  
            self.conversations[user_id] = []  
        self.conversations[user_id].append({  
            "user_input": user_input,  
            "coach_reply": coach_reply,  
            "emotion": emotion,  
            "topic": topic  
        })  
      
    def get_user_conversations(self, user_id: str, limit: int = 50) -> list:  
        if user_id in self.conversations:  
            return self.conversations[user_id]  
        return []  
      
    def get_all_users(self) -> list:  
        return list(self.users.values())  
      
    def get_all_conversations(self, limit: int = 100) -> list:  
        all_conv = []  
        for uid, convs in self.conversations.items():  
            for c in convs:  
                c["users"] = {"display_name": self.users.get(uid, {}).get("display_name", uid)}  
                all_conv.append(c)  
        return all_conv[-limit:]  
      
    def get_user_stats(self, user_id: str) -> dict:  
        convs = self.get_user_conversations(user_id)  
        emotions = {}  
        topics = {}  
        for c in convs:  
            if c.get("emotion"):  
                emotions[c["emotion"]] = emotions.get(c["emotion"], 0) + 1  
            if c.get("topic"):  
                topics[c["topic"]] = topics.get(c["topic"], 0) + 1  
        return {"total_conversations": len(convs), "emotions": emotions, "topics": topics}  
