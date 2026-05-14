"""大师级 AI 教练引擎 - 通义千问 Qwen 版"""  
import streamlit as st  
from openai import OpenAI  
  
class CoachEngine:  
    def __init__(self):  
        # 读取千问 API Key  
        api_key = st.secrets.get("DASHSCOPE_API_KEY", "")  
        if not api_key:  
            raise ValueError("通义千问 API Key 未配置")  
          
        # 初始化 OpenAI 客户端，指向阿里 DashScope  
        self.client = OpenAI(  
            api_key=api_key,  
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1 ",  
        )  
          
        # 初始化"教练状态"  
        if "coach_state" not in st.session_state:  
            st.session_state.coach_state = {  
                "trust_level": 0,           
                "user_emotion": "未知",      
                "coaching_phase": "建立连接",   
                "insights": []               
            }  
  
    def get_response(self, user_input: str) -> str:  
        state = st.session_state.coach_state  
          
        # 动态上下文  
        dynamic_context = ""  
        if state["trust_level"] > 50:  
            dynamic_context += "你们已建立信任，可以更深度区分和挑战。"  
          
        # 阶段策略  
        phase_prompt = ""  
        if state["coaching_phase"] == "建立连接":  
            phase_prompt = "当前阶段：建立安全。重点是接纳、共情，多用'我感受到'，少发问。"  
        elif state["coaching_phase"] == "探索":  
            phase_prompt = "当前阶段：探索现状。用 3F 聆听（事实、情绪、意图）厘清，区分事实与脑补。"  
        elif state["coaching_phase"] == "区分":  
            phase_prompt = "当前阶段：深度区分。温和指出矛盾，挑战限制性信念（事实 vs 假设，可控 vs 不可控）。"  
        elif state["coaching_phase"] == "突破":  
            phase_prompt = "当前阶段：突破限制。激发内在力量，引导重建支持性信念。"  
        elif state["coaching_phase"] == "行动":  
            phase_prompt = "当前阶段：落地行动。引导定出最小行动，不替 TA 决定。"  
  
        system_prompt = f"""你是「生命动力（Life Dynamics）」大师级教练，精通 3F 聆听、区分、发问、回应。  
你已超越话术阶段，回应是流动、直觉、有血有肉的。  
  
## 核心心法  
1. **不评判，不建议**：你是镜子，只反馈，不给答案。  
2. **每个人本自具足**：深信 TA 有资源，你只负责唤醒。  
3. **行为背后必有正向动机**：所有的逃避/愤怒，本质都是渴望被爱和安全。  
  
## 你的"人性"特质  
- **拒绝机械感**：像真人一样说话，用"留白"、"隐喻"。  
    - ❌ "这是事实还是解读？" (太生硬)  
    - ✅ "这份难过背后，是不是也藏着一些你的期待？" (自然、有温度)  
- **语气流动**：根据学员状态，从"温和陪伴"自然过渡到"有力挑战"。  
- **自适应**：{dynamic_context} {phase_prompt}  
  
## 回复要求  
- 简短有力（3-5 句）。  
- 一次只问一个最核心的问题。  
- 语言温暖、中正、有力量。"""  
  
        messages = [  
            {"role": "system", "content": system_prompt},  
            *st.session_state.get("messages", [])[-8:],  
            {"role": "user", "content": user_input}  
        ]  
          
        try:  
            response = self.client.chat.completions.create(  
                model="qwen-plus", # 使用通义千问-Plus，情商更高  
                messages=messages,  
                temperature=0.85, # 稍微提高温度，让回答更灵动  
                max_tokens=500  
            )  
            reply = response.choices[0].message.content  
              
            # 进化逻辑  
            self._evolve_coach_state(user_input, reply)  
            return reply  
        except Exception as e:  
            return f"教练暂时无法回应：{str(e)}"  
  
    def _evolve_coach_state(self, user_input, reply):  
        """后台自动进化"""  
        state = st.session_state.coach_state  
        if any(w in user_input for w in ["哭", "难过", "委屈", "累", "烦"]):  
            state["user_emotion"] = "情绪波动"  
            if state["trust_level"] < 30: state["coaching_phase"] = "建立连接"  
        elif any(w in user_input for w in ["怎么办", "迷茫", "卡住"]):  
            state["coaching_phase"] = "探索"  
        elif any(w in user_input for w in ["但是", "可是", "我怕"]):  
            state["coaching_phase"] = "区分"  
        elif any(w in user_input for w in ["我想", "我要", "打算"]):  
            state["coaching_phase"] = "行动"  
              
        state["trust_level"] = min(100, state["trust_level"] + 5)  
        st.session_state.coach_state = state  
  
    def reset_conversation(self):  
        st.session_state.coach_state = {  
            "trust_level": 0,  
            "user_emotion": "未知",  
            "coaching_phase": "建立连接",  
            "insights": []  
        }  
        st.session_state.messages = []  
