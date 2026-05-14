"""  
🌱 生命动力 · AI 教练小程序  
完整版 - 含用户注册/登录 + 数据库  
"""  
import streamlit as st  
from core.coach_engine import CoachEngine  
from core.emotion_detector import EmotionDetector  
  
st.set_page_config(  
    page_title="生命动力 · AI 教练",  
    page_icon="🌱",  
    layout="centered"  
)  
  
st.markdown("""  
<style>  
    .main-header { text-align: center; font-size: 2rem; color: #2d6a4f; margin-bottom: 0.5rem; }  
    .sub-header { text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 1.5rem; }  
    .chat-message { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; line-height: 1.6; }  
    .user-message { background-color: #e8f5e9; margin-left: 20%; }  
    .coach-message { background-color: #f5f5f5; margin-right: 5%; }  
    .emotion-tag { display: inline-block; background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-right: 4px; }  
</style>  
""", unsafe_allow_html=True)  
  
# 初始化数据库（带错误处理）  
if "db" not in st.session_state:  
    try:  
        from core.database import Database  
        st.session_state.db = Database()  
        st.session_state.db_ready = True  
    except Exception as e:  
        st.session_state.db_ready = False  
        st.session_state.db_error = str(e)  
  
if "logged_in" not in st.session_state:  
    st.session_state.logged_in = False  
  
if "user" not in st.session_state:  
    st.session_state.user = None  
  
if "messages" not in st.session_state:  
    st.session_state.messages = []  
  
if "dialogue_count" not in st.session_state:  
    st.session_state.dialogue_count = 0  
  
# ========== 登录/注册页面 ==========  
if not st.session_state.logged_in:  
    st.markdown('<p class="main-header">🌱 生命动力 · AI 教练</p>', unsafe_allow_html=True)  
    st.markdown('<p class="sub-header">聆听 · 发问 · 区分 · 回应</p>', unsafe_allow_html=True)  
      
    if not st.session_state.db_ready:  
        st.error("数据库连接失败：" + st.session_state.get("db_error", "未知错误"))  
        st.info("请检查 Supabase 配置是否正确")  
        st.stop()  
      
    tab1, tab2 = st.tabs(["🔑 登录", "📝 注册"])  
      
    with tab1:  
        st.markdown("### 欢迎回来")  
        login_user = st.text_input("用户名", key="login_user")  
        login_pass = st.text_input("密码", type="password", key="login_pass")  
        if st.button("登录", type="primary", use_container_width=True):  
            if login_user and login_pass:  
                result = st.session_state.db.login_user(login_user, login_pass)  
                if result["success"]:  
                    st.session_state.logged_in = True  
                    st.session_state.user = result["user"]  
                    st.session_state.messages = []  
                    st.session_state.dialogue_count = 0  
                    st.rerun()  
                else:  
                    st.error(result["error"])  
            else:  
                st.warning("请填写用户名和密码")  
      
    with tab2:  
        st.markdown("### 创建账号")  
        reg_user = st.text_input("用户名", key="reg_user")  
        reg_name = st.text_input("显示名称（选填）", key="reg_name")  
        reg_pass = st.text_input("密码", type="password", key="reg_pass")  
        reg_pass2 = st.text_input("确认密码", type="password", key="reg_pass2")  
        if st.button("注册", use_container_width=True):  
            if reg_user and reg_pass:  
                if reg_pass != reg_pass2:  
                    st.error("两次密码不一致")  
                elif len(reg_pass) < 4:  
                    st.error("密码至少 4 位")  
                else:  
                    result = st.session_state.db.register_user(reg_user, reg_pass, reg_name or reg_user)  
                    if result["success"]:  
                        st.success("注册成功！请切换到登录页登录")  
                    else:  
                        st.error(result["error"])  
            else:  
                st.warning("请填写用户名和密码")  
    st.stop()  
  
# ========== 主聊天页面 ==========  
user = st.session_state.user  
display_name = user.get("display_name", user.get("username", "学员"))  
  
with st.sidebar:  
    st.markdown(f"### 👋 你好，{display_name}")  
    st.markdown("---")  
    st.markdown("### 📖 使用说明")  
    st.markdown("- 直接说出你的感受或困惑")  
    st.markdown("- AI 教练会自动用合适的方式回应")  
    st.markdown("- 对话会保存，随时可查看")  
    st.markdown("---")  
      
    if st.button(" 查看历史对话", use_container_width=True):  
        st.session_state.show_history = not st.session_state.get("show_history", False)  
      
    if st.session_state.get("show_history"):  
        convs = st.session_state.db.get_user_conversations(user["id"], limit=20)  
        if convs:  
            for i, c in enumerate(convs):  
                st.markdown(f"**{i+1}**. {c['user_input'][:30]}...")  
        else:  
            st.caption("暂无历史记录")  
      
    st.markdown("---")  
    if st.button("🚪 退出登录", use_container_width=True):  
        st.session_state.logged_in = False  
        st.session_state.user = None  
        st.session_state.messages = []  
        st.session_state.dialogue_count = 0  
        st.rerun()  
  
st.markdown('<p class="main-header">🌱 生命动力 · AI 教练</p>', unsafe_allow_html=True)  
st.markdown('<p class="sub-header">直接说出你的感受，教练会自动回应</p>', unsafe_allow_html=True)  
  
st.markdown("### 对话")  
chat_container = st.container()  
with chat_container:  
    for msg in st.session_state.messages:  
        if msg["role"] == "user":  
            st.markdown(f'<div class="chat-message user-message"><strong>你：</strong>{msg["content"]}</div>', unsafe_allow_html=True)  
        else:  
            st.markdown(f'<div class="chat-message coach-message"><strong>🌱 教练：</strong>{msg["content"]}</div>', unsafe_allow_html=True)  
  
if st.session_state.messages:  
    last_user_msg = None  
    for msg in reversed(st.session_state.messages):  
        if msg["role"] == "user":  
            last_user_msg = msg["content"]  
            break  
    if last_user_msg:  
        analysis = EmotionDetector.analyze(last_user_msg)  
        if analysis["emotion"]["primary"] != "平静" or analysis["topic"]["primary"] != "综合":  
            tags = []  
            if analysis["emotion"]["primary"] != "平静":  
                tags.append(f'<span class="emotion-tag">💭 {analysis["emotion"]["primary"]}</span>')  
            if analysis["topic"]["primary"] != "综合":  
                tags.append(f'<span class="emotion-tag">📂 {analysis["topic"]["primary"]}</span>')  
            if tags:  
                st.markdown("".join(tags), unsafe_allow_html=True)  
  
input_key = f"input_{st.session_state.dialogue_count}"  
user_input = st.text_area(  
    "说说你现在的情况或感受...",  
    height=100,  
    placeholder="例如：我今天感到很迷茫，不知道自己在追求什么...",  
    key=input_key  
)  
  
col1, col2 = st.columns([3, 1])  
with col1:  
    send_clicked = st.button("✉️ 发送", type="primary", use_container_width=True)  
with col2:  
    reset_clicked = st.button(" 重置", use_container_width=True)  
  
if send_clicked and user_input.strip():  
    with st.spinner("教练正在思考..."):  
        analysis = EmotionDetector.analyze(user_input)  
        emotion = analysis["emotion"]["primary"]  
        topic = analysis["topic"]["primary"]  
          
        engine = CoachEngine()  
        reply = engine.get_response(user_input)  
          
        st.session_state.messages.append({"role": "user", "content": user_input})  
        st.session_state.messages.append({"role": "assistant", "content": reply})  
        st.session_state.dialogue_count += 1  
          
        if st.session_state.db_ready:  
            st.session_state.db.save_conversation(  
                user_id=user["id"],  
                user_input=user_input,  
                coach_reply=reply,  
                emotion=emotion,  
                topic=topic  
            )  
    st.rerun()  
  
if reset_clicked:  
    st.session_state.messages = []  
    st.session_state.dialogue_count = 0  
    st.rerun()  
  
st.markdown("---")  
st.markdown("""  
<div style="text-align: center; color: #999; font-size: 0.8rem;">  
💡 教练不会给你答案，而是帮你发现自己的答案。<br/>  
如果你遇到严重心理困扰，建议寻求专业心理咨询师的帮助。  
</div>  
""", unsafe_allow_html=True)  
