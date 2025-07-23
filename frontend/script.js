// frontend/script.js

async function analyzeImage() {
  const imageInput = document.getElementById("imageInput");
  const resultDiv = document.getElementById("result");
  const loadingDiv = document.getElementById("loading");

  resultDiv.innerText = "";
  loadingDiv.style.display = "block";

  if (!imageInput.files[0]) {
    loadingDiv.style.display = "none";
    resultDiv.innerText = "Please select an image.";
    return;
  }

  const formData = new FormData();
  formData.append("image", imageInput.files[0]);

  try {
    const response = await fetch("http://localhost:5000/scan", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    loadingDiv.style.display = "none";
    resultDiv.innerText = data.analysis || "No analysis returned.";
  } catch (error) {
    console.error("Error:", error);
    loadingDiv.style.display = "none";
    resultDiv.innerText = "An error occurred. Please try again.";
  }
}
