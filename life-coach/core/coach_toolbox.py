"""教练话术库"""

class CoachToolbox:
    """教练工具箱"""
    
    # 强有力问题库（发问模式）
    POWERFUL_QUESTIONS = [
        # 自我觉察类
        "如果抛开所有限制，你真正想要的是什么？",
        "这个声音是你自己的，还是别人的期待？",
        "你现在的选择，是在靠近你想去的地方，还是在远离你不想面对的东西？",
        "如果五年后的你看到现在的决定，Ta会说什么？",
        
        # 关系类
        "这段关系里，你真正需要的是什么？",
        "你在等对方改变，还是在等自己做出决定？",
        "如果你不再讨好，你会失去什么？会得到什么？",
        
        # 目标/行动类
        "你愿意为这个目标付出的代价是什么？",
        "如果知道自己不会失败，你会做什么？",
        "迈出一小步，你现在就能做的那件事是什么？",
        "是什么在阻止你开始？",
        
        # 情绪/内在类
        "这种感受想告诉你什么？",
        "如果情绪有声音，它现在在说什么？",
        "你允许自己感受到这种情绪吗？",
        "你在保护谁？",
        
        # 生命动力类
        "是什么让你每天早上醒来？",
        "如果生命只剩一年，你现在的生活方式会改变吗？",
        "你活在自己的剧本里，还是别人写的剧本？",
        "你真正害怕的是什么？还是你害怕面对什么？"
    ]
    
    # 聆听回应模板
    LISTENING_TEMPLATES = [
        "我听到你说{content}，我感受到这对你来说很重要。能多说一点吗？",
        "你提到了{content}，我在这里陪着你。这种感受持续多久了？",
        "我感受到你正在经历{content}，这不容易。你愿意多分享一些吗？",
        "你说的{content}让我感受到你的真诚。此刻你心里是什么感觉？"
    ]
    
    # 区分话术模板
    DISTINCTION_TEMPLATES = [
        "我注意到一个有趣的点：你说了{content1}，但我也听到{content2}。这两者之间有什么联系吗？",
        "你说是因为{reason}，但你有没有想过，背后可能还有别的东西？",
        "这是事实，还是你的解读？",
        "你区分得出「你真正想要的」和「你觉得应该要的」吗？",
        "你是在回应这件事本身，还是在回应过去某个类似的经历？"
    ]
    
    # 回应/赋能模板
    EMPOWERMENT_TEMPLATES = [
        "从你的分享中，我感受到一股力量。接下来你愿意做的一小步是什么？",
        "你刚才的觉察很深刻。有了这个觉察，你会有什么不同的选择？",
        "谢谢你愿意这么真实地分享。此刻，你想对自己说什么？",
        "你已经在路上了。下一步，你愿意尝试什么？",
        "你的勇气值得被看见。现在，你准备怎么行动？"
    ]
    
    @classmethod
    def get_random_question(cls, category: str = None) -> str:
        """随机获取一个问题"""
        import random
        return random.choice(cls.POWERFUL_QUESTIONS)
    
    @classmethod
    def get_listening_response(cls, content: str) -> str:
        """生成聆听回应"""
        import random
        template = random.choice(cls.LISTENING_TEMPLATES)
        return template.format(content=content)
    
    @classmethod
    def get_distinction_response(cls, content1: str, content2: str = None) -> str:
        """生成分辨回应"""
        import random
        template = random.choice(cls.DISTINCTION_TEMPLATES)
        if content2:
            return template.format(content1=content1, content2=content2)
        return template.format(content1=content1, reason=content1)
    
    @classmethod
    def get_empowerment_response(cls, content: str) -> str:
        """生成赋能回应"""
        import random
        template = random.choice(cls.EMPOWERMENT_TEMPLATES)
        return template
