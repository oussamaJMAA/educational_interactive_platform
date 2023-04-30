const result = document.getElementById("result");

      window.SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.interimResults = true;

      recognition.addEventListener("result", (e) => {
        const transcript = Array.from(e.results)
          .map((result) => result[0])
          .map((result) => result.transcript)
          .join("");

        result.innerHTML = transcript;
      });

      recognition.addEventListener("end", () => {
        recognition.stop();
      });

      function startRecognition(lang) {
        recognition.lang = lang;
        recognition.start();
      }