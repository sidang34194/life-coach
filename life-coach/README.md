# 生命动力 · AI 教练小程序

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API Key
复制 `.env.example` 为 `.env`，填入你的智谱 AI API Key：
```bash
cp .env.example .env
```
编辑 `.env` 文件：
```
ZHIPU_API_KEY=你的API_KEY_粘贴在这里
```

> 获取 API Key：https://open.bigmodel.cn/ 注册后免费获取

### 3. 运行小程序
```bash
streamlit run main.py
```

浏览器会自动打开界面，开始与 AI 教练对话！

---

## 教练模式说明

| 模式 | 作用 |
|------|------|
| 🎧 聆听 | 接纳情绪，不打断，不评判 |
| ❓ 发问 | 提出有力问题，引导自我觉察 |
| 🔍 区分 | 帮用户看到盲点和矛盾 |
| 💬 回应 | 反馈+赋能，推动行动 |

---

## 项目结构
```
life-coach/
├── main.py              # 主界面
├── core/
│   └── coach_engine.py  # 教练对话引擎
├── utils/
│   └── config.py        # 配置管理
├── requirements.txt     # 依赖
├── .env.example         # 配置模板
└── README.md            # 说明文档
```
