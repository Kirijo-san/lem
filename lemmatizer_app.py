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
    russian_letters = re.compile(r'^[а-яА-ЯёЁ\s\d\.,!?;:-]+$')
    return bool(russian_letters.fullmatch(text))

def is_real_word(word):
    """Проверяет, является ли слово существующим в русском языке"""
    parsed = morph.parse(word)
    if not parsed:
        return False
    # Если хотя бы один вариант разбора не содержит тега UNKN (неизвестное слово)
    return any('UNKN' not in p.tag for p in parsed)

text = st.text_area("Введите текст:",
                   "Гарри никогда еще так не наказывали, как за историю с бразильским удавом")

if st.button("Лемматизировать"):
    if not is_russian(text):
        st.error("❗ОБНАРУЖЕНА ЛАТИНИЦА И/ИЛИ СПЕЦСИМВОЛЫ. НЕМЕДЛЕННО УТИЛИЗИРОВАТЬ❗")
        st.stop()
    
    words = text.split()
    lemmas = []
    unknown_words = []
    
    for word in re.findall(r'[а-яА-ЯёЁ]+', text):
        try:
            parsed = morph.parse(word)
            if parsed:
                if is_real_word(word):
                    lemmas.append(parsed[0].normal_form)
                else:
                    lemmas.append(f"[{word}]")  # Помечаем несуществующие слова
                    unknown_words.append(word)
        except:
            lemmas.append(word)
    
    st.subheader("Результат:")
    st.write(" ".join(lemmas))
    
    if unknown_words:
        st.warning(f"🌸 Обнаружены подозрительные слова: {', '.join(unknown_words)}")
    
    st.metric("🌸 Слов обработано", len(words))
