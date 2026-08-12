(function () {
  const state = { auto: false, speaking: false, paused: false, voices: [], chunks: [], chunkIndex: 0, runId: 0, voiceFallback: false };
  const controls = document.querySelector(".narration-controls");
  const status = controls?.querySelector("[data-narration-status]");
  const voiceSelect = controls?.querySelector("[data-narration-voice]");
  const rateInput = controls?.querySelector("[data-narration-rate]");
  const rateValue = controls?.querySelector("[data-narration-rate-value]");
  const pauseButton = controls?.querySelector("[data-narration-pause]");
  const captions = document.querySelector(".narration-captions");
  const captionText = captions?.querySelector("[data-narration-caption]");

  function setStatus(value) { if (status) status.textContent = value; }
  function setPauseLabel(value) { if (pauseButton) pauseButton.textContent = value; }
  function showCaptions(value) { if (captions && captionText) { captionText.textContent = value; captions.hidden = false; } }
  function hideCaptions() { if (captions && captionText) { captionText.textContent = ""; captions.hidden = true; } }
  function normalizeNotes(value) { return value.split("[Sources]")[0].replace(/\s+/g, " ").trim(); }
  function currentNotes() { return normalizeNotes(Reveal.getCurrentSlide()?.querySelector("aside.notes")?.textContent || ""); }
  function splitIntoChunks(value) {
    const sentences = value.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [value];
    const chunks = [];
    let current = "";
    sentences.forEach((sentence) => {
      const clean = sentence.trim();
      if (!clean) return;
      if (`${current} ${clean}`.trim().length <= 240) current = `${current} ${clean}`.trim();
      else { if (current) chunks.push(current); current = clean; }
    });
    if (current) chunks.push(current);
    return chunks;
  }
  function selectedVoice() {
    if (state.voiceFallback || !voiceSelect?.value) return null;
    return state.voices.find((voice) => voice.name === voiceSelect.value) || null;
  }
  function rate() { return rateInput ? Number(rateInput.value) : 0.95; }
  function updateRateLabel() { if (rateValue) rateValue.textContent = `${rate().toFixed(2).replace(/0$/, "")}x`; }
  function adjustRate(delta) {
    if (!rateInput) return;
    rateInput.value = Math.min(Number(rateInput.max), Math.max(Number(rateInput.min), rate() + delta)).toFixed(2);
    updateRateLabel();
  }
  function populateVoices() {
    if (!("speechSynthesis" in window) || !voiceSelect) return;
    state.voices = window.speechSynthesis.getVoices();
    const spanish = state.voices.filter((voice) => /^es(-|_)?/i.test(voice.lang));
    const choices = spanish.length ? spanish : state.voices;
    const previous = voiceSelect.value;
    voiceSelect.innerHTML = "";
    choices.forEach((voice) => {
      const option = document.createElement("option");
      option.value = voice.name;
      option.textContent = `${voice.name} (${voice.lang})`;
      voiceSelect.appendChild(option);
    });
    if (previous) voiceSelect.value = previous;
  }
  function finishSlide(runId) {
    if (runId !== state.runId) return;
    state.speaking = false;
    state.paused = false;
    setPauseLabel("Pausa");
    if (state.auto) {
      const index = Reveal.getIndices();
      if (index.h + 1 < Reveal.getTotalSlides()) { Reveal.next(); window.setTimeout(() => speakCurrent(true), 450); }
      else { state.auto = false; hideCaptions(); setStatus("Finalizado"); }
    } else { hideCaptions(); setStatus("Listo"); }
  }
  function speakNextChunk(runId) {
    if (runId !== state.runId || state.paused) return;
    const value = state.chunks[state.chunkIndex];
    if (!value) return finishSlide(runId);
    const utterance = new SpeechSynthesisUtterance(value);
    utterance.lang = "es-MX";
    utterance.rate = rate();
    utterance.pitch = 1;
    const voice = selectedVoice();
    if (voice) utterance.voice = voice;
    showCaptions(value);
    setStatus(state.auto ? "Narrando automáticamente" : "Narrando lámina");
    utterance.onend = () => { if (runId === state.runId) { state.chunkIndex += 1; window.setTimeout(() => speakNextChunk(runId), 90); } };
    utterance.onerror = (event) => {
      if (runId !== state.runId || ["interrupted", "canceled"].includes(event?.error)) return;
      if (selectedVoice() && !state.voiceFallback) { state.voiceFallback = true; setStatus("Probando voz predeterminada"); return window.setTimeout(() => speakNextChunk(runId), 120); }
      state.speaking = false; state.auto = false; state.paused = false; hideCaptions(); setPauseLabel("Pausa"); setStatus("Error de narración");
    };
    window.speechSynthesis.speak(utterance);
  }
  function stopNarration() {
    state.runId += 1; state.auto = false; state.speaking = false; state.paused = false; state.chunks = []; state.chunkIndex = 0;
    window.speechSynthesis?.cancel(); setPauseLabel("Pausa"); hideCaptions(); setStatus("Detenido");
  }
  function togglePause() {
    if (!("speechSynthesis" in window) || !state.speaking) return;
    if (state.paused) { window.speechSynthesis.resume(); state.paused = false; setPauseLabel("Pausa"); setStatus(state.auto ? "Narrando automáticamente" : "Narrando lámina"); }
    else { window.speechSynthesis.pause(); state.paused = true; setPauseLabel("Continuar"); setStatus("En pausa"); }
  }
  function speakCurrent(autoAdvance) {
    if (!("speechSynthesis" in window)) return setStatus("Narración no disponible");
    const value = currentNotes();
    if (!value) return setStatus("Esta lámina no tiene notas");
    state.runId += 1; window.speechSynthesis.cancel(); state.auto = Boolean(autoAdvance); state.speaking = true; state.paused = false; state.voiceFallback = false;
    state.chunks = splitIntoChunks(value); state.chunkIndex = 0; setPauseLabel("Pausa"); speakNextChunk(state.runId);
  }
  function init() {
    controls?.querySelector("[data-narration-current]")?.addEventListener("click", () => speakCurrent(false));
    controls?.querySelector("[data-narration-auto]")?.addEventListener("click", () => speakCurrent(true));
    controls?.querySelector("[data-narration-pause]")?.addEventListener("click", togglePause);
    controls?.querySelector("[data-narration-stop]")?.addEventListener("click", stopNarration);
    controls?.querySelector("[data-narration-slower]")?.addEventListener("click", () => adjustRate(-0.1));
    controls?.querySelector("[data-narration-faster]")?.addEventListener("click", () => adjustRate(0.1));
    rateInput?.addEventListener("input", updateRateLabel);
    window.addEventListener("keydown", (event) => {
      if (["INPUT", "SELECT", "TEXTAREA"].includes(event.target?.tagName)) return;
      if (event.key.toLowerCase() === "n") speakCurrent(false);
      if (event.key.toLowerCase() === "a") speakCurrent(true);
      if (event.key.toLowerCase() === "x") stopNarration();
      if (event.key.toLowerCase() === "p") togglePause();
    });
    populateVoices(); updateRateLabel();
    if ("speechSynthesis" in window) { window.speechSynthesis.onvoiceschanged = populateVoices; setStatus("Listo"); }
    else setStatus("Narración no disponible");
  }
  document.addEventListener("curso0-ready", init, { once: true });
})();
