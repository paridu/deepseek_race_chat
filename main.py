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

def call_openrouter_api(prompt, api_key, model_name, framework_type, site_url=None, site_name=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": site_url or "",
        "X-Title": site_name or ""
    }
    
    framework_instruction = {
        "RACE": "ปรับปรุงโครงสร้างและภาษาของ Prompt นี้ให้เป็นมืออาชีพมากขึ้น โดยคงโครงสร้าง RACE Framework ดั้งเดิม",
        "BUILD": "ปรับปรุงและพัฒนา Web App Specification นี้ให้เป็นมืออาชีพและละเอียดมากขึ้น โดยคงโครงสร้าง BUILD Framework ดั้งเดิม พร้อมเสนอแนะเทคนิค UI/UX และ Code Structure ที่เหมาะสม"
    }
    
    data = {
        "model": AI_MODELS[model_name],
        "messages": [{
            "role": "user", 
            "content": f"{framework_instruction[framework_type]}:\n\n{prompt}"
        }],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        with st.spinner(f"🔮 AI กำลังปรับปรุง {framework_type} Specification ของคุณ..."):
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

# ตัวอย่าง RACE Templates
RACE_TEMPLATES = {
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
2. ฟังก์ชันหลัก
3. UI Components
4. การจัดการข้อมูล
5. การแสดงผล""",
        "tips": """1. ใช้ st.cache_data สำหรับฟังก์ชันที่ประมวลผลนาน
2. จัดการ state ด้วย session_state
3. แบ่ง code เป็นโมดูลที่จัดการง่าย"""
    }
}

# ตัวอย่าง BUILD Templates สำหรับ Web App Development
BUILD_TEMPLATES = {
    "E-commerce Platform": {
        "background": "ต้องการพัฒนาแพลตฟอร์ม E-commerce สำหรับร้านค้าออนไลน์ขนาดกลาง ที่ต้องการขายสินค้าหลากหลายประเภทและจัดการคำสั่งซื้ออย่างมีประสิทธิภาพ",
        "user": "เจ้าของร้านค้า (Admin), พนักงาน (Staff), และลูกค้า (Customer) โดยลูกค้าส่วนใหญ่เป็นคนรุ่นใหม่ที่คุ้นเคยกับเทคโนโลยี แต่ต้องการความสะดวกและรวดเร็ว",
        "interface": "UI/UX ที่ทันสมัย responsive design รองรับทั้ง desktop และ mobile ใช้สีโทนเขียว-ขาว เน้นความเรียบง่ายแต่สวยงาม มี search bar เด่นชั่ว และ navigation ที่ชัดเจน",
        "logic": """ฟีเจอร์หลัก:
- ระบบจัดการสินค้า (CRUD)
- ระบบตะกร้าสินค้าและ checkout
- ระบบชำระเงินหลายช่องทาง
- ระบบจัดการคำสั่งซื้อ
- ระบบรีวิวและ rating
- ระบบแจ้งเตือนสต็อก
- Dashboard สำหรับ admin""",
        "development": """Tech Stack:
Frontend: React.js + Tailwind CSS
Backend: Node.js + Express.js
Database: MongoDB
Payment: Stripe API
Hosting: Vercel (Frontend) + Railway (Backend)
Additional: JWT Authentication, Cloudinary (Images)"""
    },
    "Inventory Management System": {
        "background": "สร้างระบบจัดการสินค้าคงคลังสำหรับโรงงานผลิตขนาดกลาง ที่ต้องการติดตามวัตถุดิบ สินค้าสำเร็จรูป และการเคลื่อนไหวของสต็อกแบบ real-time",
        "user": "ผู้จัดการคลังสินค้า พนักงานคลัง และ supervisor ที่มีความรู้พื้นฐานด้านคอมพิวเตอร์ปานกลาง ต้องการระบบที่ใช้งานง่ายและแสดงข้อมูลได้ชัดเจน",
        "interface": "Dashboard แบบ clean modern design ใช้สีน้ำเงิน-เทา มี data visualization ด้วย charts และ graphs รองรับการใช้งานผ่าน tablet ในโรงงาน",
        "logic": """ฟีเจอร์หลัก:
- ระบบบันทึกสินค้าเข้า-ออก
- ระบบ barcode/QR code scanning
- การติดตามสินค้าแบบ real-time
- แจ้งเตือนสต็อกต่ำ
- รายงานการเคลื่อนไหวสต็อก
- ระบบ forecast demand
- Export รายงานเป็น Excel/PDF""",
        "development": """Tech Stack:
Frontend: Vue.js + Vuetify
Backend: Python + FastAPI
Database: PostgreSQL
Real-time: WebSocket
Hosting: Digital Ocean
Additional: Redis (Caching), Celery (Background Tasks)"""
    },
    "Learning Management System": {
        "background": "พัฒนาแพลตฟอร์มการเรียนรู้ออนไลน์สำหรับโรงเรียนขนาดกลาง ที่ต้องการจัดการคอร์สเรียน ติดตามผลการเรียน และสื่อสารระหว่างครูและนักเรียน",
        "user": "ครู (สร้างเนื้อหา), นักเรียน (เรียนและทำแบบทดสอบ), ผู้ปกครอง (ติดตามผล), และ admin (จัดการระบบ) โดยส่วนใหญ่มีความรู้ด้านเทคโนโลยีปานกลาง",
        "interface": "Design ที่เป็นมิตรและอบอุ่น ใช้สีฟ้าอ่อน-ส้ม มี responsive design ที่ใช้งานบน smartphone ได้ดี พร้อม dark mode สำหรับการเรียนตอนกลางคืน",
        "logic": """ฟีเจอร์หลัก:
- ระบบจัดการคอร์สและบทเรียน
- ระบบอัพโหลด video และเอกสาร
- ระบบสร้างแบบทดสอบ
- ระบบ chat และ forum
- ระบบ calendar และ assignment
- ระบบ grade book
- ระบบ notification""",
        "development": """Tech Stack:
Frontend: Next.js + Material-UI
Backend: Laravel + MySQL
Storage: AWS S3 (Videos/Files)
Real-time: Pusher
Hosting: Vercel + DigitalOcean
Additional: FFmpeg (Video Processing), Socket.io"""
    },
    "Task Management App": {
        "background": "สร้างแอปจัดการงานสำหรับทีมงานขนาดเล็กถึงกลาง ที่ต้องการติดตาม project timeline, assign tasks, และ collaborate แบบ real-time",
        "user": "Project Manager, Team Lead, และ Developer/Designer ที่ต้องการเครื่องมือที่ใช้งานง่ายกว่า Jira แต่มีฟีเจอร์ครบถ้วนกว่า Trello",
        "interface": "Modern minimalist design คล้าย Notion ใช้สี neutral tones (เทา-ขาว-เขียวอ่อน) มี drag & drop interface และ keyboard shortcuts เพื่อความรวดเร็ว",
        "logic": """ฟีเจอร์หลัก:
- ระบบ Kanban board
- การสร้างและ assign tasks
- ระบบ comment และ mention
- Time tracking
- File attachment
- Calendar integration
- Progress reporting
- Team collaboration tools""",
        "development": """Tech Stack:
Frontend: React.js + Ant Design
Backend: Node.js + GraphQL
Database: MongoDB
Real-time: GraphQL Subscriptions
Hosting: Netlify + Heroku
Additional: Socket.io, JWT, Cloudinary"""
    }
}

# ตั้งค่าหน้าเพจ
st.set_page_config(page_title="Multi-Framework Prompt Generator", page_icon="🚀", layout="wide")

# แสดงรูปภาพ Cover และ Header
st.markdown("""
    <div style='background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        <h1 style='text-align: center; color: #0e1117;'>🚀 Multi-Framework Prompt Generator</h1>
        <p style='text-align: center; color: #0e1117;'>สร้าง Prompt ระดับมืออาชีพด้วย RACE & BUILD Framework</p>
    </div>
    """, unsafe_allow_html=True)

# Tabs สำหรับเลือก Framework
tab1, tab2 = st.tabs(["📝 RACE Framework", "🏗️ BUILD Framework"])

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

# RACE Framework Tab
with tab1:
    with st.expander("ℹ️ เกี่ยวกับ RACE Framework", expanded=False):
        st.markdown("""
        **RACE Framework Structure:**
        1. **Role** - บทบาทของ AI
        2. **Action** - สิ่งที่ต้องการให้ทำ
        3. **Context** - บริบทและเงื่อนไข
        4. **Explanation** - รายละเอียดเพิ่มเติม
        5. **Example Output** - ตัวอย่างผลลัพธ์
        6. **Tips** - เคล็ดลับพิเศษ
        """)
    
    # เลือกใช้ตัวอย่าง RACE
    st.subheader("📝 เลือกใช้ตัวอย่าง RACE")
    selected_race_template = st.selectbox(
        "เลือกตัวอย่าง Template",
        options=["ไม่ใช้ตัวอย่าง"] + list(RACE_TEMPLATES.keys()),
        key="race_template"
    )
    
    # สร้างฟอร์ม RACE
    race_data = {}
    with st.form("race_form"):
        template = None
        if selected_race_template != "ไม่ใช้ตัวอย่าง":
            template = RACE_TEMPLATES[selected_race_template]
        
        cols = st.columns(2)
        with cols[0]:
            race_data['role'] = st.text_area(
                "1. Role",
                value=template['role'] if template else "",
                placeholder="กรอกบทบาทของ AI",
                height=150,
                key="race_role"
            )
            
            race_data['context'] = st.text_area(
                "3. Context",
                value=template['context'] if template else "",
                placeholder="กรอกบริบทและเงื่อนไข",
                height=150,
                key="race_context"
            )
            
            race_data['example_output'] = st.text_area(
                "5. Example Output",
                value=template['example_output'] if template else "",
                placeholder="กรอกตัวอย่างผลลัพธ์",
                height=150,
                key="race_example"
            )

        with cols[1]:
            race_data['action'] = st.text_area(
                "2. Action",
                value=template['action'] if template else "",
                placeholder="กรอกสิ่งที่ต้องการให้ทำ",
                height=150,
                key="race_action"
            )
            
            race_data['explanation'] = st.text_area(
                "4. Explanation",
                value=template['explanation'] if template else "",
                placeholder="กรอกรายละเอียดเพิ่มเติม",
                height=150,
                key="race_explanation"
            )
            
            race_data['tips'] = st.text_area(
                "6. Tips",
                value=template['tips'] if template else "",
                placeholder="กรอกเคล็ดลับพิเศษ",
                height=150,
                key="race_tips"
            )

        race_submitted = st.form_submit_button("✨ สร้างและปรับปรุง RACE Prompt")

    # การจัดการเมื่อกดปุ่ม submit RACE
    if race_submitted:
        if not api_key:
            st.error("กรุณากรอก OpenRouter API Key!")
        elif not all(race_data.values()):
            st.error("กรุณากรอกข้อมูลทุกช่อง!")
        else:
            raw_prompt = f"""
### 1. Role
{race_data['role']}

### 2. Action
{race_data['action']}

### 3. Context
{race_data['context']}

### 4. Explanation
{race_data['explanation']}

### 5. Example Output
{race_data['example_output']}

### 6. Tips
{race_data['tips']}
            """
            
            st.subheader("🎯 RACE Prompt ที่ปรับปรุงแล้ว")
            result = call_openrouter_api(raw_prompt, api_key, selected_model, "RACE", site_url, site_name)
            
            if result:
                st.markdown(f"```{result}```")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "💾 ดาวน์โหลด RACE Prompt",
                        result,
                        file_name="race_prompt.txt",
                        mime="text/plain"
                    )

# BUILD Framework Tab
with tab2:
    with st.expander("ℹ️ เกี่ยวกับ BUILD Framework", expanded=True):
        st.markdown("""
        **BUILD Framework สำหรับ Web App Development:**
        - 🎯 **B = Background** - บริบทและวัตถุประสงค์ของแอป
        - 👥 **U = User** - กลุ่มผู้ใช้งานเป้าหมายและพฤติกรรม
        - 🎨 **I = Interface** - UI/UX Design และ User Experience
        - 🧠 **L = Logic** - ฟีเจอร์หลัก Business Logic และ Workflow
        - 🛠️ **D = Development Stack** - เทคโนโลยีและโครงสร้างการพัฒนา
        
        **เหมาะสำหรับ:** การวางแผนและพัฒนา Web Application ทุกประเภท
        """)
    
    # เลือกใช้ตัวอย่าง BUILD
    st.subheader("🏗️ เลือกใช้ตัวอย่าง BUILD")
    selected_build_template = st.selectbox(
        "เลือกตัวอย่าง Web App Template",
        options=["ไม่ใช้ตัวอย่าง"] + list(BUILD_TEMPLATES.keys()),
        key="build_template"
    )
    
    # สร้างฟอร์ม BUILD
    build_data = {}
    with st.form("build_form"):
        template = None
        if selected_build_template != "ไม่ใช้ตัวอย่าง":
            template = BUILD_TEMPLATES[selected_build_template]
        
        # Background
        build_data['background'] = st.text_area(
            "🎯 Background - บริบทและวัตถุประสงค์",
            value=template['background'] if template else "",
            placeholder="อธิบายบริบท วัตถุประสงค์ และเหตุผลในการสร้างแอปนี้",
            height=120,
            key="build_background"
        )
        
        # User
        build_data['user'] = st.text_area(
            "👥 User - กลุ่มผู้ใช้งานเป้าหมาย",
            value=template['user'] if template else "",
            placeholder="อธิบายกลุ่มผู้ใช้งาน ความต้องการ และระดับความรู้ด้านเทคโนโลยี",
            height=120,
            key="build_user"
        )
        
        # Interface
        build_data['interface'] = st.text_area(
            "🎨 Interface - UI/UX Design",
            value=template['interface'] if template else "",
            placeholder="อธิบาย UI/UX ที่ต้องการ สี theme, responsive design, และ user experience",
            height=120,
            key="build_interface"
        )
        
        # Logic
        build_data['logic'] = st.text_area(
            "🧠 Logic - ฟีเจอร์และ Business Logic",
            value=template['logic'] if template else "",
            placeholder="รายละเอียดฟีเจอร์หลัก workflow และ business rules",
            height=150,
            key="build_logic"
        )
        
        # Development
        build_data['development'] = st.text_area(
            "🛠️ Development Stack - เทคโนโลยี",
            value=template['development'] if template else "",
            placeholder="ระบุ tech stack, database, hosting, และเครื่องมือที่ต้องการใช้",
            height=150,
            key="build_development"
        )

        build_submitted = st.form_submit_button("🚀 สร้างและปรับปรุง BUILD Specification")

    # การจัดการเมื่อกดปุ่ม submit BUILD
    if build_submitted:
        if not api_key:
            st.error("กรุณากรอก OpenRouter API Key!")
        elif not all(build_data.values()):
            st.error("กรุณากรอกข้อมูลทุกช่อง!")
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
            result = call_openrouter_api(raw_spec, api_key, selected_model, "BUILD", site_url, site_name)
            
            if result:
                st.markdown(result)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "💾 ดาวน์โหลด BUILD Spec",
                        result,
                        file_name="build_specification.md",
                        mime="text/markdown"
                    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <strong>เคล็ดลับ:</strong> ใช้ RACE สำหรับ General AI Prompts และ BUILD สำหรับ Web App Development</p>
    <p>Powered by OpenRouter AI Models</p>
</div>
""", unsafe_allow_html=True)
