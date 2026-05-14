"""  
🌱 生命动力 · AI 教练小程序  
简化版 - 自动教练模式  
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
  
if "engine" not in st.session_state:  
    try:  
        st.session_state.engine = CoachEngine()  
        st.session_state.initialized = True  
    except ValueError as e:  
        st.session_state.initialized = False  
        st.session_state.error_msg = str(e)  
  
if "messages" not in st.session_state:  
    st.session_state.messages = []  
  
if "dialogue_count" not in st.session_state:  
    st.session_state.dialogue_count = 0  
  
if "user_input" not in st.session_state:  
    st.session_state.user_input = ""  
  
with st.sidebar:  
    st.markdown("### 🌱 关于")  
    st.markdown("**生命动力 · AI 教练**\n\n不用选模式，直接说。AI 教练会自动用聆听、发问、区分、回应的方式帮助你。")  
    st.markdown("---")  
    st.markdown(f"### 📊 对话统计")  
    st.markdown(f"已进行 **{st.session_state.dialogue_count}** 轮对话")  
    if st.button("🗑️ 清空对话", use_container_width=True):  
        st.session_state.engine.reset_conversation()  
        st.session_state.messages = []  
        st.session_state.dialogue_count = 0  
        st.session_state.user_input = ""  
        st.rerun()  
  
st.markdown('<p class="main-header">🌱 生命动力 · AI 教练</p>', unsafe_allow_html=True)  
st.markdown('<p class="sub-header">直接说出你的感受，教练会自动回应</p>', unsafe_allow_html=True)  
  
if not st.session_state.initialized:  
    st.error(f"⚠️ {st.session_state.error_msg}")  
    st.stop()  
  
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
  
user_input = st.text_area(  
    "说说你现在的情况或感受...",  
    value=st.session_state.user_input,  
    height=100,  
    placeholder="例如：我今天感到很迷茫，不知道自己在追求什么...",  
    key="input_area"  
)  
  
col1, col2 = st.columns([3, 1])  
with col1:  
    send_clicked = st.button("✉️ 发送", type="primary", use_container_width=True)  
with col2:  
    reset_clicked = st.button("🔄 重置", use_container_width=True)  
  
if send_clicked and user_input.strip():  
    with st.spinner("教练正在思考..."):  
        reply = st.session_state.engine.get_response(user_input)  
        st.session_state.messages.append({"role": "user", "content": user_input})  
        st.session_state.messages.append({"role": "assistant", "content": reply})  
        st.session_state.dialogue_count += 1  
        st.session_state.user_input = ""  
    st.rerun()  
  
if reset_clicked:  
    st.session_state.engine.reset_conversation()  
    st.session_state.messages = []  
    st.session_state.dialogue_count = 0  
    st.session_state.user_input = ""  
    st.rerun()  
  
st.markdown("---")  
st.markdown("""  
<div style="text-align: center; color: #999; font-size: 0.8rem;">  
💡 教练不会给你答案，而是帮你发现自己的答案。<br/>  
如果你遇到严重心理困扰，建议寻求专业心理咨询师的帮助。  
</div>  
""", unsafe_allow_html=True)  
