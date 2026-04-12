
/**
 * List of all constants used in this file
 */

const BACKEND_API_URL = "/api/compare";
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

/**
 * Adding Event Listeners to get the Prompt Message from user 
 */
const promptMessage = document.getElementById("prompt");
// Support pressing 'enter' key to submit response as well, other then Send button
promptMessage.addEventListener("keydown", (ev) => {
  if (ev.key === "Enter" && (ev.metaKey || ev.ctrlKey)) {
    ev.preventDefault();
    sendPromptToAIModels();
  }
});


/**
 * Adding Event Listener for the Send Button
 */
const sendButton = document.getElementById("send");
sendButton.addEventListener("click", sendPromptToAIModels);

// Focus on async-await pattern when invoking the APIs to backend
async function sendPromptToAIModels() {
  const prompt = promptMessage.value.trim();
  if (!prompt) {
    setStatus("Enter a prompt first.");
    return;
  }
  sendButton.disabled = true;
  setStatus("Calling models…");
  resultsEl.innerHTML = "";

  try {
    // Sending prompt from UI to backend directly.
    const res = await fetch(BACKEND_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || res.statusText);
    }
    const data = await res.json();
    renderResults(data);
    setStatus("Done.");
  } catch (e) {
    setStatus(`Error: ${e.message}`);
  } finally {
    sendButton.disabled = false;
  }
}



function setStatus(text) {
  statusEl.textContent = text;
}

function renderResults(data) {
  resultsEl.innerHTML = "";
  data.results.forEach((r) => {
    const card = document.createElement("article");
    card.className = "card";
    const title = document.createElement("h2");
    title.textContent = `${r.provider} · ${r.model}`;
    card.appendChild(title);
    if (r.error) {
      const err = document.createElement("p");
      err.className = "error";
      err.textContent = r.error;
      card.appendChild(err);
    } else {
      const pre = document.createElement("pre");
      pre.className = "answer";
      pre.textContent = r.text || "(empty response)";
      card.appendChild(pre);
    }
    resultsEl.appendChild(card);
  });
}


