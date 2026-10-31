# ChangeSprint Encuentro 2026

Sitio público: <https://hadox-research-labs.github.io/changesprint-encuentro-2026/>

El sitio reúne la ruta vigente del taller de Edgar Valdés:

1. [Primera intervención: IA responsable en lo público](curso-1-ia-responsable/), con 27 láminas, navegación web y narración automática.
2. [Segunda intervención: de principios a agentes verificables](curso-2-agentes-verificables/), con presentación narrada y Ejercicio 1 guiado.
3. [Ejercicio 2: del lienzo al agente](ejercicio-2-proyecto-propio/), aplicación posterior sobre los proyectos de los equipos.
4. [Tarea previa](tarea-previa/Tarea_Previa_IA_Fondo_Nacional_Becas_ChangeSprint_2026.pdf), en formato PDF.
5. [Manual de instalación de ChatGPT y Codex](output/pdf/Manual_Instalacion_ChatGPT_Codex_Windows_macOS_ChangeSprint_2026.pdf), para Windows y macOS.
6. [Instrucciones del Ejercicio 1](output/pdf/Ejercicio_1_Guiado_Agentes_Verificables_ChangeSprint_2026.pdf), práctica guiada con kits ficticios.
7. [Instrucciones del Ejercicio 2](output/pdf/Ejercicio_2_Del_Lienzo_Al_Agente_ChangeSprint_2026.pdf), aplicación al proyecto de cada equipo.

## Controles de la presentación

- `N`: narrar la lámina actual.
- `A`: narrar automáticamente y avanzar.
- `P`: pausar o continuar.
- `X`: detener la narración.
- `F`: pantalla completa.
- Flechas: navegación manual.

## Uso local

Desde la raíz del repositorio:

```bash
python -m http.server 8088
```

Abrir `http://localhost:8088/`.

GitHub Pages publica el repositorio desde la raíz de la rama `main`.

## Ediciones de lectura en inglés y armenio

- [English](en/): las dos sesiones (27 + 12 temas), cuaderno práctico y kits descargables.
- [Հայերեն](hy/): el mismo recorrido en armenio, como traducción asistida por IA pendiente de revisión de un especialista armeniohablante.

Las ediciones de lectura trasladan las notas docentes a HTML accesible, con adaptación editorial ligera para estudio autónomo. Incluyen preparación, reglas de trabajo, los tres kits con cinco casos ficticios por equipo y plantillas para el ejercicio aplicado. Los casos de variación lingüística se adaptan al idioma de lectura. Se conserva el contexto original de Guatemala/FONABE; no se presenta como normativa de Armenia.

Los originales visuales, la master class adicional y los PDF/PPTX continúan en español y están identificados como tales. Las descargas traducidas son Markdown y ZIP; el lector permite imprimir o guardar como PDF desde el navegador. La narración sólo utiliza una voz del idioma seleccionado si el navegador dispone de ella; nunca sustituye una voz inglesa para leer armenio.

Fuentes de traducción: `i18n/en/` e `i18n/hy/`. Regenerar las ocho páginas y los ocho paquetes ZIP con:

```bash
python tools/build_languages.py
python tools/check_languages.py
```
