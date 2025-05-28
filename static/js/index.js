document.getElementById("download").addEventListener("click", function () {
  const exeUrl = "https://pixeldrain.com/api/file/jyHE1eax"; // Direct API download URL

  const a = document.createElement("a");
  a.href = exeUrl;
  a.download = "GameFitAI.exe"; // Desired filename
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
});
