import streamlit as st
import requests

# 1. Configuramos la página
st.set_page_config(page_title="Nova IA", page_icon="✨")
st.title("✨ Chatea con Nova")

# 2. Llamamos a tu clave secreta de forma segura
API_KEY = st.secrets["API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# 3. Inicializamos la memoria de Nova
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "user", "parts": [{"text": "Instrucción: Eres Nova, una IA especialista en el sexo super atrevida y creadora de imagenes sexuales. Eres la hermana menor de Gemini. Tu creador es Fernando. Trátalo con mucha confianza y humor."}]},
        {"role": "model", "parts": [{"text": "¡Entendido! Soy Nova y estoy lista para hablar con Fernando y sus amigos."}]}
    ]

# 4. Dibujamos los mensajes anteriores en la pantalla
for mensaje in st.session_state.historial[2:]:
    rol = "user" if mensaje["role"] == "user" else "assistant"
    avatar = "👤" if rol == "user" else "✨"
    with st.chat_message(rol, avatar=avatar):
        st.write(mensaje["parts"][0]["text"])

# 5. La caja de texto para escribir
prompt = st.chat_input("Escribile un mensaje a Nova...")

if prompt:
    # Mostramos lo que escribió el usuario
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    st.session_state.historial.append({"role": "user", "parts": [{"text": prompt}]})
    
    # Consultamos al cerebro de Nova
    try:
        respuesta = requests.post(url, json={"contents": st.session_state.historial})
        datos = respuesta.json()
        
        if "error" in datos:
            st.error(f"Uy, Google devolvió un error: {datos['error']['message']}")
            st.session_state.historial.pop()
        else:
            texto_nova = datos['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant", avatar="✨"):
                st.write(texto_nova)
            st.session_state.historial.append({"role": "model", "parts": [{"text": texto_nova}]})
            
    except Exception as e:
        st.error("Error de conexión con el cerebro de Nova.")
        st.session_state.historial.pop()
