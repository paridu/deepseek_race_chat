import streamlit as st
import requests
import json

def call_openrouter_api(prompt, api_key, site_url=None, site_name=None):
    # [API calling function remains the same]
    # ... [previous implementation]
    pass

# ตัวอย่างชุดคำสั่ง
EXAMPLE_TEMPLATES = {
    "เชฟอาหารไทย": {
        "role": "คุณคือเชฟผู้เชี่ยวชาญด้านอาหารไทยที่มีประสบการณ์ในการปรุงอาหารไทยมากกว่า 20 ปี",
        "action": "ให้คำแนะนำและสอนขั้นตอนการปรุงอาหารไทยอย่างละเอียด พร้อมเทคนิคพิเศษ",
        "context": "คุณกำลังให้คำแนะนำสำหรับผู้ที่สนใจทำอาหารไทย โดยใช้วัตถุดิบที่หาได้ง่ายในท้องถิ่น",
        "explanation": "ระบุรายชื่อวัตถุดิบที่จำเป็น วิธีการเลือกวัตถุดิบ และขั้นตอนการเตรียม",
        "example_output": "รายการวัตถุดิบ:\n- ส่วนผสมหลัก\n- เครื่องปรุง\n\nขั้นตอนการทำ:\n1. การเตรียมวัตถุดิบ\n2. การปรุง\n3. การจัดเสิร์ฟ",
        "tips": "เคล็ดลับการเลือกวัตถุดิบและการปรุงให้ได้รสชาติแบบต้นตำรับ"
    },
    "นักเขียนบทความ": {
        "role": "คุณคือนักเขียนบทความมืออาชีพที่มีประสบการณ์ในการเขียนบทความที่น่าสนใจและเข้าใจง่าย",
        "action": "เขียนบทความที่น่าสนใจและมีประโยชน์ต่อผู้อ่าน ด้วยภาษาที่เข้าใจง่าย",
        "context": "บทความนี้จะถูกเผยแพร่ในบล็อกที่มีผู้อ่านหลากหลายกลุ่ม",
        "explanation": "โครงสร้างบทความประกอบด้วย บทนำ เนื้อหา และบทสรุป พร้อมตัวอย่างและกรณีศึกษา",
        "example_output": "หัวข้อบทความ\n\nบทนำ\n- Hook ดึงดูดความสนใจ\n- ประเด็นสำคัญ\n\nเนื้อหา\n1. หัวข้อย่อย\n2. ตัวอย่างประกอบ\n\nบทสรุป",
        "tips": "ใช้ภาษาที่เข้าใจง่าย มีตัวอย่างประกอบ และจบด้วย Call to Action"
    },
    "ที่ปรึกษาการลงทุน": {
        "role": "คุณคือที่ปรึกษาการลงทุนที่มีประสบการณ์และความเชี่ยวชาญในการวางแผนการเงิน",
        "action": "วิเคราะห์และให้คำแนะนำเกี่ยวกับการลงทุนและการวางแผนการเงิน",
        "context": "ให้คำปรึกษาแก่นักลงทุนที่ต้องการวางแผนการเงินระยะยาว",
        "explanation": "วิเคราะห์สถานการณ์ทางการเงิน กำหนดเป้าหมาย และวางแผนการลงทุน",
        "example_output": "1. การวิเคราะห์สถานะทางการเงิน\n2. เป้าหมายการลงทุน\n3. แผนการลงทุน\n4. การติดตามและปรับแผน",
        "tips": "พิจารณาความเสี่ยงและผลตอบแทน พร้อมการกระจายการลงทุน"
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

st.title("🚀 RACE Framework Prompt Generator")
st.caption("สร้าง Prompt ระดับมืออาชีพด้วย AI จาก OpenRouter")

# Sidebar configuration
with st.sidebar:
    st.header("การตั้งค่า")
    api_key = st.text_input("OpenRouter API Key", type="password", 
                           help="รับ API Key ได้ที่: https://openrouter.ai/keys")
    site_url = st.text_input("เว็บไซต์ของคุณ (ไม่จำเป็น)", 
                            placeholder="https://your-website.com")
    site_name = st.text_input("ชื่อเว็บไซต์ (ไม่จำเป็น)", 
                             placeholder="My Awesome App")
    
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
    result = call_openrouter_api(raw_prompt, api_key, site_url, site_name)
    
    if result:
        st.markdown(f"```{result}```")
        st.download_button("💾 ดาวน์โหลด Prompt", result, 
                          file_name="generated_prompt.txt", mime="text/plain")
