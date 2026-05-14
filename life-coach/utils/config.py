"""配置管理模块"""  
import os  
try:  
    import streamlit as st  
    _STREAMLIT_AVAILABLE = True  
except ImportError:  
    _STREAMLIT_AVAILABLE = False  
  
if _STREAMLIT_AVAILABLE and hasattr(st, "secrets") and "ZHIPU_API_KEY" in st.secrets:  
    _API_KEY = st.secrets["ZHIPU_API_KEY"]  
else:  
    from dotenv import load_dotenv  
    load_dotenv()  
    _API_KEY = os.getenv("ZHIPU_API_KEY", "")  
  
class Config:  
    ZHIPU_API_KEY = _API_KEY  
    ZHIPU_MODEL = "glm-4-flash"  
