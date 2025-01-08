import streamlit as st
from langchain_community.llms.ollama import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import random


# CSS personalizado para mejorar el diseño visual
st.markdown("""
    <style>
    .text-input-container {
        position: relative;
        width: 100%;
        display: flex;
        align-items: center;
        background-color: #FFFFFF
    }
    .text-input {
        width: 100%;
        padding-right: 40px;
    }
    .arrow {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 20px;
        color: white;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 75%;
    }
    .human-message {
        background-color: #ececec;
        text-align: left;
    }
    .bot-message {
        background-color: #6c63ff;
        text-align: right;
        color: white;
    }
    .container {
        display: flex;
        justify-content: space-between;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


llm = Ollama()
llm.model = "llama3.1:latest"


# Lista de frases de apoyo emocional
frases_apoyo_emocional = [
    "No estás solo; siempre hay personas que te quieren y te apoyan, como yo. Puedes contar conmigo en todo momento.",
    "Lo que estás pasando es muy difícil, pero eres muy fuerte y valiente. Estoy aquí para escucharte y ayudarte.",
    "Eres más fuerte de lo que crees. Sigue adelante.",
    "Recuerda que mereces respeto y cariño, siempre. Nada de lo que te puedan decir cambia lo especial que eres.",
    "Es normal sentirse triste a veces, recuerda que hay muchas cosas muy bonitas.",
    "Eres único y valioso, y el mundo necesita a personas como tú. No dejes que nadie te haga sentir menos.",
    "Hay personas que te quieren y siempre puedes pedir ayuda.",
    "Quienes lastiman también tienen heridas. No dejes que eso te defina.",
    "Tienes cualidades únicas que te hacen especial y fuerte."
]

# Función para obtener una frase de apoyo emocional aleatoria
def obtener_frase_apoyo():
    return random.choice(frases_apoyo_emocional)

# Función principal que controla la lógica del asistente emocional
def main():
    # Título principal de la aplicación
    st.title("Tommy tu amigo virtual 🤖")

    # Sección donde el usuario puede introducir el nombre del asistente
    bot_name = st.text_input("Nombre de tu Asistente Virtual:", value="Bot")

    # Prompt o mensaje base que define el comportamiento del asistente
    prompt = f"""Hola, me llamo {bot_name}. Respondo preguntas con respuestas simples quisiera conocerte mejor. Estoy aquí para ofrecerte apoyo emocional si lo necesitas y reforzar tu animo cuando lo necesites. "Aquí estoy para ayudarte"."""

    # Área para mostrar y permitir que el usuario edite la descripción del asistente
    bot_description = st.text_area("Descripción de tu Asistente Virtual:", value=prompt)

    # Historial de chat que se mantiene en la sesión de Streamlit
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Configuración del prompt del asistente con Langchain
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),  # Mensaje inicial del sistema que define el comportamiento del asistente
            MessagesPlaceholder(variable_name="chat_history"),  # Historial de mensajes para mantener la conversación
            ("human", "{input}"),  # Mensaje que introduce el usuario en el chat
        ]
    )

    # Unir el template del prompt con el modelo de lenguaje (LLaMA)
    chain = prompt_template | llm

    # Contenedor para el input del usuario
    st.markdown("<div class='text-input-container'>", unsafe_allow_html=True)

    # Entrada del usuario para hacer preguntas o comentarios
    user_input = st.text_input("Escribe tu pregunta o cuéntame cómo te sientes :", key="user_input", on_change=lambda: process_input(st.session_state.user_input), placeholder="Escribe aquí...")

    # Procesar la entrada del usuario
    def process_input(input_text):
        # Comprobar si el usuario ha ingresado texto
        if input_text:
            # Si el usuario dice "adios", se detiene la aplicación
            if input_text.lower() == "adios":
                st.stop()
            else:
                # Si el usuario pide frases emocionales o motivacionales
                if any(phrase in input_text.lower() for phrase in ["frases emocionales", "frase de apoyo", "motivación", "frase motivacional"]):
                    frase_apoyo = obtener_frase_apoyo()  # Obtener frase motivacional
                    st.session_state["chat_history"].append(HumanMessage(content=input_text))  # Guardar mensaje del usuario
                    st.session_state["chat_history"].append(AIMessage(content=f"{bot_name}: {frase_apoyo}"))  # Respuesta del bot
                else:
                    # Si es otro tipo de mensaje, se envía al modelo LLaMA para generar una respuesta
                    response = chain.invoke({"input": input_text, "chat_history": st.session_state["chat_history"]})
                    st.session_state["chat_history"].append(HumanMessage(content=input_text))  # Guardar mensaje del usuario
                    st.session_state["chat_history"].append(AIMessage(content=response))  # Respuesta del bot

                # Si el usuario menciona un problema o emociones negativas, el asistente ofrece apoyo emocional
                if any(word in input_text.lower() for word in ["problema", "ayuda", "triste", "siento", "me ayudas", "mal"]):
                    st.session_state["chat_history"].append(
                        AIMessage(content=f"{bot_name}: Parece que estás pasando por un momento difícil. ¿Te gustaría hablar más sobre eso?")
                    )
                    # Enviar una frase de apoyo emocional
                    frase_apoyo = obtener_frase_apoyo()
                    st.session_state["chat_history"].append(
                        AIMessage(content=f"{bot_name}: {frase_apoyo}")
                    )

                # Limpiar el campo de entrada después de procesar
                st.session_state.user_input = ""

    # Mostrar el historial del chat con diseño mejorado

    st.subheader("Chat")

    # Crear una variable para almacenar todo el historial de mensajes
    chat_display = ""

    # Iterar sobre el historial y concatenar mensajes
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            # Formato para el mensaje del usuario
            chat_display += f"Humano👻: {msg.content}\n\n"
        elif isinstance(msg, AIMessage):
            # Formato para el mensaje del asistente
            chat_display += f"{bot_name}🤖: {msg.content}\n\n"

    # Mostrar todo el historial de mensajes en un área de texto
    st.text_area("Historial del chat", value=chat_display, height=400, key="chat_area", disabled=True)


# Ejecución principal de la aplicación
if __name__ == '__main__':
    main()