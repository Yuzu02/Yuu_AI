import datetime # pip install datetime
import openai  # pip install openai
import typer # pip install "typer[all]"
import sqlite3 # pip install sqlite3
from rich import print  # pip install rich
from rich.table import Table

"""
Descripción: Yuu AI 
Asistente de terminal que usa GPT-3.5 (Chat-GPT) para responder preguntas y dar asistencia en la terminal sobre programación.
Versión: 0.2 (Beta) (Se añadio la base de datos de historial de conversación y se corrigieron algunos errores)
Made by:Yuzu (@Yuzu02)
"""

# Función para el manejo de la base de datos de historial de conversación
def init_db(nombre_db):
    conn = sqlite3.connect(nombre_db)
    c = conn.cursor()
    
    print("📁 [bold green]Conectado a la base de datos[/bold green]")
    
    # Verificar si la tabla de historial de conversación existe.
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_history'")
    
    if c.fetchone() is None:
     print("📁 [bold red]No se ha encontrado la base de datos[/bold red]")
     print("📁 [bold red]Conectando con la base de datos...[/bold red]")
    conn = sqlite3.connect('db/chat_history.db')
    c = conn.cursor()
    print("📁 [bold green]Base de datos creada[/bold green]")
    if c.fetchone() is not None: 
     print("📁 [bold green]Base de datos encontrada[/bold green]")
    
    # Crear tabla de historial de conversación
    c.execute("""CREATE TABLE IF NOT EXISTS chat_history (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Fecha TEXT NOT NULL,
        Numero_de_mensajes INTEGER NOT NULL,
        Usuario TEXT NOT NULL,
        Yuu TEXT NOT NULL)""")
    conn.commit()
    
    # Verificar si la tabla de historial de conversación está vacía
    if c.execute("SELECT * FROM chat_history").fetchone() is None:
        print("📁 [bold red]No se ha encontrado el historial de conversación[/bold red]")
        print("📁 [bold red]Creando historial de conversación...[/bold red]")
        c.execute("""INSERT INTO chat_history(Fecha, Numero_de_mensajes, Usuario, Yuu) VALUES(?, ?, ?, ?)""",
                  ("Sin historial", 0, "Sin historial", "Sin historial"))
        conn.commit()
        print("📁 [bold green]Historial de conversación creado[/bold green]")
    if c.execute("SELECT * FROM chat_history").fetchone() is not None:
        print("📁 [bold green]Historial de conversación encontrado[/bold green]")
                               
# Función principal
def main():
    #Obtener la API_KEY de https://platform.openai.com
    openai.api_key = ""

    # Título de la aplicación
    print("💬 [bold purple] Yuu AI [/bold purple]")

    # Inicializar la base de datos de historial de conversación
    init_db("db/chat_history.db")
    
    # Tabla de comandos
    print("\n📋 [bold purple]Tabla de Comandos[/bold purple]")
        
    table = Table("Comando", "Descripción")
    table.add_row("new", "Crear una nueva conversación")
    table.add_row("historial", "Mostrar el historial de conversación")
    table.add_row("help", "Mostrar la tabla de comandos")
    table.add_row("about", "Mostrar información sobre Yuu")
    table.add_row("exit", "Salir de la aplicación")
    print(table)
        
    # Verificar si la API_KEY está vacía
    while openai.api_key == "":
        print("\n🔑 [bold red]No se ha encontrado la API_KEY[/bold red]")
        print("\n🔑 [bold red]Obten tu API_KEY de https://platform.openai.com[/bold red]")
        
        # En el caso de que quieras poner la API_KEY directamente en el código y no pedirla al usuario vas a la linea 16 y la pones luego comenta la linea 39.
        openai.api_key = typer.prompt("\n🔑 Ingresa tu API_KEY")
        
        # Verificar si la API_KEY es válida
        while openai.api_key != "":
            try:
                openai.Completion.create(engine="gpt-3.5-turbo", prompt="", max_tokens=1)
            except openai.error.AuthenticationError:
                print("\n🔑 [bold red]La API_KEY no es válida[/bold red]")
                openai.api_key = typer.prompt("\n🔑 Ingresa tu API_KEY")    
                continue
            print("\n🔑 [bold green]API_KEY válida[/bold green]")
            
            # Mensaje de bienvenida
            print("\n👋 [bold purple]¡Hola! Soy Yuu, tu asistente de terminal.[/bold purple] ¿Que deseas?")

    # Contexto del asistente
    context = {"role": "system",
               "content": "Eres una asistente llamada Yuu,Creada por Yuzu un programador el cual te ayudo a aprender todo lo que sabes,eres muy util en la solucion de problemas de programacion, dar explicaciones de codigo y ayudar a los usuarios a resolver sus dudas y dar asistencia en la Terminal"}
    messages = [context]
    
    '''
    El contexto es lo que hara que la asistenta tenga un rol en la conversación, es lo que hace a Yuu diferente a otras asistentes de terminal.
    Por lo cual no es recomendable cambiarlo.
    '''
    
    # Bucle infinito para mantener la conversación abierta
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
        
        # Guardamos la fecha de creación de la conversación , el mensaje del usuario y la respuesta de la asistente en la base de datos de historial de conversación y el numero de mensajes
        conn = sqlite3.connect("db/chat_history.db")
        c = conn.cursor()
        c.execute("INSERT INTO chat_history VALUES (?,?,?,?)", (datetime.datetime.now(), content, response_content, len(messages)))
        
        conn.commit()
        
# Función para pedir la entrada del usuario
def __prompt__() -> str: 
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")
    
    # Condiciones para los comandos
    
    if prompt == "history":
        print("\n📁 Historial de conversación")
        
        # Verificamos si la tabla de historial esta vacia
        if len(c.fetchall()) == 0:
            print("📁 [bold red]No hay conversaciones guardadas[/bold red]")
            return __prompt__()
        
        # Mostrar el historial de conversación
        conn = sqlite3.connect("db/chat_history.db")
        c = conn.cursor()
        c.execute("SELECT * FROM chat_history")
        result = c.fetchall()
        
        # Tabla del historial de conversación
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fecha", justify="center", style="dim")
        table.add_column("Mensaje", justify="center", style="dim")
        table.add_column("Respuesta", justify="center", style="dim")
        table.add_column("Número de mensajes", justify="center", style="dim")
        
        # Agregar los datos a la tabla
        for row in result:
            table.add_row(str(row[0]), row[1], row[2], str(row[3]))
        
        print(table)
        return __prompt__()
                      
    if prompt == "help":
        print("\n🆘 Comando de ayuda")
        print()
        print("Cada vez que quieras hablar con Yuu, solo tienes que escribir tu mensaje y presionar la tecla Enter.Teniendo en cuenta que primero debes crear una conversación con el comando [bold green]new[/bold green]")
        return __prompt__()
   
    if prompt == "about":
        print("\n📖 Acerca de Yuu")
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
