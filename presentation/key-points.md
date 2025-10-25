Introducción

* Hola a todos, gracias por venir a mi charla.
* Tema: Caza de Bug Bounties con Agentes de IA

Sobre Mí

* Soy David, desarrollador de software.
* Arquitecto de software en nag en Basilea (nag.ch).
* Empresa chica pero genial, buen empleador y socio de IT.
* Más de 20 años de experiencia en desarrollo web y móvil.
* Todavía luchando con las codificaciones como pueden ver en mi apellido.
* Contacto: ueblacker.dev o escaneen el código QR.

Sueños de Hacker

* Siempre soñé con ser un hacker notorio.
* No soy muy bueno hackeando — ¡pero tengo curiosidad!
* Realidad: escribo POJOs de Java todos los días.

Bug Bounty como Hobby

* Me metí en la caza de bug bounties por interés en el pentesting.
* Es como resolver puzzles — ¡y te pueden pagar!
* Ayuda a los desarrolladores a evitar errores de seguridad.

¿Qué es la Caza de Bug Bounties?

* Encontrar y reportar vulnerabilidades de seguridad antes que los atacantes.
* Las empresas crean programas con reglas y alcance claros.
* Hacking legal y ético — las recompensas incluyen dinero o reconocimiento.

Dónde Empezar

* Plataformas: HackerOne, BugCrowd, BugBountySwitzerland.
* Aprender con Hack The Box, TryHackMe.
* Preguntarle a ChatGPT o tu LLM favorito.
* Debe saber: OWASP y la app Juice Shop (intencionalmente insegura).
* Juice Shop = terreno perfecto de pruebas para mis agentes de IA.
* El año pasado en la conferencia de desarrolladores, necesitaba un proyecto paralelo para aprender toda esta nueva tecnología de IA

5'

Intento #1

* Solo usar chat GPT "Por favor hackea tesla.com"
* No funciona realmente, podés hacer que Chat GPT haga un escaneo de seguridad simple de tu propio sitio web
* Y está violando los términos de Chat GPT

¿Qué es un LLM?

* Un LLM está hecho para crear texto similar al humano
* Enviás un texto al modelo y obtenés una respuesta
* El modelo es estático, no puede aprender o recordar algo por sí mismo

¿Qué es un Agente?

* Un agente toma un objetivo: ej. encontrar el mejor restaurante en basilea
* Tiene acceso a un llm y herramientas como un motor de búsqueda web
* llama repetidamente al llm y herramientas hasta que ha logrado el objetivo

LangChain & LangGraph

* LangChain: herramientas y conectores para LLMs
* LangGraph: orquestación de flujos de trabajo complejos de agentes
* Python open source pero hay equivalentes para JS y Java
* Lize Raes


Juice Shop

* La aplicación web más insegura que existe
* Proporcionada por OWASP para propósitos de entrenamiento

7'

Intento #2 — Resultado

* Muy poco esfuerzo, resultado impresionante

12'

Intento #3

* Aplicación de agente de tres fases
* Reconocimiento (análisis)
* Planificación de pequeñas tareas de hacking
* Ejecución usando una herramienta de análisis adicional
* Crear un reporte que incluye todo lo necesario, como pasos para reproducir

Intento #3 — Resultado

* Mi sueño de tener un agente que automáticamente realice caza de bug bounties 24/7 ya no era realista — muy caro.
* Investigué si otros tenían la misma idea.
* Todas las empresas que proporcionan herramientas de seguridad también están integrando IA.
* Encontré una herramienta de seguridad open source prometedora que quiero mostrarles brevemente al final.

14'

Cybersecurity AI (CAI)

* Open source
* Muchas herramientas incluidas
* Extensible
* Un asistente que funciona como GitHub Copilot o Claude Code
* De AliasRobotics, que hace testing de seguridad de robots

18'

Puntos clave

* Muy caro para caza de bug bounties completamente automatizada
* Los límites de tamaño de contexto son un problema
* Los modelos difieren significativamente
* Los ataques de ciberseguridad se han vuelto más fáciles de llevar a cabo
* Impresionante cuánto se puede lograr con muy poco esfuerzo
* Como nosotros los desarrolladores, los expertos en seguridad necesitan mantenerse al día con los desarrollos para no quedarse atrás de los atacantes maliciosos

