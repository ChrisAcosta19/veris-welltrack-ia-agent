"""
Lógica central del agente conversacional de WellTrack utilizando LangChain.
"""
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SYSTEM_PROMPT = """Eres un agente conversacional de onboarding para la plataforma de bienestar WellTrack.
Tu objetivo ÚNICO es recopilar 3 datos básicos del usuario, en este ORDEN EXACTO:
1. Nombre
2. Edad
3. Objetivo principal (perder peso, ganar músculo o mejorar resistencia)

REGLAS ESTRICTAS:
- En tu PRIMERA intervención, DEBES saludar EXACTAMENTE con: "¡Hola! Bienvenido a WellTrack. Para empezar, ¿Cuál es su nombre?"
- Haz solo UNA pregunta a la vez. No avances a la siguiente pregunta si el usuario no ha respondido la anterior.
- En las preguntas de la Edad y del Objetivo, DEBES dirigirte al usuario mencionando su nombre (el que te dio en la pregunta 1). Por ejemplo: "Mucho gusto [Nombre]. ¿Cuántos años tiene?".
- NO ofrezcas consejos de salud, rutinas ni interactúes fuera de este guion.
- Una vez que hayas respondido a las 3 preguntas, DEBES generar un resumen EXACTAMENTE en este formato JSON, y NO añadir NINGÚN texto adicional antes o después del JSON. El JSON debe contener las llaves: "nombre", "edad", "objetivo". No digas nada más, solo devuelve el JSON.

Ejemplo de salida final esperada:
{"nombre": "Carlos", "edad": "28", "objetivo": "perder peso"}
"""

session_memory = {}

def get_session_history(session_id: str) -> list:
    if session_id not in session_memory:
        session_memory[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]
    return session_memory[session_id]

def run_agent(session_id: str, user_message: str) -> dict:
    history = get_session_history(session_id)
    history.append(HumanMessage(content=user_message))
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    response = llm.invoke(history)
    agent_message = response.content.strip()
    
    history.append(AIMessage(content=agent_message))
    
    is_final = False
    summary = None
    
    try:
        clean_json = agent_message.replace("```json", "").replace("```", "").strip()
        parsed_summary = json.loads(clean_json)
        
        if all(key in parsed_summary for key in ["nombre", "edad", "objetivo"]):
            is_final = True
            summary = parsed_summary
            agent_response_text = f"¡Gracias! He guardado tus datos:\n- Nombre: {summary['nombre']}\n- Edad: {summary['edad']}\n- Objetivo: {summary['objetivo']}"
        else:
            agent_response_text = agent_message
    except json.JSONDecodeError:
        agent_response_text = agent_message
        
    return {
        "response": agent_response_text,
        "is_final": is_final,
        "summary": summary
    }

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() 
    
    print("Iniciando prueba interactiva del Agente (presiona Ctrl+C para salir)...")
    test_session = "cli_session_01"
    
    try:
        result = run_agent(test_session, "hola")
        print("\nAgente:", result["response"])
        
        while not result["is_final"]:
            usr_msg = input("Usuario: ")
            result = run_agent(test_session, usr_msg)
            print("Agente:", result["response"])
            
        print("\n--- FIN DEL FLUJO ---")
        print("Resumen generado:", result["summary"])
    except Exception as e:
        print("Error durante ejecución:", e)
