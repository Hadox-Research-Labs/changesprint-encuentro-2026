(async function () {
  const response = await fetch("slides-data.json");
  if (!response.ok) throw new Error("No se pudo cargar el contenido de la presentación.");
  const slides = await response.json();
  const container = document.querySelector("[data-slides-container]");

  slides.forEach((slide, index) => {
    const section = document.createElement("section");
    const number = String(index + 1).padStart(2, "0");
    section.dataset.backgroundImage = `assets/slides/slide-${number}.png?v=20260812-2`;
    section.dataset.backgroundSize = "contain";
    section.dataset.backgroundColor = [3, 7, 12].includes(index + 1) ? "#0c3747" : "#f7f4ea";
    section.dataset.slideTitle = slide.title;

    const notes = document.createElement("aside");
    notes.className = "notes";
    notes.textContent = `${slide.narration}\n\n[Sources]\n${slide.sources.map((source) => `- ${source}`).join("\n")}`;
    section.appendChild(notes);
    container.appendChild(section);
  });

  await Reveal.initialize({
    hash: true,
    controls: true,
    progress: true,
    slideNumber: "c/t",
    width: 1600,
    height: 900,
    margin: 0.02,
    minScale: 0.2,
    maxScale: 2,
    transition: "fade",
    backgroundTransition: "fade",
    pdfSeparateFragments: false,
    plugins: [RevealNotes]
  });

  document.dispatchEvent(new CustomEvent("curso0-ready"));
})().catch((error) => {
  const status = document.querySelector("[data-narration-status]");
  if (status) status.textContent = "Error de carga";
  console.error(error);
});
