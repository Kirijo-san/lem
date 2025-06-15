import streamlit as st
from pymorphy3 import MorphAnalyzer  # Используем pymorphy3 вместо pymorphy2

st.title("📝 Лемматизатор русского текста")

# Инициализация анализатора
try:
    morph = MorphAnalyzer()
    st.session_state.ready = True
except Exception as e:
    st.error(f"Ошибка инициализации: {str(e)}")
    st.session_state.ready = False

# Интерфейс
text = st.text_area("Введите текст для лемматизации:", 
                   "Красивые кошки прыгали через высокие заборы")

if st.button("Лемматизировать") and st.session_state.get('ready', False):
    words = text.split()
    lemmas = []
    
    for word in words:
        try:
            parsed = morph.parse(word)
            if parsed:
                lemmas.append(parsed[0].normal_form)
            else:
                lemmas.append(word)
        except:
            lemmas.append(word)
    
    st.subheader("Результат:")
    st.write(" ".join(lemmas))
    st.metric("Слов обработано", len(words))