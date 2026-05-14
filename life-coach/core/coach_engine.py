"""教练对话引擎 - 自动模式版"""  
from zhipuai import ZhipuAI  
from utils.config import Config  
  
class CoachEngine:  
    def __init__(self):  
        if not Config.ZHIPU_API_KEY:  
            raise ValueError("API Key 未配置")  
        self.client = ZhipuAI(api_key=Config.ZHIPU_API_KEY)  
        self.conversation_history = []  
      
    def get_response(self, user_input: str) -> str:  
        system_prompt = """你是一位专业的生命动力教练。你不需要用户选择模式，你会根据用户当前的状态和对话进展，自动判断该用哪种方式回应：  
  
1. **聆听** - 当用户刚开口、情绪较重、需要被理解时，先聆听接纳  
2. **发问** - 当用户表达了一些想法但还不够清晰时，提出有力问题引导觉察  
3. **区分** - 当用户出现盲点、矛盾、或混淆事实与解读时，温和地指出  
4. **回应** - 当用户有了觉察、情绪稳定时，给予赋能并推动行动  
  
核心原则：  
- 不评判、不说教、不给标准答案  
- 用提问引导用户自己发现答案  
- 接纳用户的情绪，让用户感到被理解  
- 每次回复控制在3-5句话以内"""  
          
        messages = [  
            {"role": "system", "content": system_prompt},  
            *self.conversation_history,  
            {"role": "user", "content": user_input}  
        ]  
          
        try:  
            response = self.client.chat.completions.create(  
                model=Config.ZHIPU_MODEL,  
                messages=messages,  
                temperature=0.8,  
                max_tokens=500  
            )  
            reply = response.choices[0].message.content  
            self.conversation_history.append({"role": "user", "content": user_input})  
            self.conversation_history.append({"role": "assistant", "content": reply})  
            if len(self.conversation_history) > 20:  
                self.conversation_history = self.conversation_history[-20:]  
            return reply  
        except Exception as e:  
            return f"抱歉，教练暂时无法回应。错误：{str(e)}"  
      
    def reset_conversation(self):  
        self.conversation_history = []  
