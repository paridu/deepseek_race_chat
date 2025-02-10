import streamlit as st
import requests
import json

def call_openrouter_api(prompt, api_key, site_url=None, site_name=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": site_url or "",  # ระบุ URL เว็บไซต์ของคุณ (ถ้ามี)
        "X-Title": site_name or ""        # ระบุชื่อเว็บไซต์ของคุณ (ถ้ามี)
    }
    
    data = {
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
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
            response.raise_for_status()  # ตรวจสอบสถานะการตอบกลับจาก API
            
            result = response.json()  # แปลงข้อมูลที่ได้จาก API
            return result['choices'][0]['message']['content']
            
    except requests.exceptions.HTTPError as e:
        # การจัดการข้อผิดพลาดจาก HTTP Request
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


# ส่วนติดต่อผู้ใช้ด้วย Streamlit
st.set_page_config(page_title="RACE Prompt Generator", page_icon="🚀", layout="wide")

with st.sidebar:
    st.header("การตั้งค่า")
    api_key = st.text_input("OpenRouter API Key", type="password", help="รับ API Key ได้ที่: https://openrouter.ai/keys")
    site_url = st.text_input("เว็บไซต์ของคุณ (ไม่จำเป็น)", placeholder="https://your-website.com")
    site_name = st.text_input("ชื่อเว็บไซต์ (ไม่จำเป็น)", placeholder="My Awesome App")
    
    st.markdown("---")
    st.markdown("""
    **📚 คู่มือการใช้งาน:**
    1. กรอกข้อมูลแต่ละส่วนตาม RACE Framework
    2. ใส่ OpenRouter API Key
    3. กดปุ่มสร้าง Prompt
    4. ดาวน์โหลดหรือคัดลอกผลลัพธ์
    """)

st.title("🚀 RACE Framework Prompt Generator")
st.caption("สร้าง Prompt ระดับมืออาชีพด้วย AI จาก OpenRouter")

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

form_data = {}
with st.form("race_form"):
    cols = st.columns(2)
    with cols[0]:
        form_data['role'] = st.text_area(
            "1. Role", 
            placeholder="""เช่น 'AI จะทำหน้าที่เป็นผู้ช่วยในการสร้างและจัดการ Streamlit app เพื่อบริหารการขออนุมัติจากผู้จัดการในองค์กร โดยแอปจะต้องช่วยให้การขออนุมัติเป็นระบบระเบียบและง่ายขึ้น'""",
            height=150
        )
        
        form_data['context'] = st.text_area(
    "3. Context", 
    placeholder="""เช่น 'แอปนี้ถูกสร้างขึ้นสำหรับองค์กรที่มีการขออนุมัติทรัพยากรต่างๆ จากผู้จัดการ
    แอปต้องสามารถจัดการคำขออนุมัติที่มีรายละเอียดหลากหลาย เช่น งบประมาณ, เวลา, และทรัพยากรที่ใช้
    การอนุมัติและการปฏิเสธจะถูกบันทึกและสามารถดูประวัติได้ ระบบต้องสามารถเชื่อมต่อกับฐานข้อมูลขององค์กรเพื่อดึงข้อมูลโปรเจคและการอนุมัติที่ผ่านมา'""",
    height=150
)

        
        form_data['example_output'] = st.text_area(
            "5. Example Output", 
             placeholder="""เช่น'ต้องการโค้ด Python แบบสมบูรณ์ใน 1 ไฟล์ พร้อมออกแบบฐานข้อมูล Mysql ตัวอย่าง พร้อมสร้างความสัมพันธ์ของตารางข้อมูล และแสดงโครงสร้างไฟล์ทุกครั้งว่ามีไฟล์อะไรบ้าง..'""",
            height=150
        )

    with cols[1]:
        form_data['action'] = st.text_area(
            "2. Action", 
            placeholder="""เช่น 'สร้างแอป Streamlit ที่ให้พนักงานสามารถยื่นคำขออนุมัติสำหรับโปรเจคหรือการใช้ทรัพยากรต่างๆ
ระบบจะมีการตรวจสอบข้อมูลที่จำเป็น เช่น ข้อมูลโปรเจค, งบประมาณที่ขออนุมัติ, และวันที่กำหนด
ผู้จัดการจะได้รับการแจ้งเตือนเกี่ยวกับคำขออนุมัติและสามารถอนุมัติหรือปฏิเสธได้ในระบบ'""",
            height=150
        )
        
        form_data['explanation'] = st.text_area(
            "4. Explanation", 
           placeholder="""เช่น 'การสร้างแอปจะใช้ฟังก์ชันจาก Streamlit สำหรับการแสดงผลข้อมูลและการสร้างแบบฟอร์มสำหรับการขออนุมัติ
ระบบจะใช้ st.selectbox สำหรับให้ผู้ใช้เลือกโปรเจคที่ต้องการขออนุมัติ, st.text_area สำหรับกรอกรายละเอียดคำขอ, และ st.button สำหรับส่งคำขออนุมัติ
จะมีระบบแจ้งเตือน (Notification) ที่ส่งผ่านอีเมลหรือภายในแอปเมื่อผู้จัดการได้รับคำขอ
จะมีการบันทึกข้อมูลการอนุมัติในฐานข้อมูล เช่น MySQL'""",
            height=150
        )
        
        form_data['tips'] = st.text_area(
            "6. Tips", 
            placeholder="เช่น 'ถ้าอยากได้โค้ดเร็ว → ใส่ `เขียนโค้ดให้เสร็จใน 1 ไฟล์`พร้อมทั้งปรับแต่ง UX UI ให้เป็นมืออาชีพ '",
            height=150
        )

    submitted = st.form_submit_button("✨ สร้างและปรับปรุง Prompt")

if submitted:
    if not api_key:
        st.error("กรุณากรอก OpenRouter API Key!")
        st.stop()
        
    if not all(form_data.values()):
        st.error("กรุณากรอกข้อมูลทุกช่อง! ข้อมูลที่ขาดหายไปจะถูกแสดงในฟอร์ม")
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
        st.download_button("💾 ดาวน์โหลด Prompt", result, file_name="generated_prompt.txt", mime="text/plain")
