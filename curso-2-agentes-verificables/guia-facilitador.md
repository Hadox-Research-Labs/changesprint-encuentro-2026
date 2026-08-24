# Guía de facilitación

## Parte 2 — ChatGPT, Codex y agentes verificables

### Resultado de la sesión

Al final de 120 minutos, cada equipo habrá configurado en Codex un agente especializado, ejecutado cinco pruebas y documentado al menos una corrección. No se construirá un sistema de producción ni se utilizarán datos reales.

### Preparación del facilitador

1. Confirmar que cada equipo cuenta con una computadora Windows y acceso a ChatGPT/Codex.
2. Pedir que descarguen el kit correspondiente desde la página del curso.
3. Descomprimir el kit en una carpeta local y abrir esa carpeta en Codex.
4. Mantener el modo de permisos en **Ask for approval** durante el taller.
5. Prohibir expresamente el uso de expedientes o información personal real.

### Guion de 120 minutos

- **00–10 min:** apertura, relación con la sesión anterior y resultado esperado.
- **10–25 min:** Chat, Work y Codex; recorrido de la aplicación en Windows.
- **25–40 min:** carpeta, contexto, herramientas, terminal, permisos y artefactos.
- **40–50 min:** prompt, `AGENTS.md`, skill, plugin y subagente.
- **50–65 min:** demostración del revisor de ensayos.
- **65–70 min:** descarga de kits y asignación de roles.
- **70–105 min:** construcción y cinco pruebas por equipo.
- **105–115 min:** corrección y repetición de una prueba fallida.
- **115–120 min:** demostraciones breves y cierre.

### Demostración recomendada

1. Ejecutar el caso de ensayo con un prompt suelto: “Califica este ensayo”.
2. Señalar criterios implícitos, ausencia de evidencia y exceso de autoridad.
3. Abrir la carpeta configurada con `AGENTS.md`, rúbrica y formato de salida.
4. Crear la skill con `$skill-creator`.
5. Ejecutar el caso con inyección de instrucciones.
6. Mostrar cómo la salida cita evidencia, declara incertidumbre y conserva la revisión humana.

### Roles dentro de cada equipo

- **Operador/a:** trabaja directamente en Codex.
- **Responsable de reglas:** revisa `AGENTS.md` y límites.
- **Responsable de evidencia:** comprueba citas, faltantes e inferencias.
- **Responsable de pruebas:** lleva la bitácora.
- **Relator/a:** prepara la demostración de tres minutos.

### Señales de que el equipo necesita intervención

- Está intentando resolver todo mediante un único prompt.
- La salida toma una decisión final sobre el beneficio.
- Se califican ortografía o estilo sin que la rúbrica lo permita.
- El agente inventa información faltante.
- No se guardan resultados ni bitácora.
- El equipo evita probar casos difíciles para que la demostración “salga bien”.

### Criterio de cierre

El equipo no necesita presentar un agente perfecto. Debe poder explicar qué hace, qué no hace, con qué evidencia trabaja, cómo se probó y qué riesgo permanece bajo supervisión humana.

### Fuentes oficiales del entorno

- Codex para Windows: https://learn.chatgpt.com/docs/windows/windows-app
- Chat, Work y Codex: https://learn.chatgpt.com/docs/use-chatgpt
- Configuración con `AGENTS.md`: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Construcción de skills: https://learn.chatgpt.com/docs/build-skills
- Permisos: https://learn.chatgpt.com/docs/permission-modes
- Subagentes: https://learn.chatgpt.com/docs/agent-configuration/subagents

