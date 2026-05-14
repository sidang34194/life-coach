"""教练对话引擎"""
from zhipuai import ZhipuAI
from utils.config import Config

class CoachEngine:
    """AI 教练对话引擎"""
    
    def __init__(self):
        """初始化引擎"""
        if not Config.ZHIPU_API_KEY or Config.ZHIPU_API_KEY == "你的API_KEY粘贴在这里":
            raise ValueError("请先在 .env 文件中配置 ZHIPU_API_KEY")
        
        self.client = ZhipuAI(api_key=Config.ZHIPU_API_KEY)
        self.conversation_history = []
    
    def get_response(self, user_input: str, mode: str = "聆听") -> str:
        """获取 AI 教练回复"""
        
        # 构建当前模式的系统提示词
        mode_prompt = Config.COACH_MODES.get(mode, Config.COACH_MODES["聆听"])
        system_prompt = f"{Config.COACH_SYSTEM_PROMPT}\n\n{mode_prompt}"
        
        # 构建对话历史
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history,
            {"role": "user", "content": user_input}
        ]
        
        # 调用 API
        try:
            response = self.client.chat.completions.create(
                model=Config.ZHIPU_MODEL,
                messages=messages,
                temperature=0.8,  # 稍微有创意，但保持专业
                max_tokens=500
            )
            
            reply = response.choices[0].message.content
            
            # 保存对话历史（保留最近10轮）
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return reply
            
        except Exception as e:
            return f"抱歉，教练暂时无法回应。请检查 API Key 是否正确。\n错误信息：{str(e)}"
    
    def reset_conversation(self):
        """重置对话"""
        self.conversation_history = []
