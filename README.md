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

## Traducciones completas del sitio original

- [English](en/): la misma página principal, master class, dos presentaciones y ejercicio aplicado que el original.
- [Հայերեն](hy/): las mismas cinco páginas en armenio, como traducción asistida por IA pendiente de revisión de un especialista armeniohablante.

Se conserva la estructura HTML, las secciones, las imágenes y los destinos de navegación del sitio español. Cada texto y atributo accesible de las páginas tiene una traducción explícita; el constructor falla si falta una. Se traducen íntegramente las 39 notas de las dos sesiones y las 17 notas de la master class por idioma. Las notas aparecen debajo de cada lámina, se sincronizan con la navegación y pueden narrarse en el idioma seleccionado si el navegador ofrece una voz adecuada. Cambiar de idioma conserva la lámina actual.

Las imágenes de las láminas y los archivos originales PDF/PPTX siguen en español. Las descargas que conservan el original se identifican como tales; los guiones íntegros y la guía de facilitación están traducidos. Los materiales de práctica de la primera edición de lectura permanecen disponibles en `en/downloads/` y `hy/downloads/`, pero no sustituyen los originales ni las traducciones completas. Los enlaces anteriores `session-1.html`, `session-2.html` y `workshop.html` redirigen ahora a las páginas completas. No hay una portada resumida alternativa por idioma.

Fuentes activas: `i18n/full-ui-source.json`, `i18n/full-ui.tsv`, `i18n/en/notes-full.md`, `i18n/hy/notes-full.md`, `i18n/masterclass-full.tsv` e `i18n/full-docs/`. Regenerar y comprobar las diez páginas completas con:

```bash
python tools/build_languages.py
python tools/check_languages.py
```
