"""大师级 AI 教练引擎 - 最终修复版 (Qwen-Turbo)"""  
import streamlit as st  
from openai import OpenAI  
  
class CoachEngine:  
    def __init__(self):  
        # 读取 Key  
        api_key = st.secrets.get("BAILIAN_API_KEY", "") or st.secrets.get("DASHSCOPE_API_KEY", "")  
        if not api_key:  
            raise ValueError("未配置 API Key")  
          
        self.client = OpenAI(  
            api_key=api_key,  
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1 ",  
        )  
          
        if "coach_state" not in st.session_state:  
            st.session_state.coach_state = {  
                "trust_level": 0,  
                "user_emotion": "未知",  
                "coaching_phase": "建立连接"  
            }  
  
    def get_response(self, user_input: str) -> str:  
        state = st.session_state.coach_state  
          
        # 动态策略  
        phase_prompt = f"当前阶段：{state['coaching_phase']}。请根据此阶段调整你的回应方式。"  
          
        system_prompt = f"""你是「生命动力」大师级教练。  
核心心法：不评判、不建议、每个人本自具足、行为背后有正向动机。  
风格：像真人一样说话，有温度、有留白，拒绝机械感。  
要求：简短有力（3-5 句），一次只问一个核心问题。  
{phase_prompt}"""  
  
        messages = [  
            {"role": "system", "content": system_prompt},  
            *st.session_state.get("messages", [])[-8:],  
            {"role": "user", "content": user_input}  
        ]  
          
        try:  
            # 使用官方稳定模型 qwen-turbo  
            response = self.client.chat.completions.create(  
                model="qwen-turbo",   
                messages=messages,  
                temperature=0.85,  
                max_tokens=500  
            )  
            reply = response.choices[0].message.content  
              
            # 记录消息  
            st.session_state.setdefault("messages", []).append({"role": "user", "content": user_input})  
            st.session_state.setdefault("messages", []).append({"role": "assistant", "content": reply})  
              
            # 进化逻辑  
            self._evolve_coach_state(user_input)  
            return reply  
              
        except Exception as e:  
            # 返回详细报错，方便排查  
            return f"❌ 模型调用失败：{str(e)}"  
  
    def _evolve_coach_state(self, user_input):  
        state = st.session_state.coach_state  
        if any(w in user_input for w in ["哭", "难过", "累"]):  
            state["coaching_phase"] = "建立连接"  
        elif any(w in user_input for w in ["怎么办", "迷茫"]):  
            state["coaching_phase"] = "探索"  
        elif any(w in user_input for w in ["但是", "可是"]):  
            state["coaching_phase"] = "区分"  
        elif any(w in user_input for w in ["我想", "我要"]):  
            state["coaching_phase"] = "行动"  
        state["trust_level"] = min(100, state["trust_level"] + 5)  
