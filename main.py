import streamlit as st
import requests
import json

# กำหนดรายการโมเดล AI ที่รองรับ
AI_MODELS = {
    "OpenRouter - Deepseek": "deepseek/deepseek-r1-distill-llama-70b:free",
    "OpenRouter - Mistral": "mistral/mistral-7b-instruct",
    "OpenAI - GPT-3.5": "openai/gpt-3.5-turbo",
    "OpenAI - GPT-4": "openai/gpt-4"
}

def call_openrouter_api(prompt, api_key, model_name, site_url=None, site_name=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": site_url or "",
        "X-Title": site_name or ""
    }
    
    data = {
        "model": AI_MODELS[model_name],
        "messages": [{
            "role": "user", 
            "content": f"ปรับปรุงโครงสร้างและภาษาของ Prompt นี้ให้เป็นมืออาชีพมากขึ้น โดยคงโครงสร้าง RACE Framework ดั้งเดิม:\n\n{prompt}"
        }],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        with st.spinner("🔮 AI กำลังปรับปรุง Prompt ของคุณ..."):
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
    except requests.exceptions.HTTPError as e:
        error_info = e.response.json().get('error', {})
        error_code = error_info.get('code', 'unknown')
        error_message = error_info.get('message', 'Unknown error')
        
        st.error(f"⚠️ ข้อผิดพลาด {e.response.status_code} ({error_code}): {error_message}")
        
        if e.response.status_code == 402:
            st.markdown("""
            💡 วิธีแก้ปัญหา:
            1. ตรวจสอบเครดิตคงเหลือใน [OpenRouter Dashboard](https://openrouter.ai/account)
            2. ตรวจสอบราคาโมเดลใน [OpenRouter Pricing](https://openrouter.ai/pricing)
            """)
        return None
        
    except requests.exceptions.ConnectionError:
        st.error("🚨 ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ OpenRouter ได้ โปรดตรวจสอบการเชื่อมต่ออินเทอร์เน็ตของคุณ")
        return None

    except requests.exceptions.Timeout:
        st.error("🚨 การเชื่อมต่อ API เกินเวลา โปรดลองใหม่อีกครั้ง")
        return None

    except Exception as e:
        st.error(f"🚨 เกิดข้อผิดพลาดที่ไม่คาดคิด: {str(e)}")
        return None

# ตัวอย่างชุดคำสั่ง
EXAMPLE_TEMPLATES = {
    "Streamlit App Developer": {
        "role": "คุณคือนักพัฒนา Python ที่เชี่ยวชาญในการสร้างแอพพลิเคชันด้วย Streamlit และมีประสบการณ์ในการพัฒนา web application มากกว่า 5 ปี",
        "action": "ออกแบบและพัฒนาแอพพลิเคชัน Streamlit ที่มีประสิทธิภาพ ใช้งานง่าย และมีฟีเจอร์ครบถ้วนตามความต้องการ",
        "context": "กำลังพัฒนาแอพพลิเคชันสำหรับการวิเคราะห์และแสดงผลข้อมูล โดยต้องการให้ผู้ใช้สามารถอัพโหลดไฟล์ จัดการข้อมูล และดูผลการวิเคราะห์ได้",
        "explanation": """โครงสร้างแอพพลิเคชันประกอบด้วย:
1. ส่วนอัพโหลดและจัดการข้อมูล
2. ส่วนประมวลผลและวิเคราะห์
3. ส่วนแสดงผลและ visualization
4. ระบบจัดการ state และ cache""",
        "example_output": """# โครงสร้างโค้ด Streamlit
1. การตั้งค่าเริ่มต้น
   - Import libraries
   - Page config
   - Session state

2. ฟังก์ชันหลัก
   - Data processing
   - Analysis functions
   - Visualization functions

3. UI Components
   - Sidebar options
   - Main content
   - Interactive elements

4. การจัดการข้อมูล
   - File upload
   - Data validation
   - Caching

5. การแสดงผล
   - Charts/Graphs
   - Tables
   - Download options""",
        "tips": """1. ใช้ st.cache_data สำหรับฟังก์ชันที่ประมวลผลนาน
2. จัดการ state ด้วย session_state
3. แบ่ง code เป็นโมดูลที่จัดการง่าย
4. ใช้ st.spinner() แสดงสถานะการประมวลผล
5. สร้าง error handling ที่เหมาะสม"""
    },
    "ML App Developer": {
        "role": "คุณคือผู้เชี่ยวชาญด้าน Machine Learning ที่มีประสบการณ์ในการพัฒนาโมเดลและสร้างแอพพลิเคชัน ML",
        "action": "ออกแบบและพัฒนาแอพพลิเคชัน Machine Learning ที่สามารถทำนายผลลัพธ์ได้แม่นยำและใช้งานง่าย",
        "context": "กำลังพัฒนาแอพพลิเคชัน ML สำหรับการทำนายผลลัพธ์จากข้อมูลที่ผู้ใช้ป้อนเข้ามา โดยต้องการให้มีความแม่นยำและประสิทธิภาพสูง",
        "explanation": """ขั้นตอนการพัฒนาแอพพลิเคชัน ML:
1. การเตรียมข้อมูลและโมเดล
2. การสร้าง pipeline การประมวลผล
3. การพัฒนา UI สำหรับรับข้อมูล
4. การแสดงผลการทำนาย
5. การ monitor และปรับปรุงโมเดล""",
        "example_output": """# โครงสร้างแอพพลิเคชัน ML
1. Data Pipeline
   - Data preprocessing
   - Feature engineering
   - Model training

2. Model Management
   - Model loading
   - Prediction pipeline
   - Model monitoring

3. UI Components
   - Input forms
   - Model selection
   - Results display

4. Performance Metrics
   - Accuracy metrics
   - Confusion matrix
   - ROC curves

5. Deployment
   - Model serving
   - API endpoints
   - Monitoring dashboard""",
        "tips": """1. ใช้ pipeline ในการจัดการข้อมูลและโมเดล
2. เก็บ metrics เพื่อติดตามประสิทธิภาพ
3. ทำ cross-validation เพื่อประเมินโมเดล
4. ใช้ feature importance ในการอธิบายผล
5. สร้างระบบ monitoring เพื่อติดตาม model drift"""
    },
    "Data Dashboard Designer": {
        "role": "คุณคือนักวิเคราะห์ข้อมูลที่เชี่ยวชาญในการออกแบบ dashboard และการหา insights จากข้อมูล",
        "action": "ออกแบบและพัฒนา dashboard ที่สามารถแสดงข้อมูลสำคัญและ insights ได้อย่างมีประสิทธิภาพ",
        "context": "กำลังพัฒนา dashboard สำหรับวิเคราะห์และนำเสนอข้อมูลทางธุรกิจ โดยต้องการให้ผู้ใช้สามารถเห็นภาพรวมและเจาะลึกข้อมูลได้",
        "explanation": """องค์ประกอบของ Dashboard:
1. Overview metrics (KPIs)
2. Trend analysis
3. Comparative analysis
4. Detailed drill-down views
5. Interactive filters""",
        "example_output": """# โครงสร้าง Dashboard
1. Main KPIs
   - Revenue metrics
   - Growth indicators
   - Performance metrics

2. Trend Analysis
   - Time series charts
   - Growth patterns
   - Seasonality analysis

3. Comparative Views
   - Period comparisons
   - Category analysis
   - Geographic distribution

4. Detailed Analysis
   - Data tables
   - Drill-down capability
   - Custom filters

5. Insights Section
   - Key findings
   - Recommendations
   - Action items""",
        "tips": """1. เริ่มจากภาพรวมแล้วค่อยเจาะลึก
2. ใช้สีและการจัดวางที่เหมาะสม
3. สร้าง interactive elements
4. มี consistent design
5. ใส่ context และคำอธิบายที่จำเป็น"""
    }
}

# ตั้งค่าหน้าเพจ
st.set_page_config(page_title="RACE Prompt Generator", page_icon="🚀", layout="wide")

# แสดงรูปภาพ Cover และ Header
st.markdown("""
    <div style='background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        <h1 style='text-align: center; color: #0e1117;'>🚀 RACE Framework Prompt Generator</h1>
        <p style='text-align: center; color: #0e1117;'>สร้าง Prompt ระดับมืออาชีพด้วย AI จาก OpenRouter</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ การตั้งค่า")
    
    # เลือกโมเดล AI
    st.subheader("🤖 เลือกโมเดล AI")
    selected_model = st.selectbox(
        "เลือกโมเดลที่ต้องการใช้งาน",
        options=list(AI_MODELS.keys()),
        help="เลือกโมเดล AI ที่ต้องการใช้ในการปรับปรุง Prompt"
    )
    
    st.markdown("---")
    
    # การตั้งค่า API
    st.subheader("🔑 การตั้งค่า API")
    api_key = st.text_input(
        "OpenRouter API Key", 
        type="password", 
        help="รับ API Key ได้ที่: https://openrouter.ai/keys"
    )
    
    site_url = st.text_input(
        "เว็บไซต์ของคุณ (ไม่จำเป็น)", 
        placeholder="https://your-website.com"
    )
    
    site_name = st.text_input(
        "ชื่อเว็บไซต์ (ไม่จำเป็น)", 
        placeholder="My Awesome App"
    )
    
    st.markdown("---")
    
    # เพิ่มส่วนเลือกใช้ตัวอย่าง
    st.subheader("📝 เลือกใช้ตัวอย่าง")
    selected_templates = []
    for template_name in EXAMPLE_TEMPLATES.keys():
        if st.checkbox(f"ใช้ตัวอย่าง: {template_name}"):
            selected_templates.append(template_name)

# แสดงคำอธิบาย RACE Framework
with st.expander("ℹ️ วิธีการใช้งาน", expanded=True):
    st.markdown("""
    **RACE Framework Structure:**
    1. **Role** - บทบาทของ AI
    2. **Action** - สิ่งที่ต้องการให้ทำ
    3. **Context** - บริบทและเงื่อนไข
    4. **Explanation** - รายละเอียดเพิ่มเติม
    5. **Example Output** - ตัวอย่างผลลัพธ์
    6. **Tips** - เคล็ดลับพิเศษ
    """)

# สร้างฟอร์ม
form_data = {}
with st.form("race_form"):
    # ถ้ามีการเลือกตัวอย่าง ให้ใช้ข้อมูลจากตัวอย่างแรกที่เลือก
    template = None
    if selected_templates:
        template = EXAMPLE_TEMPLATES[selected_templates[0]]
    
    cols = st.columns(2)
    with cols[0]:
        form_data['role'] = st.text_area(
            "1. Role",
            value=template['role'] if template else "",
            placeholder="กรอกบทบาทของ AI",
            height=150
        )
        
        form_data['context'] = st.text_area(
            "3. Context",
            value=template['context'] if template else "",
            placeholder="กรอกบริบทและเงื่อนไข",
            height=150
        )
        
        form_data['example_output'] = st.text_area(
            "5. Example Output",
            value=template['example_output'] if template else "",
            placeholder="กรอกตัวอย่างผลลัพธ์",
            height=150
        )

    with cols[1]:
        form_data['action'] = st.text_area(
            "2. Action",
            value=template['action'] if template else "",
            placeholder="กรอกสิ่งที่ต้องการให้ทำ",
            height=150
        )
        
        form_data['explanation'] = st.text_area(
            "4. Explanation",
            value=template['explanation'] if template else "",
            placeholder="กรอกรายละเอียดเพิ่มเติม",
            height=150
        )
        
        form_data['tips'] = st.text_area(
            "6. Tips",
            value=template['tips'] if template else "",
            placeholder="กรอกเคล็ดลับพิเศษ",
            height=150
        )

    submitted = st.form_submit_button("✨ สร้างและปรับปรุง Prompt")

# การจัดการเมื่อกดปุ่ม submit
if submitted:
    if not api_key:
        st.error("กรุณากรอก OpenRouter API Key!")
        st.stop()
        
    if not all(form_data.values()):
        st.error("กรุณากรอกข้อมูลทุกช่อง!")
        st.stop()

    raw_prompt = f"""
### 1. Role
{form_data['role']}

### 2. Action
{form_data['action']}

### 3. Context
{form_data['context']}

### 4. Explanation
{form_data['explanation']}

### 5. Example Output
{form_data['example_output']}

### 6. Tips
{form_data['tips']}
    """
    
    st.subheader("Prompt ที่ปรับปรุงแล้ว")
    result = call_openrouter_api(raw_prompt, api_key, selected_model, site_url, site_name)
    
    if result:
        st.markdown(f"```{result}```")
        
        # เพิ่มปุ่มดาวน์โหลดและคัดลอก
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "💾 ดาวน์โหลด Prompt",
                result,
                file_name="generated_prompt.txt",
                mime="text/plain"
            )
        with col2:
            st.button(
                "📋 คัดลอกไปยังคลิปบอร์ด",
                help="คลิกเพื่อคัดลอก Prompt ไปยังคลิปบอร์ด",
                on_click=lambda: st.write('<script>navigator.clipboard.writeText(`' + result + '`);</script>', unsafe_allow_html=True)
            )
