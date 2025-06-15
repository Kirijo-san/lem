import streamlit as st
from pymorphy3 import MorphAnalyzer
import re

st.title("🌸 Лемматизатор русского языка")

try:
    morph = MorphAnalyzer()
except Exception as e:
    st.error(f"Ошибка инициализации: {str(e)}")
    st.stop()

def is_russian(text):
    """Проверяет, содержит ли текст только русские буквы и разрешенные символы"""
    russian_letters = re.compile(r'^[а-яА-ЯёЁ\s\d\.,!?;:-]+$')  # Добавлена закрывающая скобка
    return bool(russian_letters.fullmatch(text))

text = st.text_area("Введите текст:",
                   "Гарри никогда еще так не наказывали, как за историю с бразильским удавом")

if st.button("Лемматизировать"):
    if not is_russian(text):
        st.error("❗ОБНАРУЖЕНА ЛАТИНИЦА И/ИЛИ СПЕЦСИМВОЛЫ. НЕМЕДЛЕННО УТИЛИЗИРОВАТЬ❗")
        st.stop()
    
    words = text.split()
    lemmas = []
    
    for word in re.findall(r'[а-яА-ЯёЁ]+', text):  # Этот блок ДОЛЖЕН быть внутри if
        try:
            parsed = morph.parse(word)
            if parsed:
                lemmas.append(parsed[0].normal_form)
        except:
            lemmas.append(word)
    
    st.subheader("Результат:")
    st.write(" ".join(lemmas))
    st.metric("🌸Слов обработано", len(words))
