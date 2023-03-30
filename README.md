<h1> Yuu AI </h1>

<p>Yuu AI es un asistente de terminal que utiliza GPT-3.5 (Chat-GPT) para responder preguntas y ofrecer asistencia en la terminal sobre programación. Puedes crear una conversación con Yuu y hacerle cualquier pregunta relacionada con la programación.</p>

<h2>Instalación</h2>
<p>Para utilizar Yuu AI, necesitarás instalar los siguientes paquetes: </p>

<ul>
<li>OPENAI</li>
<li>TYPER</li>
<li>RICH</li>
</ul>

<h2> Tomar en cuenta lo siguiente: </h2>

<p>Primero, debes obtener una API_KEY de https://platform.openai.com. Una vez que tengas la API_KEY, puedes configurarla en el archivo main.py en la línea 17, o introducirla cuando se te solicite al iniciar la aplicación.</p>

<h2> Personalización </h2>
<p>Puedes personalizar la configuración de Yuu cambiando el modelo de lenguaje, el número de tokens y la temperatura en el archivo main.py. También puedes agregar más parámetros a la función openai.ChatCompletion.create() como top_p, frequency_penalty y presence_penalty. Consulta la documentación de OpenAI para más información.</p>
