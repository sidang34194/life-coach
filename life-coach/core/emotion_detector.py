"""情绪识别模块"""

class EmotionDetector:
    """简单的情绪识别"""
    
    # 情绪关键词库
    EMOTION_KEYWORDS = {
        "迷茫": ["迷茫", "不知道", "困惑", "不确定", "模糊", "方向", "意义"],
        "焦虑": ["焦虑", "紧张", "担心", "害怕", "压力", "睡不着", "心慌"],
        "愤怒": ["生气", "愤怒", "烦", "恼火", "不爽", "恨", "讨厌"],
        "悲伤": ["难过", "伤心", "痛苦", "哭", "失落", "绝望", "无助"],
        "无力": ["累", "疲惫", "无力", "没意思", "不想", "放弃", "算了"],
        "兴奋": ["开心", "兴奋", "期待", "激动", "棒", "太好了", "惊喜"],
        "孤独": ["孤独", "一个人", "没人理解", "没人懂", "寂寞", "空虚"],
        "愤怒": ["生气", "愤怒", "烦", "恼火", "不爽", "恨", "讨厌", "烦死了"],
    }
    
    # 话题分类
    TOPIC_KEYWORDS = {
        "关系": ["关系", "感情", "恋爱", "婚姻", "分手", "离婚", "伴侣", "朋友", "同事"],
        "事业": ["工作", "事业", "职场", "升职", "辞职", "创业", "老板", "同事", "领导"],
        "自我": ["自己", "自我", "价值", "自信", "自卑", "身份", "我是谁"],
        "家庭": ["父母", "妈妈", "爸爸", "家人", "孩子", "家庭", "原生家庭"],
        "金钱": ["钱", "经济", "财务", "债务", "收入", "贫穷", "富有"],
        "健康": ["健康", "身体", "病", "吃药", "医院", "失眠", "抑郁"],
        "成长": ["学习", "成长", "改变", "突破", "觉察", "修行", "修行"],
    }
    
    @classmethod
    def detect_emotion(cls, text: str) -> dict:
        """检测情绪"""
        text = text.lower()
        emotions = {}
        
        for emotion, keywords in cls.EMOTION_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    emotions[emotion] = emotions.get(emotion, 0) + 1
        
        # 返回最匹配的情绪
        if emotions:
            primary = max(emotions, key=emotions.get)
            return {"primary": primary, "all": emotions}
        return {"primary": "平静", "all": {}}
    
    @classmethod
    def detect_topic(cls, text: str) -> dict:
        """检测话题分类"""
        text = text.lower()
        topics = {}
        
        for topic, keywords in cls.TOPIC_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    topics[topic] = topics.get(topic, 0) + 1
        
        if topics:
            primary = max(topics, key=topics.get)
            return {"primary": primary, "all": topics}
        return {"primary": "综合", "all": {}}
    
    @classmethod
    def analyze(cls, text: str) -> dict:
        """综合分析"""
        return {
            "emotion": cls.detect_emotion(text),
            "topic": cls.detect_topic(text)
        }
