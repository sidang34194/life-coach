"""  
🌱 生命动力 · AI 教练小程序  
含后台管理功能 + 本地数据库模式  
"""  
import streamlit as st  
from core.coach_engine import CoachEngine  
from core.emotion_detector import EmotionDetector  
  
st.set_page_config(  
    page_title="生命动力 · AI 教练",  
    page_icon="🌱",  
    layout="wide" # 加宽界面方便看后台  
)  
  
# 样式  
st.markdown("""  
<style>  
    .chat-message { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; line-height: 1.6; }  
    .user-message { background-color: #e8f5e9; margin-left: 20%; }  
    .coach-message { background-color: #f5f5f5; margin-right: 5%; }  
</style>  
""", unsafe_allow_html=True)  
  
# 初始化数据库（本地模式）  
if "db" not in st.session_state:  
    try:  
        from core.database import Database  
        st.session_state.db = Database()  
    except Exception as e:  
        st.error(f"数据库初始化失败: {e}")  
  
if "logged_in" not in st.session_state:  
    st.session_state.logged_in = False  
  
if "user" not in st.session_state:  
    st.session_state.user = None  
  
if "messages" not in st.session_state:  
    st.session_state.messages = []  
  
if "dialogue_count" not in st.session_state:  
    st.session_state.dialogue_count = 0  
  
# ========== 侧边栏 ==========  
with st.sidebar:  
    st.markdown("### 🌱 菜单")  
              # 显示数据库状态  
    db = st.session_state.get("db")  
    if db:  
        if db.is_online:  
            st.success("🟢 数据库：已连接 (永久保存)")  
        else:  
            st.error(f"🔴 数据库：离线！\n原因：{db.error_msg[:50]}...")  
    else:  
        st.warning("数据库未初始化")  


    # 管理员入口  
    st.markdown("---")  
    st.markdown("### 🔐 管理员入口")  
    admin_pass = st.text_input("管理员密码", type="password", key="admin_pass_input")  
      
    if admin_pass == "admin888":  
        st.success("✅ 管理员已登录")  
          
        # === 后台数据看板 ===  
        st.markdown("---")  
        st.header("📊 学员数据看板")  
          
        all_users = st.session_state.db.get_all_users()  
        st.subheader(f"已注册学员：{len(all_users)} 人")  
          
        if all_users:  
            for u in all_users:  
                with st.expander(f"👤 **{u['display_name']}** ({u['username']})"):  
                    st.write(f"注册时间：刚刚")  
                      
                    # 显示对话记录  
                    chats = st.session_state.db.get_user_conversations(u['username'])  
                    if chats:  
                        st.markdown("**最近对话：**")  
                        for i, c in enumerate(reversed(chats)):  
                            st.markdown(f"**{i+1}**. 学员：{c['user_input']}")  
                            st.markdown(f"  教练：{c['coach_reply']}")  
                            st.divider()  
                    else:  
                        st.caption("暂无对话记录")  
        else:  
            st.info("暂时还没有学员注册")  
    else:  
        # 普通学员菜单  
        if st.session_state.logged_in:  
            st.markdown(f"### 👋 {st.session_state.user['display_name']}")  
            if st.button("🚪 退出登录", use_container_width=True):  
                st.session_state.logged_in = False  
                st.session_state.user = None  
                st.session_state.messages = []  
                st.rerun()  
  
# ========== 主界面（学员端） ==========  
if not st.session_state.logged_in and admin_pass != "admin888":  
    st.markdown("<h2 style='text-align: center;'>🌱 生命动力 · AI 教练</h2>", unsafe_allow_html=True)  
    st.markdown("<p style='text-align: center;'>学员登录 / 注册</p>", unsafe_allow_html=True)  
      
    tab1, tab2 = st.tabs(["🔑 登录", "📝 注册"])  
      
    with tab1:  
        u_name = st.text_input("用户名", key="login_u")  
        u_pass = st.text_input("密码", type="password", key="login_p")  
        if st.button("登录", type="primary", use_container_width=True):  
            res = st.session_state.db.login_user(u_name, u_pass)  
            if res["success"]:  
                st.session_state.logged_in = True  
                st.session_state.user = res["user"]  
                st.rerun()  
            else:  
                st.error(res["error"])  
      
    with tab2:  
        r_name = st.text_input("用户名", key="reg_u")  
        r_disp = st.text_input("昵称", key="reg_n")  
        r_pass = st.text_input("密码", type="password", key="reg_p")  
        r_pass2 = st.text_input("确认密码", type="password", key="reg_p2")  
        if st.button("注册", use_container_width=True):  
            if r_pass != r_pass2:  
                st.error("两次密码不一致")  
            else:  
                res = st.session_state.db.register_user(r_name, r_pass, r_disp or r_name)  
                if res["success"]:  
                    st.success("注册成功！请登录")  
                else:  
                    st.error(res["error"])  
  
# ========== 聊天界面 ==========  
elif st.session_state.logged_in:  
    user = st.session_state.user  
    st.markdown(f"<h3>👋 你好，{user['display_name']}</h3>", unsafe_allow_html=True)  
      
    # 显示聊天  
    for msg in st.session_state.messages:  
        if msg["role"] == "user":  
            st.markdown(f'<div class="chat-message user-message"><strong>你：</strong>{msg["content"]}</div>', unsafe_allow_html=True)  
        else:  
            st.markdown(f'<div class="chat-message coach-message"><strong>🌱 教练：</strong>{msg["content"]}</div>', unsafe_allow_html=True)  
      
    # 输入框  
    inp_key = f"input_{st.session_state.dialogue_count}"  
    user_input = st.text_area("说说你的感受...", height=80, key=inp_key)  
      
    col1, col2 = st.columns([4, 1])  
    with col1:  
        if st.button("发送", type="primary", use_container_width=True) and user_input:  
            # 调用 AI  
            engine = CoachEngine()  
            # 这里的 get_response 需要你自己确认 coach_engine.py 是对的  
            reply = "（AI 回复功能需要 coach_engine.py 配合）"   
            try:  
                reply = engine.get_response(user_input)  
            except:  
                reply = "教练暂时无法回复"  
              
            st.session_state.messages.append({"role": "user", "content": user_input})  
            st.session_state.messages.append({"role": "assistant", "content": reply})  
            st.session_state.dialogue_count += 1  
              
            # 保存到本地数据库  
            st.session_state.db.save_conversation(  
                user_id=user['username'], # 本地模式用 username 做 ID  
                user_input=user_input,  
                coach_reply=reply,  
                emotion="未知", # 简化处理  
                topic="未知"  
            )  
            st.rerun()  
