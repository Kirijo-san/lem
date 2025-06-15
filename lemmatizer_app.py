import streamlit as st
from pymorphy3 import MorphAnalyzer
import re

st.title("📝 Лемматизатор русского языка")

# Инициализация анализатора
try:
    morph = MorphAnalyzer()
except Exception as e:
    st.error(f"Ошибка инициализации: {str(e)}")
    st.stop()

# Функция проверки на русский текст
def is_russian(text):
    """Проверяет, содержит ли текст только русские буквы и разрешенные символы"""
    russian_letters = re.compile(r'^[а-яА-ЯёЁ\s\d\.,!?;:-]+$')
    return bool(russian_letters.fullmatch(text))

text = st.text_area("Введите текст (на русском языке!):", 
                   "Гарри никогда еще так не наказывали, как за историю с бразильским удавом")

if st.button("Лемматизировать"):
    # Проверка на русский язык
    if not is_russian(text):
        st.error("Ошибка: допускается только русский текст! Удалите латинские буквы и специальные символы.")
        st.stop()  # Останавливаем выполнение
    
    # Если текст прошел проверку
    words = text.split()
    lemmas = []
    
    for word in re.findall(r'[а-яА-ЯёЁ]+', text):  # Игнорируем числа и пунктуацию
        try:
            parsed = morph.parse(word)
            if parsed:
                lemmas.append(parsed[0].normal_form)
        except:
            lemmas.append(word)
    
    st.subheader("Результат:")
    st.write(" ".join(lemmas))
    st.success(f"Успешно обработано {len(lemmas)} слов")
