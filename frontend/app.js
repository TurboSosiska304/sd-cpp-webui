const promptInput = document.getElementById("prompt");

const widthInput = document.getElementById("width");
const heightInput = document.getElementById("height");
const stepsInput = document.getElementById("steps");
const seedInput = document.getElementById("seed");

const generateButton = document.getElementById("generate");

const imageContainer = document.getElementById("image-container");

const statusElement = document.getElementById("status");


function setStatus(text) {
    statusElement.textContent = text;
}


function setGenerating(isGenerating) {
    generateButton.disabled = isGenerating;

    if (isGenerating) {
        generateButton.textContent = "Generating...";
    } else {
        generateButton.textContent = "Generate";
    }
}


async function generate() {

    const prompt = promptInput.value.trim();

    if (!prompt) {
        setStatus("Prompt is empty");
        return;
    }


    const request = {
        prompt: prompt,

        width: Number(widthInput.value),

        height: Number(heightInput.value),

        steps: Number(stepsInput.value),

        seed: Number(seedInput.value),
    };


    setGenerating(true);

    setStatus("Generating...");


    imageContainer.innerHTML = `
        <div class="placeholder">
            stable-diffusion.cpp is working...
        </div>
    `;


    try {

        const response = await fetch(
            "/api/generate",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify(request),
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.detail || "Generation failed"
            );
        }


        if (!data.success || !data.image) {
            throw new Error(
                "Backend returned an invalid response"
            );
        }


        const image = document.createElement("img");

        image.src = data.image;

        image.alt = "Generated image";


        imageContainer.innerHTML = "";

        imageContainer.appendChild(image);


        setStatus("Done");

    } catch (error) {

        console.error(error);


        imageContainer.innerHTML = `
            <div class="placeholder">
                Generation failed.<br><br>
                ${escapeHtml(error.message)}
            </div>
        `;


        setStatus("Error");

    } finally {

        setGenerating(false);
    }
}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


generateButton.addEventListener(
    "click",
    generate
);