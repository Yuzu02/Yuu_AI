import openai  # pip install openai
import typer  # pip install "typer[all]"
from rich import print  # pip install rich
from rich.table import Table

"""+
Descripción: Yuu AI 
Asistente de terminal que usa GPT-3.5 (Chat-GPT) para responder preguntas y dar asistencia en la terminal sobre programación.
Versión: 0.1
Made by:Yuzu (@Yuzu02)
"""

# Función principal
def main():
    #Obtener la API_KEY de https://platform.openai.com
    openai.api_key = ""

    # Título de la aplicación
    print("💬 [bold purple] Yuu AI [/bold purple]")
    
    # Tabla de comandos
    table = Table("Comando", "Descripción")
    table.add_row("new", "Crear una nueva conversación")
    table.add_row("help", "Mostrar la tabla de comandos")
    table.add_row("about", "Mostrar información sobre Yuu")
    table.add_row("exit", "Salir de la aplicación")
  
    print(table)
    
    # Mensaje de bienvenida
    print("\n👋 [bold purple]¡Hola! Soy Yuu, tu asistente de terminal.[/bold purple] ¿Que deseas?")
    
    # Verificar si la API_KEY está vacía
    while openai.api_key == "":
        print("\n🔑 [bold red]No se ha encontrado la API_KEY[/bold red]")
        print("\n🔑 [bold red]Obten tu API_KEY de https://platform.openai.com[/bold red]")
        
        # En el caso de que quieras poner la API_KEY directamente en el código y no pedirla al usuario vas a la linea 17 y la pones luego comenta la linea 39.
        openai.api_key = typer.prompt("\n🔑 Ingresa tu API_KEY")

    # Contexto del asistente
    context = {"role": "system",
               "content": "Eres una asistente llamada Yuu,Creada por Yuzu un programador el cual te ayudo a aprender todo lo que sabes,eres muy util en la solucion de problemas de programacion, dar explicaciones de codigo y ayudar a los usuarios a resolver sus dudas y dar asistencia en la Terminal"}
    messages = [context]
    
    '''
    El contexto es lo que hara que la asistenta tenga un rol en la conversación, es lo que hace a Yuu diferente a otras asistentes de terminal.
    Por lo cual no es recomendable cambiarlo.
    '''
    
    # Bucle infinito para mantener la conversación
    while openai.api_key != "":

        content = __prompt__()
        
        # Condiciones para los principales comandos
        if content == "new":
            print("🆕 Nueva conversación creada")
            messages = [context]
            content = __prompt__()

        messages.append({"role": "user", "content": content})
        
        # Parametros de la asistente
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=1000, temperature=0.9) 
        
        '''
        Libertad en cuanto a los parametros de la asistente, puedes cambiar el modelo de lenguaje de la asistente, el número de tokens, la temperatura, etc.
        
        Para cambiar el modelo de lenguaje de la asistente visita  https://platform.openai.com/docs/models
        Para cambiar el número de tokens cambia el valor de max_tokens (El maximo de tokens depende del modelo de lenguaje)
        Lo mismo para la temperatura, cambia el valor de temperature (Este valor va de 0 a 1)
        
        Y si deseas agregar mas parametros aca te dejo una lista de parametros que puedes usar:
        
        top_p: float = 1.0 (El valor por defecto es 1.0 y va de 0 a 1)
        frequency_penalty: float = 0.0 (El valor por defecto es 0.0 y va de 0 a 1)
        presence_penalty: float = 0.0 (El valor por defecto es 0.0 y no se recomienda cambiarlo)
        '''
        
        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})

        print(f"[bold green]> [/bold green] [green]{response_content}[/green]")

# Función para pedir la entrada del usuario
def __prompt__() -> str: 
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")
    
    # Condiciones para los comandos
    if prompt == "help":
        print("🆘 Comando de ayuda")
        print()
        print("Cada vez que quieras hablar con Yuu, solo tienes que escribir tu mensaje y presionar la tecla Enter.Teniendo en cuenta que primero debes crear una conversación con el comando [bold green]new[/bold green]")
        return __prompt__()
   
    if prompt == "about":
        print("📖 Acerca de Yuu")
        print()
        print("Yuu es una asistente de terminal que usa GPT-3.5 (Chat-GPT) creada por Yuzu (@Yuzu02) para responder preguntas y dar asistencia en la terminal sobre programación.")
        
    if prompt == "exit":
        exit = typer.confirm("✋ ¿Estás seguro?")
        if exit:
            print("👋 ¡Hasta luego!")
            raise typer.Abort()

        return __prompt__()
    return prompt

# Ejecutar la función principal
if __name__ == "__main__":
    typer.run(main)    