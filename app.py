import streamlit as st, requests, json, PyPDF2
API = "https://api.together.xyz/v1/chat/completions"
KEY = "ВСТАВЬТЕ_СЮДА_ВАШ_API_КЛЮЧ"

st.title("Юридический ИИ-агент (2 юриста)")
uploaded = st.file_uploader("PDF-договор", type="pdf")
question = st.text_area("Ваш вопрос", placeholder="Какие риски вы видите?")
if st.button("Спросить"):
    if not uploaded:
        st.warning("Сначала загрузите PDF")
        st.stop()
    # читаем текст
    pdf_text = ""
    with uploaded as f:
        reader = PyPDF2.PdfReader(f)
        for p in reader.pages:
            pdf_text += p.extract_text()
    prompt = f"Договор:\n{pdf_text[:12_000]}\n\nВопрос: {question}\nКраткий ответ:"
    headers = {"Authorization": f"Bearer {KEY}"}
    data = {
        "model": "meta-llama/Llama-3.1-8B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
        "temperature": 0.2
    }
    r = requests.post(API, headers=headers, json=data, timeout=60).json()
    st.write(r["choices"][0]["message"]["content"])
