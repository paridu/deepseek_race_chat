import streamlit as st
import requests

# กำหนดฟังก์ชันสำหรับการเชื่อมต่อ API ของ DeepSeek
def call_deepseek_api(prompt, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": f"ปรับปรุงประโยคนี้ให้มีความสมบูรณ์และเป็นธรรมชาติมากขึ้น: {prompt}"}]
    }

    try:
        with st.spinner("กำลังปรับปรุงคำสั่งด้วย AI..."):
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"เกิดข้อผิดพลาดขณะเชื่อมต่อ API: {e}")
        return None

# ตั้งค่าหน้า Streamlit
st.title("📝 RACE Framework Form Generator with AI Enhancement")

# เพิ่ม text box สำหรับกรอก API Key
api_key_input = st.text_input("กรอก API Key ของ DeepSeek", type="password")

# สร้างฟอร์มสำหรับกรอกข้อมูล
with st.form("race_form"):
    st.subheader("1. Role")
    role = st.text_area("ระบุบทบาทของ AI (เช่น 'คุณคือผู้เชี่ยวชาญด้าน...')", 
                        placeholder="เช่น 'คุณคือผู้เชี่ยวชาญด้าน Python และ Streamlit'")

    st.subheader("2. Action")
    action = st.text_area("ระบุสิ่งที่ต้องการให้ AI ทำ", 
                          placeholder="เช่น 'สร้างแอป Streamlit ที่...'")

    st.subheader("3. Context")
    context = st.text_area("ระบุบริบท (ทักษะ, ทรัพยากร, ข้อจำกัด)", 
                           placeholder="เช่น 'ผู้เรียนมีทักษะ Python พื้นฐาน...'")

    st.subheader("4. Explanation")
    explanation = st.text_area("อธิบายรายละเอียดเพิ่มเติม", 
                               placeholder="เช่น 'ใช้ Session State จัดการประวัติแชท...'")

    st.subheader("5. Example Output")
    example_output = st.text_area("ระบุผลลัพธ์ที่คาดหวัง", 
                                  placeholder="เช่น 'ต้องการโค้ด Python แบบสมบูรณ์ใน 1 ไฟล์...'")

    st.subheader("6. Tips")
    tips = st.text_area("ใส่เคล็ดลับเพิ่มเติม", 
                        placeholder="เช่น 'ถ้าอยากได้โค้ดเร็วๆ → ใส่ `เขียนโค้ดให้เสร็จใน 1 ไฟล์`'")

    submitted = st.form_submit_button("สร้างและปรับปรุง Prompt")

if submitted:
    if not all([role, action, context, explanation, example_output, api_key_input]):
        st.error("กรุณากรอกข้อมูลทุกส่วนและ API Key!")
    else:
        raw_prompt = f"""
### **1. Role**  
{role}

### **2. Action**  
{action}

### **3. Context**  
{context}

### **4. Explanation**  
{explanation}

### **5. Example Output**  
{example_output}

### **6. Tips**  
✅ **เคล็ดลับ**:  
{tips}
"""
        enhanced_prompt = call_deepseek_api(raw_prompt, api_key_input)

        if enhanced_prompt:
            st.success("Prompt ของคุณพร้อมแล้ว!")
            st.code(enhanced_prompt, language="plaintext")
            st.download_button(
                label="ดาวน์โหลด Prompt",
                data=enhanced_prompt,
                file_name="enhanced_race_prompt.txt",
                mime="text/plain"
            )
