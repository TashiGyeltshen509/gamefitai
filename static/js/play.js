// Setup socket.io connection based on current protocol, hostname, port
const protocol = window.location.protocol;
const hostname = window.location.hostname;
const port = window.location.port || (protocol === "https:" ? 443 : 80);
const socket = io.connect(`${protocol}//${hostname}:${port}`, {
  transports: ["websocket"],
  timeout: 10000,
});

// Generate a random token to identify this client session
const token = Math.floor(1000 + Math.random() * 9000).toString();
console.log("Your token:", token);

// Get the <img> element to display processed frames
const processedImg = document.getElementById("processed-video");

// Create reusable canvas and context for capturing frames
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

// Access webcam video stream
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    const video = document.createElement("video");
    video.srcObject = stream;
    video.play();

    // Start capturing frames once video is ready
    video.onloadeddata = () => {
      captureAndSendFrame(video);
    };
  })
  .catch((err) => {
    console.error("Camera access error:", err);
  });

// Capture frame, encode as JPEG base64, send to server, repeat for ~30fps
function captureAndSendFrame(video) {
  if (video.videoWidth === 0 || video.videoHeight === 0) {
    // Not ready, try again shortly
    setTimeout(() => captureAndSendFrame(video), 100);
    return;
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Compress JPEG quality to reduce data size
  const frame = canvas.toDataURL("image/jpeg", 0.7);

  // Send the frame with the token to server for processing
  socket.emit("client_frame", { frame, token });

  // Capture next frame after ~33ms (~30fps)
  setTimeout(() => captureAndSendFrame(video), 33);
}

// Listen for processed frames from server specific to this token
socket.on(`processed_frame_${token}`, (data) => {
  if (data.frame) {
    processedImg.src = data.frame;
    // Optional: console.log("Displayed processed frame");
  } else {
    console.warn("No frame received");
  }
});

// Socket connection event handlers
socket.on("connect", () => {
  console.log("Socket connected:", socket.id);
});
socket.on("connect_error", (err) => {
  console.error("Socket connection error:", err);
});
socket.on("disconnect", (reason) => {
  console.warn("Socket disconnected:", reason);
});
