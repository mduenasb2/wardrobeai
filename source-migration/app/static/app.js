const state = { person: null, garment: null, busy: false };
const maxDimension = 1024;

function byId(id) { return document.getElementById(id); }

function bindImageSlot(kind) {
  const input = byId(`${kind}-input`);
  const zone = byId(`${kind}-drop`);
  const preview = byId(`${kind}-preview`);
  const empty = byId(`${kind}-empty`);
  const actions = byId(`${kind}-actions`);
  const name = byId(`${kind}-name`);
  const openPicker = () => input.click();

  zone.addEventListener("click", (event) => {
    if (!event.target.closest("button")) openPicker();
  });
  zone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openPicker();
    }
  });
  byId(`${kind}-replace`).addEventListener("click", openPicker);
  byId(`${kind}-remove`).addEventListener("click", (event) => {
    event.stopPropagation();
    state[kind] = null;
    input.value = "";
    renderSlot(kind);
    showMessage("");
  });
  input.addEventListener("change", async () => {
    const file = input.files?.[0];
    input.value = "";
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      showMessage("Choose a supported image file.");
      return;
    }
    try {
      const decoded = await createImageBitmap(file);
      const scale = Math.min(1, maxDimension / Math.max(decoded.width, decoded.height));
      const canvas = document.createElement("canvas");
      canvas.width = Math.max(1, Math.round(decoded.width * scale));
      canvas.height = Math.max(1, Math.round(decoded.height * scale));
      canvas.getContext("2d", { alpha: false }).drawImage(decoded, 0, 0, canvas.width, canvas.height);
      decoded.close();
      state[kind] = { canvas, dataUrl: canvas.toDataURL("image/jpeg", 0.9), name: file.name };
      renderSlot(kind);
      showMessage("");
    } catch {
      showMessage("This image could not be opened. Choose another file.");
    }
  });

  function renderSlot(slot) {
    const image = state[slot];
    const slotPreview = byId(`${slot}-preview`);
    byId(`${slot}-empty`).hidden = Boolean(image);
    byId(`${slot}-actions`).hidden = !image;
    slotPreview.hidden = !image;
    if (image) {
      slotPreview.src = image.dataUrl;
      byId(`${slot}-name`).textContent = image.name;
    } else {
      slotPreview.removeAttribute("src");
      byId(`${slot}-name`).textContent = "";
    }
  }
}

function showMessage(text) {
  byId("message").textContent = text;
}

function compositePreview() {
  const person = state.person.canvas;
  const garment = state.garment.canvas;
  const output = document.createElement("canvas");
  output.width = person.width;
  output.height = person.height;
  const context = output.getContext("2d");
  context.drawImage(person, 0, 0);
  const garmentWidth = output.width * 0.68;
  const garmentHeight = garmentWidth * garment.height / garment.width;
  const left = (output.width - garmentWidth) / 2;
  const top = output.height * 0.28;
  context.drawImage(garment, 0, 0, garment.width, garment.height, left, top, garmentWidth, garmentHeight);
  return output.toDataURL("image/png");
}

function normalizeAsPng(dataUrl) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      const output = document.createElement("canvas");
      output.width = image.naturalWidth;
      output.height = image.naturalHeight;
      output.getContext("2d").drawImage(image, 0, 0);
      resolve(output.toDataURL("image/png"));
    };
    image.onerror = () => reject(new Error("The generated image could not be decoded."));
    image.src = dataUrl;
  });
}

async function generate() {
  if (!state.person) {
    showMessage("Please upload your photo first.");
    return;
  }
  if (!state.garment) {
    showMessage("Please select a clothing image first.");
    return;
  }
  state.busy = true;
  const button = byId("generate");
  button.disabled = true;
  button.querySelector("span:first-child").textContent = "Creating your preview…";
  showMessage("");
  try {
    const response = await fetch("/api/try-on", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ person: state.person.dataUrl, garment: state.garment.dataUrl }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Image generation failed.");
    let image = compositePreview();
    if (result.mode === "gemini" && result.image) {
      try {
        image = await normalizeAsPng(result.image);
      } catch {
        image = compositePreview();
      }
    }
    byId("result-image").src = image;
    byId("download").href = image;
    byId("workflow").hidden = true;
    byId("result").hidden = false;
    byId("result-message").textContent = result.message || (result.mode === "gemini" ? "Generated with Gemini." : "Local preview · no image was sent to an external service.");
    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (error) {
    showMessage(error instanceof Error ? error.message : "Unable to generate the try-on image. Please try again.");
  } finally {
    state.busy = false;
    button.disabled = false;
    button.querySelector("span:first-child").textContent = "Try on this look";
  }
}

byId("generate").addEventListener("click", generate);
byId("another").addEventListener("click", () => {
  state.garment = null;
  byId("garment-input").value = "";
  byId("garment-preview").removeAttribute("src");
  byId("garment-preview").hidden = true;
  byId("garment-empty").hidden = false;
  byId("garment-actions").hidden = true;
  byId("garment-name").textContent = "";
  byId("result-image").removeAttribute("src");
  byId("result").hidden = true;
  byId("workflow").hidden = false;
  showMessage("");
  window.scrollTo({ top: 0, behavior: "smooth" });
});

bindImageSlot("person");
bindImageSlot("garment");
fetch("/api/health").then((response) => response.json()).then(({ gemini_available }) => {
  byId("mode-hint").textContent = gemini_available
    ? "Gemini is configured · otherwise a local preview is used"
    : "Local preview mode · no API key required";
}).catch(() => {
  byId("mode-hint").textContent = "Local preview mode · no API key required";
});
