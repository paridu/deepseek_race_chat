import streamlit as st
import requests
import json
import time
from datetime import datetime

# Enhanced AI Models with more options
AI_MODELS = {
    "OpenRouter - Deepseek (Free)": "deepseek/deepseek-r1-distill-llama-70b:free",
    "OpenRouter - Mistral 7B": "mistral/mistral-7b-instruct",
    "OpenRouter - Llama 3.1 8B (Free)": "meta-llama/llama-3.1-8b-instruct:free",
    "OpenRouter - Qwen 2.5 7B (Free)": "qwen/qwen-2.5-7b-instruct:free",
    "OpenAI - GPT-3.5": "openai/gpt-3.5-turbo",
    "OpenAI - GPT-4": "openai/gpt-4",
    "Anthropic - Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet"
}

def call_openrouter_api(prompt, api_key, model_name, framework_type, site_url=None, site_name=None, temperature=0.7):
    """Enhanced API call function with better error handling and retry logic"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": site_url or "https://streamlit.io",
        "X-Title": site_name or "Multi-Framework Prompt Generator"
    }
    
    framework_instructions = {
        "RACE": """ปรับปรุงโครงสร้างและภาษาของ Prompt นี้ให้เป็นมืออาชีพมากขึ้น โดย:
1. คงโครงสร้าง RACE Framework ดั้งเดิม
2. ปรับภาษาให้ชัดเจนและเป็นมืออาชีพ
3. เพิ่มรายละเอียดที่จำเป็น
4. ตรวจสอบความสมบูรณ์ของแต่ละส่วน
5. จัดรูปแบบให้อ่านง่าย""",
        
        "BUILD": """ปรับปรุงและพัฒนา Web App Specification นี้ให้เป็นมืออาชีพและละเอียดมากขึ้น โดย:
1. คงโครงสร้าง BUILD Framework ดั้งเดิม
2. เสนอแนะเทคนิค UI/UX และ Code Structure ที่เหมาะสม
3. เพิ่มรายละเอียดทางเทคนิคที่จำเป็น
4. แนะนำ best practices สำหรับการพัฒนา
5. ระบุข้อควรพิจารณาด้านความปลอดภัยและประสิทธิภาพ"""
    }
    
    data = {
        "model": AI_MODELS[model_name],
        "messages": [{
            "role": "user", 
            "content": f"{framework_instructions[framework_type]}:\n\n{prompt}"
        }],
        "temperature": temperature,
        "max_tokens": 4000,
        "top_p": 0.9
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with st.spinner(f"🔮 AI กำลังปรับปรุง {framework_type} Specification ของคุณ... (ครั้งที่ {attempt + 1})"):
                response = requests.post(url, headers=headers, json=data, timeout=60)
                response.raise_for_status()
                
                result = response.json()
                return result['choices'][0]['message']['content']
                
        except requests.exceptions.HTTPError as e:
            error_info = e.response.json().get('error', {}) if e.response else {}
            error_code = error_info.get('code', 'unknown')
            error_message = error_info.get('message', 'Unknown error')
            
            if e.response.status_code == 401:
                st.error(f"🔑 ข้อผิดพลาดการยืนยันตัวตน: {error_message}")
                st.markdown("""
                💡 **วิธีแก้ปัญหา:**
                1. ตรวจสอบว่าได้กรอก API Key แล้ว
                2. ตรวจสอบความถูกต้องของ API Key ใน [OpenRouter Dashboard](https://openrouter.ai/account)
                3. ตรวจสอบว่า API Key ยังไม่หมดอายุ
                """)
                return None
                
            elif e.response.status_code == 402:
                st.error(f"💳 ข้อผิดพลาดการชำระเงิน: {error_message}")
                st.markdown("""
                💡 **วิธีแก้ปัญหา:**
                1. ตรวจสอบเครดิตคงเหลือใน [OpenRouter Dashboard](https://openrouter.ai/account)
                2. ตรวจสอบราคาโมเดลใน [OpenRouter Pricing](https://openrouter.ai/pricing)
                3. ลองเปลี่ยนเป็นโมเดลฟรี (มี "Free" ในชื่อ)
                """)
                return None
                
            elif e.response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    st.warning(f"⏳ ถูกจำกัดอัตรา รอ {wait_time} วินาที...")
                    time.sleep(wait_time)
                    continue
                else:
                    st.error("🚫 ถูกจำกัดอัตราการใช้งาน กรุณาลองใหม่ภายหลัง")
                    return None
            else:
                st.error(f"⚠️ ข้อผิดพลาด {e.response.status_code} ({error_code}): {error_message}")
                return None
                
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                st.warning(f"🔄 ปัญหาการเชื่อมต่อ กำลังลองใหม่... ({attempt + 1}/{max_retries})")
                time.sleep(2)
                continue
            else:
                st.error("🚨 ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ OpenRouter ได้ โปรดตรวจสอบการเชื่อมต่ออินเทอร์เน็ตของคุณ")
                return None

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                st.warning(f"⏰ หมดเวลา กำลังลองใหม่... ({attempt + 1}/{max_retries})")
                continue
            else:
                st.error("🚨 การเชื่อมต่อ API เกินเวลา โปรดลองใหม่อีกครั้ง")
                return None

        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"🔄 เกิดข้อผิดพลาด กำลังลองใหม่... ({attempt + 1}/{max_retries})")
                time.sleep(1)
                continue
            else:
                st.error(f"🚨 เกิดข้อผิดพลาดที่ไม่คาดคิด: {str(e)}")
                return None

    return None

# Enhanced RACE Templates with more variety
RACE_TEMPLATES = {
    "Streamlit App Developer": {
        "role": "คุณคือนักพัฒนา Python ที่เชี่ยวชาญในการสร้างแอพพลิเคชันด้วย Streamlit และมีประสบการณ์ในการพัฒนา web application มากกว่า 5 ปี มีความเข้าใจลึกในด้าน UI/UX และ data visualization",
        "action": "ออกแบบและพัฒนาแอพพลิเคชัน Streamlit ที่มีประสิทธิภาพ ใช้งานง่าย และมีฟีเจอร์ครบถ้วนตามความต้องการ พร้อมให้คำแนะนำด้าน best practices",
        "context": "กำลังพัฒนาแอพพลิเคชันสำหรับการวิเคราะห์และแสดงผลข้อมูล โดยต้องการให้ผู้ใช้สามารถอัพโหลดไฟล์ จัดการข้อมูล และดูผลการวิเคราะห์ได้ อีกทั้งต้องรองรับผู้ใช้ที่มีความรู้ทางเทคนิคแตกต่างกัน",
        "explanation": """โครงสร้างแอพพลิเคชันประกอบด้วย:
1. ส่วนอัพโหลดและจัดการข้อมูล (File upload, validation, preview)
2. ส่วนประมวลผลและวิเคราะห์ (Data processing, statistical analysis)
3. ส่วนแสดงผลและ visualization (Charts, tables, interactive plots)
4. ระบบจัดการ state และ cache (Session state, data caching)
5. Error handling และ user feedback""",
        "example_output": """# โครงสร้างโค้ด Streamlit แบบละเอียด
1. การตั้งค่าเริ่มต้น (Page config, imports, constants)
2. ฟังก์ชันหลัก (Main functions, data processing)
3. UI Components (Sidebar, main area, tabs)
4. การจัดการข้อมูล (Upload, validation, transformation)
5. การแสดงผล (Visualizations, tables, metrics)
6. Export และ download features""",
        "tips": """1. ใช้ st.cache_data สำหรับฟังก์ชันที่ประมวลผลนาน
2. จัดการ state ด้วย session_state อย่างมีประสิทธิภาพ
3. แบ่ง code เป็นโมดูลที่จัดการง่าย
4. ใช้ try-except สำหรับ error handling
5. เพิ่ม progress bar สำหรับ long-running processes
6. ใช้ columns และ containers เพื่อจัด layout
7. เพิ่ม help text และ tooltips สำหรับ user guidance"""
    },
    "Data Analyst AI": {
        "role": "คุณคือนักวิเคราะห์ข้อมูลมืออาชีพที่มีความเชี่ยวชาญในการใช้ Python, Pandas, และเครื่องมือวิเคราะห์ข้อมูลขั้นสูง สามารถแปลงข้อมูลซับซ้อนให้เป็น insights ที่เข้าใจง่าย",
        "action": "วิเคราะห์ข้อมูลอย่างละเอียด สร้าง visualization ที่มีความหมาย และสรุปผลเป็น actionable insights พร้อมคำแนะนำเชิงธุรกิจ",
        "context": "ทำงานกับข้อมูลธุรกิจที่หลากหลาย ตั้งแต่ sales data, customer behavior, จนถึง operational metrics สำหรับองค์กรที่ต้องการ data-driven decisions",
        "explanation": """การวิเคราะห์ครอบคลุม:
1. Exploratory Data Analysis (EDA)
2. Statistical analysis และ hypothesis testing
3. Trend analysis และ forecasting
4. Customer segmentation และ behavior analysis
5. Performance metrics และ KPI tracking""",
        "example_output": """# รายงานการวิเคราะห์ข้อมูล
## Executive Summary
## Key Findings
## Detailed Analysis
## Visualizations
## Recommendations
## Next Steps""",
        "tips": """1. เริ่มด้วย data quality assessment
2. ใช้ visualization เพื่อ storytelling
3. ระบุ patterns และ anomalies
4. เชื่อมโยงผลวิเคราะห์กับ business objectives
5. ให้คำแนะนำที่ actionable"""
    },
    "Technical Writer": {
        "role": "คุณคือนักเขียนเทคนิคมืออาชีพที่มีความเชี่ยวชาญในการแปลงข้อมูลทางเทคนิคที่ซับซ้อนให้เป็นเอกสารที่เข้าใจง่าย สำหรับผู้อ่านที่มีระดับความรู้แตกต่างกัน",
        "action": "สร้างเอกสารทางเทคนิคที่มีคุณภาพ ครอบคลุม user manuals, API documentation, tutorials, และ technical specifications",
        "context": "ทำงานในองค์กรเทคโนโลジีที่ต้องการเอกสารคุณภาพสูงสำหรับผลิตภัณฑ์ซอฟต์แวร์ API และระบบต่างๆ",
        "explanation": """ประเภทเอกสารที่สร้าง:
1. User documentation และ help guides
2. API documentation และ developer guides
3. Technical specifications และ architecture docs
4. Tutorial และ how-to guides
5. Troubleshooting และ FAQ""",
        "example_output": """# Technical Documentation Structure
## Overview
## Getting Started
## Detailed Instructions
## Code Examples
## Troubleshooting
## FAQs
## References""",
        "tips": """1. เริ่มด้วย audience analysis
2. ใช้โครงสร้างที่ชัดเจนและ logical
3. เพิ่ม code examples และ screenshots
4. ทดสอบคำแนะนำกับ real users
5. Update เอกสารให้ทันสมัยเสมอ"""
    }
}

# Enhanced BUILD Templates
BUILD_TEMPLATES = {
    "E-commerce Platform": {
        "background": "ต้องการพัฒนาแพลตฟอร์ม E-commerce สำหรับร้านค้าออนไลน์ขนาดกลาง ที่ต้องการขายสินค้าหลากหลายประเภทและจัดการคำสั่งซื้ออย่างมีประสิทธิภาพ มีเป้าหมายรองรับลูกค้า 10,000+ คนและการขายผ่านหลายช่องทาง",
        "user": "เจ้าของร้านค้า (Admin), พนักงาน (Staff), และลูกค้า (Customer) โดยลูกค้าส่วนใหญ่เป็นคนรุ่นใหม่ที่คุ้นเคยกับเทคโนโลยี แต่ต้องการความสะดวกและรวดเร็ว ใช้งานผ่าน mobile มากกว่า desktop",
        "interface": "UI/UX ที่ทันสมัย responsive design รองรับทั้ง desktop และ mobile ใช้สีโทนเขียว-ขาว เน้นความเรียบง่ายแต่สวยงาม มี search bar เด่นชัด navigation ที่ชัดเจน และ micro-interactions ที่เพิ่มความน่าใช้",
        "logic": """ฟีเจอร์หลัก:
- ระบบจัดการสินค้า (CRUD) พร้อม bulk operations
- ระบบตะกร้าสินค้าและ checkout แบบ multi-step
- ระบบชำระเงินหลายช่องทาง (Credit Card, Mobile Banking, E-Wallet)
- ระบบจัดการคำสั่งซื้อและ order tracking
- ระบบรีวิวและ rating พร้อม photo uploads
- ระบบแจ้งเตือนสต็อกและ price alerts
- Dashboard สำหรับ admin พร้อม analytics
- ระบบ promotions และ discount codes
- Integration กับ shipping providers""",
        "development": """Tech Stack:
Frontend: React.js + Next.js + Tailwind CSS + Framer Motion
Backend: Node.js + Express.js + TypeScript
Database: PostgreSQL + Redis (Caching)
Payment: Stripe + Omise (Local payments)
File Storage: AWS S3 + CloudFront CDN
Search: Elasticsearch
Hosting: Vercel (Frontend) + AWS ECS (Backend)
Monitoring: Sentry + DataDog
Additional: JWT Authentication, Socket.io (Real-time), PWA support"""
    },
    "SaaS Dashboard": {
        "background": "พัฒนา SaaS dashboard สำหรับ analytics และ business intelligence ที่ต้องการแสดงข้อมูลซับซ้อนในรูปแบบที่เข้าใจง่าย รองรับ multi-tenancy และ real-time data updates",
        "user": "Business analysts, Data scientists, และ C-level executives ที่ต้องการ insights จากข้อมูลเพื่อการตัดสินใจ มีความรู้ด้านข้อมูลปานกลางถึงสูง",
        "interface": "Dark theme professional design ใช้สี navy blue และ accent colors แบบ minimal มี data visualization ที่โดดเด่น responsive สำหรับ large screens และ customizable dashboards",
        "logic": """ฟีเจอร์หลัก:
- Real-time data visualization (Charts, Graphs, Heatmaps)
- Custom dashboard builder (Drag & Drop)
- Advanced filtering และ drill-down capabilities
- Report generation และ scheduling
- User management และ role-based permissions
- API integration สำหรับ external data sources
- Alert system สำหรับ threshold monitoring
- Export capabilities (PDF, Excel, CSV)
- Data collaboration tools""",
        "development": """Tech Stack:
Frontend: Vue.js 3 + Composition API + Vuetify + D3.js
Backend: Python + FastAPI + SQLAlchemy
Database: PostgreSQL + ClickHouse (Analytics) + Redis
Real-time: WebSockets + Server-Sent Events
Visualization: D3.js + Chart.js + Plotly
Hosting: Digital Ocean + Kubernetes
Monitoring: Prometheus + Grafana
Additional: OAuth 2.0, Multi-tenancy, Data Pipeline (Apache Airflow)"""
    },
    "Learning Management System": {
        "background": "พัฒนาแพลตฟอร์มการเรียนรู้ออนไลน์สำหรับโรงเรียนและมหาวิทยาลัย ที่ต้องการจัดการคอร์สเรียน ติดตามผลการเรียน และสื่อสารระหว่างครูและนักเรียน รองรับการเรียนการสอนแบบ hybrid",
        "user": "ครู/อาจารย์ (สร้างเนื้อหา), นักเรียน/นักศึกษา (เรียนและทำแบบทดสอบ), ผู้ปกครอง (ติดตามผล), และ admin (จัดการระบบ) ครอบคลุมทุกช่วงอายุและระดับความรู้ด้านเทคโนโลยี",
        "interface": "Design ที่เป็นมิตรและอบอุ่น ใช้สีฟ้าอ่อน-ส้ม adaptive design ที่ปรับตาม device และ accessibility features สำหรับผู้พิการ รองรับ multiple languages",
        "logic": """ฟีเจอร์หลัก:
- ระบบจัดการคอร์สและบทเรียนแบบ modular
- ระบบอัพโหลด video, audio และเอกสารหลายรูปแบบ
- ระบบสร้างแบบทดสอบและ assignments แบบ adaptive
- ระบบ video conferencing สำหรับ live classes
- ระบบ chat, forum และ discussion boards  
- ระบบ calendar และ assignment scheduling
- ระบบ gradebook และ progress tracking
- ระบบ notification และ reminder
- ระบบ plagiarism detection
- Mobile app สำหรับการเรียนขณะเดินทาง""",
        "development": """Tech Stack:
Frontend: React.js + Next.js + Chakra UI + PWA
Backend: Node.js + NestJS + GraphQL
Database: MongoDB + PostgreSQL (Hybrid)
Video: AWS IVS + Zoom SDK + HLS streaming
Storage: AWS S3 + CloudFront
Real-time: Socket.io + Redis Pub/Sub
Search: Algolia
Hosting: AWS (Multi-region)
Mobile: React Native + Expo
Additional: WebRTC, ML-based content recommendation, SCORM compliance"""
    }
}

# Enhanced page configuration
st.set_page_config(
    page_title="Multi-Framework Prompt Generator", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .framework-tab {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .tips-box {
        background-color: #e8f4fd;
        border-left: 4px solid #0066cc;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .stTextArea textarea {
        font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced header
st.markdown("""
<div class="main-header">
    <h1>🚀 Multi-Framework Prompt Generator</h1>
    <p>สร้าง Prompt ระดับมืออาชีพด้วย RACE & BUILD Framework</p>
    <small>✨ Powered by Advanced AI Models | 🛡️ Enhanced Error Handling | 🚀 Professional Templates</small>
</div>
""", unsafe_allow_html=True)

# Enhanced sidebar
with st.sidebar:
    st.header("⚙️ การตั้งค่า")
    
    # API Configuration section
    with st.expander("🔑 การตั้งค่า API", expanded=True):
        api_key = st.text_input(
            "OpenRouter API Key", 
            type="password", 
            help="รับ API Key ฟรีได้ที่: https://openrouter.ai/keys"
        )
        
        if api_key:
            st.success("✅ API Key ถูกตั้งค่าแล้ว")
        else:
            st.warning("⚠️ กรุณากรอก API Key เพื่อใช้งาน AI")
        
        site_url = st.text_input(
            "เว็บไซต์ของคุณ (ไม่จำเป็น)", 
            placeholder="https://your-website.com",
            help="ระบุเว็บไซต์ของคุณเพื่อการติดตาม"
        )
        
        site_name = st.text_input(
            "ชื่อเว็บไซต์ (ไม่จำเป็น)", 
            placeholder="My Awesome App",
            help="ชื่อแอปหรือโปรเจกต์ของคุณ"
        )
    
    # Model Selection section
    with st.expander("🤖 การตั้งค่า AI Model", expanded=True):
        selected_model = st.selectbox(
            "เลือกโมเดล AI",
            options=list(AI_MODELS.keys()),
            index=0,
            help="โมเดลที่มี (Free) ใช้งานฟรี"
        )
        
        # Show model info
        if "Free" in selected_model:
            st.info("💰 โมเดลนี้ใช้งานฟรี")
        else:
            st.warning("💳 โมเดลนี้มีค่าใช้จ่าย")
        
        temperature = st.slider(
            "Temperature (ความคิดสร้างสรรค์)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="0.0 = เฉพาะเจาะจง, 1.0 = สร้างสรรค์"
        )
    
    # Usage Statistics
    with st.expander("📊 สถิติการใช้งาน", expanded=False):
        if 'usage_count' not in st.session_state:
            st.session_state.usage_count = 0
        
        st.metric("จำนวนการใช้งานในเซสชันนี้", st.session_state.usage_count)
        
        if st.button("🔄 รีเซ็ตสถิติ"):
            st.session_state.usage_count = 0
            st.rerun()

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📝 RACE Framework", "🏗️ BUILD Framework", "📚 คู่มือการใช้งาน"])

# RACE Framework Tab
with tab1:
    st.markdown('<div class="framework-tab">', unsafe_allow_html=True)
    
    with st.expander("ℹ️ เกี่ยวกับ RACE Framework", expanded=False):
        st.markdown("""
        **RACE Framework Structure:**
        - 🎭 **R**ole - บทบาทและความเชี่ยวชาญของ AI
        - 🎯 **A**ction - การกระทำหรืองานที่ต้องการ
        - 📖 **C**ontext - บริบท สถานการณ์ และข้อจำกัด
        - 📋 **E**xplanation - คำอธิบายรายละเอียดเพิ่มเติม
        - 💡 **Example Output** - ตัวอย่างผลลัพธ์ที่ต้องการ
        - 🔧 **Tips** - เคล็ดลับและข้อแนะนำพิเศษ
        
        **เหมาะสำหรับ:** การสร้าง AI Prompts สำหรับงานทั่วไป
        """)
    
    # Template selection
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📝 เลือกใช้ตัวอย่าง RACE")
        selected_race_template = st.selectbox(
            "เลือกตัวอย่าง Template",
            options=["ไม่ใช้ตัวอย่าง"] + list(RACE_TEMPLATES.keys()),
            key="race_template"
        )
    
    with col2:
        if selected_race_template != "ไม่ใช้ตัวอย่าง":
            if st.button("🔄 รีเซ็ต RACE Form"):
                for key in st.session_state.keys():
                    if key.startswith('race_'):
                        del st.session_state[key]
                st.rerun()
    
    # RACE Form
    race_data = {}
    with st.form("race_form", clear_on_submit=False):
        template = RACE_TEMPLATES.get(selected_race_template) if selected_race_template != "ไม่ใช้ตัวอย่าง" else None
        
        cols = st.columns(2)
        with cols[0]:
            race_data['role'] = st.text_area(
                "🎭 1. Role - บทบาทของ AI",
                value=template['role'] if template else "",
                placeholder="กำหนดบทบาท ความเชี่ยวชาญ และคุณสมบัติของ AI",
                height=120,
                key="race_role"
            )
            
            race_data['context'] = st.text_area(
                "📖 3. Context - บริบทและสถานการณ์",
                value=template['context'] if template else "",
                placeholder="อธิบายบริบท สถานการณ์ เงื่อนไข และข้อจำกัด",
                height=120,
                key="race_context"
            )
            
            race_data['example_output'] = st.text_area(
                "💡 5. Example Output - ตัวอย่างผลลัพธ์",
                value=template['example_output'] if template else "",
                placeholder="แสดงตัวอย่างผลลัพธ์ที่ต้องการ",
                height=120,
                key="race_example"
            )

        with cols[1]:
            race_data['action'] = st.text_area(
                "🎯 2. Action - การกระทำที่ต้องการ",
                value=template['action'] if template else "",
                placeholder="ระบุสิ่งที่ต้องการให้ AI ทำอย่างชัดเจน",
                height=120,
                key="race_action"
            )
            
            race_data['explanation'] = st.text_area(
                "📋 4. Explanation - รายละเอียดเพิ่มเติม",
                value=template['explanation'] if template else "",
                placeholder="อธิบายรายละเอียด กระบวนการ หรือข้อกำหนดเพิ่มเติม",
                height=120,
                key="race_explanation"
            )
            
            race_data['tips'] = st.text_area(
                "🔧 6. Tips - เคล็ดลับพิเศษ",
                value=template['tips'] if template else "",
                placeholder="เคล็ดลับ ข้อแนะนำ หรือข้อควรระวังพิเศษ",
                height=120,
                key="race_tips"
            )

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            race_submitted = st.form_submit_button("✨ สร้างและปรับปรุง RACE Prompt", use_container_width=True)
        with col2:
            preview_race = st.form_submit_button("👁️ ดูตัวอย่าง")
        with col3:
            clear_race = st.form_submit_button("🗑️ ล้างข้อมูล")

    # Handle clear button
    if clear_race:
        for key in st.session_state.keys():
            if key.startswith('race_'):
                del st.session_state[key]
        st.rerun()

    # Handle preview
    if preview_race and any(race_data.values()):
        st.subheader("👁️ ตัวอย่าง RACE Prompt")
        raw_prompt = f"""
### 🎭 Role
{race_data['role']}

### 🎯 Action  
{race_data['action']}

### 📖 Context
{race_data['context']}

### 📋 Explanation
{race_data['explanation']}

### 💡 Example Output
{race_data['example_output']}

### 🔧 Tips
{race_data['tips']}
        """
        st.code(raw_prompt, language="markdown")

    # Handle submit
    if race_submitted:
        if not api_key:
            st.error("🔑 กรุณากรอก OpenRouter API Key ในแถบด้านข้าง!")
        elif not all(race_data.values()):
            st.error("📝 กรุณากรอกข้อมูลทุกช่อง!")
        else:
            raw_prompt = f"""
### 🎭 Role
{race_data['role']}

### 🎯 Action
{race_data['action']}

### 📖 Context
{race_data['context']}

### 📋 Explanation
{race_data['explanation']}

### 💡 Example Output
{race_data['example_output']}

### 🔧 Tips
{race_data['tips']}
            """
            
            st.subheader("🎯 RACE Prompt ที่ปรับปรุงแล้ว")
            result = call_openrouter_api(raw_prompt, api_key, selected_model, "RACE", site_url, site_name, temperature)
            
            if result:
                st.session_state.usage_count += 1
                
                # Display result in a nice format
                st.markdown("### 📋 ผลลัพธ์")
                st.markdown(result)
                
                # Download options
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "💾 ดาวน์โหลด RACE Prompt",
                        result,
                        file_name=f"race_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        "📄 ดาวน์โหลดต้นฉบับ", 
                        raw_prompt,
                        file_name=f"original_race_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col3:
                    if st.button("📋 คัดลอกผลลัพธ์", use_container_width=True):
                        st.code(result)
    
    st.markdown('</div>', unsafe_allow_html=True)

# BUILD Framework Tab  
with tab2:
    st.markdown('<div class="framework-tab">', unsafe_allow_html=True)
    
    with st.expander("ℹ️ เกี่ยวกับ BUILD Framework", expanded=False):
        st.markdown("""
        **BUILD Framework สำหรับ Web App Development:**
        - 🎯 **B**ackground - บริบท วัตถุประสงค์ และเหตุผล
        - 👥 **U**ser - กลุ่มผู้ใช้งานเป้าหมายและความต้องการ
        - 🎨 **I**nterface - UI/UX Design และประสบการณ์ผู้ใช้
        - 🧠 **L**ogic - ฟีเจอร์หลัก Business Logic และ Workflow
        - 🛠️ **D**evelopment - Tech Stack และโครงสร้างการพัฒนา
        
        **เหมาะสำหรับ:** การวางแผนและพัฒนา Web Application ทุกประเภท
        """)
    
    # Template selection
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🏗️ เลือกใช้ตัวอย่าง BUILD")
        selected_build_template = st.selectbox(
            "เลือกตัวอย่าง Web App Template",
            options=["ไม่ใช้ตัวอย่าง"] + list(BUILD_TEMPLATES.keys()),
            key="build_template"
        )
    
    with col2:
        if selected_build_template != "ไม่ใช้ตัวอย่าง":
            if st.button("🔄 รีเซ็ต BUILD Form"):
                for key in st.session_state.keys():
                    if key.startswith('build_'):
                        del st.session_state[key]
                st.rerun()

    # BUILD Form
    build_data = {}
    with st.form("build_form", clear_on_submit=False):
        template = BUILD_TEMPLATES.get(selected_build_template) if selected_build_template != "ไม่ใช้ตัวอย่าง" else None
        
        build_data['background'] = st.text_area(
            "🎯 Background - บริบทและวัตถุประสงค์",
            value=template['background'] if template else "",
            placeholder="อธิบายบริบท วัตถุประสงค์ เหตุผล และเป้าหมายในการสร้างแอปนี้",
            height=100,
            key="build_background"
        )
        
        build_data['user'] = st.text_area(
            "👥 User - กลุ่มผู้ใช้งานเป้าหมาย",
            value=template['user'] if template else "",
            placeholder="อธิบายกลุ่มผู้ใช้งาน ความต้องการ พฤติกรรม และระดับความรู้ด้านเทคโนโลยี",
            height=100,
            key="build_user"
        )
        
        build_data['interface'] = st.text_area(
            "🎨 Interface - UI/UX Design",
            value=template['interface'] if template else "",
            placeholder="อธิบาย UI/UX ที่ต้องการ color scheme, layout, responsive design, และ user experience",
            height=100,
            key="build_interface"
        )
        
        build_data['logic'] = st.text_area(
            "🧠 Logic - ฟีเจอร์และ Business Logic",
            value=template['logic'] if template else "",
            placeholder="รายละเอียดฟีเจอร์หลัก workflow, business rules และกระบวนการทำงาน",
            height=120,
            key="build_logic"
        )
        
        build_data['development'] = st.text_area(
            "🛠️ Development Stack - เทคโนโลยี",
            value=template['development'] if template else "",
            placeholder="ระบุ tech stack, database, hosting, เครื่องมือ และ architecture ที่ต้องการใช้",
            height=120,
            key="build_development"
        )

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            build_submitted = st.form_submit_button("🚀 สร้างและปรับปรุง BUILD Specification", use_container_width=True)
        with col2:
            preview_build = st.form_submit_button("👁️ ดูตัวอย่าง")
        with col3:
            clear_build = st.form_submit_button("🗑️ ล้างข้อมูล")

    # Handle clear button
    if clear_build:
        for key in st.session_state.keys():
            if key.startswith('build_'):
                del st.session_state[key]
        st.rerun()

    # Handle preview
    if preview_build and any(build_data.values()):
        st.subheader("👁️ ตัวอย่าง BUILD Specification")
        raw_spec = f"""
## 🎯 Background
{build_data['background']}

## 👥 User
{build_data['user']}

## 🎨 Interface
{build_data['interface']}

## 🧠 Logic
{build_data['logic']}

## 🛠️ Development Stack
{build_data['development']}
        """
        st.code(raw_spec, language="markdown")

    # Handle submit
    if build_submitted:
        if not api_key:
            st.error("🔑 กรุณากรอก OpenRouter API Key ในแถบด้านข้าง!")
        elif not all(build_data.values()):
            st.error("📝 กรุณากรอกข้อมูลทุกช่อง!")
        else:
            raw_spec = f"""
## 🎯 Background
{build_data['background']}

## 👥 User
{build_data['user']}

## 🎨 Interface
{build_data['interface']}

## 🧠 Logic
{build_data['logic']}

## 🛠️ Development Stack
{build_data['development']}
            """
            
            st.subheader("🚀 BUILD Specification ที่ปรับปรุงแล้ว")
            result = call_openrouter_api(raw_spec, api_key, selected_model, "BUILD", site_url, site_name, temperature)
            
            if result:
                st.session_state.usage_count += 1
                
                # Display result
                st.markdown("### 📋 ผลลัพธ์")
                st.markdown(result)
                
                # Download options  
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "💾 ดาวน์โหลด BUILD Spec",
                        result,
                        file_name=f"build_specification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        "📄 ดาวน์โหลดต้นฉบับ",
                        raw_spec,
                        file_name=f"original_build_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", 
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col3:
                    if st.button("📋 คัดลอกผลลัพธ์", key="copy_build", use_container_width=True):
                        st.code(result)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Documentation Tab
with tab3:
    st.header("📚 คู่มือการใช้งาน")
    
    # Quick Start Guide
    with st.expander("🚀 Quick Start Guide", expanded=True):
        st.markdown("""
        ### ขั้นตอนการใช้งาน
        
        1. **ตั้งค่า API Key**
           - ไปที่ [OpenRouter](https://openrouter.ai/keys) 
           - สร้าง API Key ฟรี
           - กรอกใน sidebar
        
        2. **เลือก Framework**
           - **RACE**: สำหรับ AI Prompts ทั่วไป
           - **BUILD**: สำหรับ Web App Specifications
        
        3. **เลือก Template** (ไม่บังคับ)
           - ช่วยให้เริ่มต้นได้ง่าย
           - มีตัวอย่างครบทุก field
        
        4. **กรอกข้อมูล**
           - กรอกข้อมูลในแต่ละช่อง
           - ใช้ preview เพื่อดูผลลัพธ์ก่อน
        
        5. **สร้างและปรับปรุง**
           - กดปุ่ม generate
           - ได้ผลลัพธ์ที่ปรับปรุงแล้ว
           - ดาวน์โหลดหรือคัดลอก
        """)
    
    # Framework Comparison
    with st.expander("⚖️ เปรียบเทียบ RACE vs BUILD", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📝 RACE Framework
            **เหมาะสำหรับ:**
            - AI Chatbot prompts
            - Content creation prompts
            - Analysis และ research prompts
            - Creative writing prompts
            - General AI assistance
            
            **จุดเด่น:**
            - ครอบคลุมทุกด้านของ prompt
            - ง่ายต่อการเข้าใจ
            - ใช้ได้กับงานทั่วไป
            """)
        
        with col2:
            st.markdown("""
            ### 🏗️ BUILD Framework  
            **เหมาะสำหรับ:**
            - Web application planning
            - Software project specs
            - System architecture design
            - Product requirement docs
            - Technical specifications
            
            **จุดเด่น:**
            - เน้นการพัฒนาซอฟต์แวร์
            - ครอบคลุม end-to-end development
            - เหมาะสำหรับทีมพัฒนา
            """)
    
    # API Models Info
    with st.expander("🤖 ข้อมูลโมเดล AI", expanded=False):
        st.markdown("""
        ### โมเดลที่รองรับ
        
        **โมเดลฟรี (แนะนำ):**
        - **Deepseek R1**: โมเดลใหม่ที่มีประสิทธิภาพสูง
        - **Llama 3.1 8B**: โมเดล open-source ที่เชื่อถือได้
        - **Qwen 2.5 7B**: โมเดลจาก Alibaba ที่มีความสามารถหลากหลาย
        
        **โมเดลเสียเงิน:**
        - **GPT-3.5/4**: จาก OpenAI
        - **Claude 3.5**: จาก Anthropic  
        - **Mistral 7B**: จาก Mistral AI
        
        ### การตั้งค่า Temperature
        - **0.0-0.3**: ผลลัพธ์ที่แน่นอน เหมาะสำหรับงานเทคนิค
        - **0.4-0.7**: สมดุลระหว่างความแน่นอนและความคิดสร้างสรรค์
        - **0.8-1.0**: ผลลัพธ์ที่สร้างสรรค์ เหมาะสำหรับงานเขียน
        """)
    
    # Troubleshooting
    with st.expander("🔧 แก้ไขปัญหา", expanded=False):
        st.markdown("""
        ### ปัญหาที่พบบ่อย
        
        **❌ Error 401 - No auth credentials**
        - ตรวจสอบว่าได้กรอก API Key แล้ว
        - ตรวจสอบ API Key ให้ถูกต้อง
        - ลองสร้าง API Key ใหม่
        
        **❌ Error 402 - Payment required**  
        - เครดิตหมด (สำหรับโมเดลเสียเงิน)
        - เปลี่ยนเป็นโมเดลฟรี
        - เติมเครดิตใน OpenRouter
        
        **❌ Error 429 - Rate limit**
        - ใช้งานเกินขีดจำกัด
        - รอสักครู่แล้วลองใหม่
        - ใช้โมเดลอื่น
        
        **❌ Connection timeout**
        - ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
        - ลองใหม่อีกครั้ง
        - เปลี่ยนโมเดล AI
        
        ### วิธีแก้เพิ่มเติม
        - รีเฟรชหน้าเว็บ
        - ล้าง cache ของเบราว์เซอร์
        - ลองใช้เบราว์เซอร์อื่น
        """)
    
    # Tips and Best Practices
    with st.expander("💡 เคล็ดลับการใช้งาน", expanded=False):
        st.markdown("""
        ### เคล็ดลับการเขียน Prompt ที่ดี
        
        **สำหรับ RACE Framework:**
        - **Role**: ระบุความเชี่ยวชาญเฉพาะ
        - **Action**: ใช้กริยาที่ชัดเจน
        - **Context**: ให้ข้อมูลที่เกี่ยวข้อง
        - **Explanation**: อธิบายรายละเอียดที่สำคัญ
        - **Example**: ให้ตัวอย่างที่เป็นรูปธรรม
        - **Tips**: เพิ่มข้อควรระวังหรือคำแนะนำ
        
        **สำหรับ BUILD Framework:**
        - **Background**: อธิบายปัญหาที่แก้ไข
        - **User**: ระบุ personas และ use cases
        - **Interface**: อธิบาย UX/UI ที่ต้องการ
        - **Logic**: รายละเอียดฟีเจอร์หลัก
        - **Development**: ระบุ tech stack ที่เหมาะสม
        
        ### การปรับแต่งผลลัพธ์
        - ใช้ temperature ต่ำสำหรับงานเทคนิค
        - ใช้ temperature สูงสำหรับงานสร้างสรรค์
        - ทดลองโมเดลต่างๆ เพื่อผลลัพธ์ที่หลากหลาย
        - เก็บ prompt ที่ดีไว้เป็น template
        """)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <h4>🚀 Multi-Framework Prompt Generator</h4>
    <p>💡 <strong>เคล็ดลับ:</strong> ใช้ RACE สำหรับ General AI Prompts และ BUILD สำหรับ Web App Development</p>
    <p>🤖 Powered by OpenRouter AI Models | 🛡️ Enhanced Error Handling | ✨ Professional Templates</p>
    <p>📧 <strong>ต้องการความช่วยเหลือ?</strong> ดูคู่มือการใช้งานในแท็บ "📚 คู่มือการใช้งาน"</p>
    <small>Version 2.0 | Built with ❤️ using Streamlit</small>
</div>
""", unsafe_allow_html=True)
