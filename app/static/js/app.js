const timer = document.querySelector("[data-timer]");
if (timer) {
  const started = Date.now();
  setInterval(() => {
    timer.textContent = `${Math.floor((Date.now() - started) / 1000)}s`;
  }, 1000);
}

const voiceButton = document.querySelector("[data-voice]");
if (voiceButton) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    voiceButton.hidden = true;
  } else {
    voiceButton.addEventListener("click", () => {
      const recognition = new SpeechRecognition();
      recognition.lang = document.documentElement.lang || "ru-RU";
      recognition.onresult = (event) => {
        const textarea = document.querySelector("textarea[name='answer_text']");
        textarea.value = `${textarea.value} ${event.results[0][0].transcript}`.trim();
      };
      recognition.start();
    });
  }
}

