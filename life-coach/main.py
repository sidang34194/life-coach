"""
🌱 生命动力 · AI 教练小程序
主界面 - 完整版
"""
import streamlit as st
from core.coach_engine import CoachEngine
from core.emotion_detector import EmotionDetector

# 页面配置
st.set_page_config(
    page_title="生命动力 · AI 教练",
    page_icon="🌱",
    layout="centered"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 2rem;
        color: #2d6a4f;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    .user-message {
        background-color: #e8f5e9;
        margin-left: 20%;
    }
    .coach-message {
        background-color: #f5f5f5;
        margin-right: 5%;
    }
    .emotion-tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin-right: 4px;
    }
    .mode-indicator {
        text-align: center;
        padding: 8px;
        background: #f0f4c3;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .sidebar-info {
        font-size: 0.85rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 Session State
if "engine" not in st.session_state:
    try:
        st.session_state.engine = CoachEngine()
        st.session_state.initialized = True
    except ValueError as e:
        st.session_state.initialized = False
        st.session_state.error_msg = str(e)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "聆听"

if "dialogue_count" not in st.session_state:
    st.session_state.dialogue_count = 0

# 侧边栏
with st.sidebar:
    st.markdown("### 🌱 关于")
    st.markdown("""
    **生命动力 · AI 教练**
    
    基于「聆听、发问、区分、回应」的教练技术，帮你自我觉察、找到答案。
    """)
    
    st.markdown("---")
    st.markdown("### 📖 教练模式")
    st.markdown("""
    - **🎧 聆听** — 接纳情绪，不评判
    - **❓ 发问** — 提出有力问题
    - **🔍 区分** — 看到盲点
    - **💬 回应** — 赋能+推动行动
    """)
    
    st.markdown("---")
    st.markdown(f"### 📊 对话统计")
    st.markdown(f"已进行 **{st.session_state.dialogue_count}** 轮对话")
    
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.engine.reset_conversation()
        st.session_state.messages = []
        st.session_state.dialogue_count = 0
        st.rerun()

# 主界面
st.markdown('<p class="main-header">🌱 生命动力 · AI 教练</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">聆听 · 发问 · 区分 · 回应</p>', unsafe_allow_html=True)

# 检查初始化
if not st.session_state.initialized:
    st.error(f"⚠️ {st.session_state.error_msg}")
    st.info("请在 `.env` 文件中配置你的智谱 AI API Key。获取地址：https://open.bigmodel.cn/")
    st.stop()

# 教练模式选择
st.markdown("### 选择教练模式")
modes = ["🎧 聆听", "❓ 发问", "🔍 区分", "💬 回应"]
mode_mapping = {"🎧 聆听": "聆听", "❓ 发问": "发问", "🔍 区分": "区分", "💬 回应": "回应"}

cols = st.columns(4)
for i, mode in enumerate(modes):
    if cols[i].button(mode, use_container_width=True, type="primary" if mode_mapping[mode] == st.session_state.current_mode else "secondary"):
        st.session_state.current_mode = mode_mapping[mode]

st.markdown(f'<div class="mode-indicator">当前模式：**{st.session_state.current_mode}**</div>', unsafe_allow_html=True)

# 对话历史展示
st.markdown("### 对话")

chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>你：</strong>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message coach-message"><strong>🌱 教练：</strong>{msg["content"]}</div>', unsafe_allow_html=True)

# 情绪/话题分析展示（如果有）
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

# 用户输入
user_input = st.text_area(
    "说说你现在的情况或感受...",
    height=100,
    placeholder="例如：我今天感到很迷茫，不知道自己在追求什么..."
)

# 按钮
col1, col2 = st.columns([3, 1])
with col1:
    send_clicked = st.button("✉️ 发送", type="primary", use_container_width=True)
with col2:
    reset_clicked = st.button("🔄 重置", use_container_width=True)

# 处理发送
if send_clicked and user_input.strip():
    with st.spinner("教练正在思考..."):
        reply = st.session_state.engine.get_response(user_input, st.session_state.current_mode)
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.dialogue_count += 1
    st.rerun()

# 处理重置
if reset_clicked:
    st.session_state.engine.reset_conversation()
    st.session_state.messages = []
    st.session_state.dialogue_count = 0
    st.rerun()

# 底部说明
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8rem;">
💡 教练不会给你答案，而是帮你发现自己的答案。<br/>
如果你遇到严重心理困扰，建议寻求专业心理咨询师的帮助。
</div>
""", unsafe_allow_html=True)
