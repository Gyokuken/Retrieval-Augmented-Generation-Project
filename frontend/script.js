const BACKEND_URL = "https://retrieval-augmented-generation-project-production.up.railway.app"; 
// change to deployed backend URL later

async function ingest() {
  const text = document.getElementById("docInput").value.trim();

  if (!text) {
    alert("Please paste a document to ingest.");
    return;
  }

  try {
    const res = await fetch(`${BACKEND_URL}/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        title: "User Input"
      })
    });

    if (!res.ok) throw new Error("Ingest failed");

    alert("Document ingested successfully!");
    document.getElementById("docInput").value = "";
  } catch (err) {
    console.error(err);
    alert("Failed to ingest document.");
  }
}

async function ask() {
  const query = document.getElementById("queryInput").value.trim();
  const answerEl = document.getElementById("answer");
  const timingEl = document.getElementById("timing");
  const sourcesEl = document.getElementById("sources");

  if (!query) {
    alert("Please enter a question.");
    return;
  }

  // Reset UI
  answerEl.textContent = "Thinking...";
  timingEl.textContent = "";
  sourcesEl.innerHTML = "";

  try {
    const res = await fetch(`${BACKEND_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    if (!res.ok) throw new Error("Query failed");

    const data = await res.json();

    // Answer
    answerEl.textContent =
      data.answer || "No relevant answer found.";

    // Timing
    if (data.latency_ms !== undefined) {
      timingEl.textContent = `Response time: ${data.latency_ms} ms`;
    }

    // Sources
    if (data.sources && data.sources.length > 0) {
      data.sources.forEach((src, i) => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>[${i + 1}]</strong> ${src.content}`;
        sourcesEl.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "No sources returned.";
      sourcesEl.appendChild(li);
    }
  } catch (err) {
    console.error(err);
    answerEl.textContent =
      "Something went wrong while generating the answer.";
  }
}

