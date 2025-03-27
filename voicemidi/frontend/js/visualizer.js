// Audio visualizer module for VoiceMIDI
import { appState } from "./app.js";

// Canvas and animation context
let canvas;
let ctx;
let animationId;
let lastTimestamp = 0;

// Audio data
const audioData = {
  waveform: new Array(1024).fill(0),
  pitch: {
    frequency: 0,
    confidence: 0,
  },
  level: 0,
};

// Visualization configuration
const config = {
  fps: 30,
  waveformColor: "#8e44ad",
  backgroundColor: "transparent",
  gridColor: "rgba(255, 255, 255, 0.1)",
  textColor: "rgba(255, 255, 255, 0.7)",
  lineWidth: 2,
  gridSpacingX: 50,
  gridSpacingY: 25,
};

// Set up the audio visualizer
export function setupAudioVisualizer() {
  // Get the canvas element
  canvas = document.getElementById("waveform-canvas");
  if (!canvas) {
    console.error("Waveform canvas not found");
    return;
  }

  // Set up the canvas for high-DPI displays
  setupCanvas();

  // Get the rendering context
  ctx = canvas.getContext("2d");

  // Start the animation loop
  startAnimation();

  // Set up resize handler
  window.addEventListener("resize", handleResize);
}

// Set up the canvas size and resolution
function setupCanvas() {
  // Get the device pixel ratio
  const dpr = window.devicePixelRatio || 1;

  // Get the canvas dimensions from CSS
  const rect = canvas.getBoundingClientRect();

  // Set the canvas size in pixels (multiplying by DPR for high-DPI displays)
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;

  // Scale the canvas to handle device pixel ratio
  if (dpr > 1) {
    canvas.style.width = rect.width + "px";
    canvas.style.height = rect.height + "px";
  }
}

// Handle window resize
function handleResize() {
  setupCanvas();
}

// Start the animation loop
function startAnimation() {
  if (animationId) {
    cancelAnimationFrame(animationId);
  }

  lastTimestamp = performance.now();

  // Start the animation loop
  animate();
}

// Animation loop
function animate(timestamp = 0) {
  animationId = requestAnimationFrame(animate);

  // Limit the frame rate
  const elapsed = timestamp - lastTimestamp;
  if (elapsed < 1000 / config.fps) {
    return;
  }

  lastTimestamp = timestamp;

  // Clear the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw the visualization
  drawVisualization();
}

// Draw the visualization
function drawVisualization() {
  // Draw the grid
  drawGrid();

  // Draw the waveform
  drawWaveform();

  // Draw frequency markers
  drawFrequencyMarkers();
}

// Draw the background grid
function drawGrid() {
  const width = canvas.width;
  const height = canvas.height;

  ctx.strokeStyle = config.gridColor;
  ctx.lineWidth = 1;

  // Vertical grid lines
  for (let x = 0; x < width; x += config.gridSpacingX) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }

  // Horizontal grid lines
  for (let y = 0; y < height; y += config.gridSpacingY) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }
}

// Draw the audio waveform
function drawWaveform() {
  const width = canvas.width;
  const height = canvas.height;
  const middle = height / 2;

  // Create a simulated waveform for demonstration
  // In a real implementation, this would use actual audio data
  simulateWaveform();

  ctx.strokeStyle = config.waveformColor;
  ctx.lineWidth = config.lineWidth;

  ctx.beginPath();

  const sliceWidth = width / audioData.waveform.length;

  for (let i = 0; i < audioData.waveform.length; i++) {
    const x = i * sliceWidth;
    const y = middle + audioData.waveform[i] * middle;

    if (i === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  }

  ctx.stroke();
}

// Draw frequency markers
function drawFrequencyMarkers() {
  const width = canvas.width;
  const height = canvas.height;

  // Draw frequency ticks on the left side
  ctx.fillStyle = config.textColor;
  ctx.font = "10px sans-serif";
  ctx.textAlign = "left";

  // Add some frequency markers (for illustration purposes)
  const frequencies = [100, 250, 500, 1000, 2000, 4000, 8000];

  frequencies.forEach((freq) => {
    // Map frequencies logarithmically to the canvas height
    const y = height - (Math.log(freq) / Math.log(10000)) * height;

    ctx.fillText(`${freq}Hz`, 5, y);
  });
}

// Simulate a waveform (replace with real audio data)
function simulateWaveform() {
  const time = performance.now() / 1000;

  // Generate a sine wave
  for (let i = 0; i < audioData.waveform.length; i++) {
    // Combine multiple sine waves for a more interesting waveform
    const t = i / audioData.waveform.length;

    // Base frequency from the appState (or use a default)
    const baseFreq = appState.currentFrequency || 440;

    // Calculate multiple harmonics
    const fundamental = Math.sin(
      2 * Math.PI * (t * 2 + time) * (baseFreq / 440)
    );
    const harmonic1 =
      Math.sin(2 * Math.PI * (t * 4 + time) * (baseFreq / 440)) * 0.5;
    const harmonic2 =
      Math.sin(2 * Math.PI * (t * 8 + time) * (baseFreq / 440)) * 0.25;

    // Combine the harmonics
    audioData.waveform[i] = (fundamental + harmonic1 + harmonic2) / 1.75;

    // Apply the audio level
    audioData.waveform[i] *= appState.audioLevel;
  }
}

// Update the visualizer with new audio data
export function updateVisualizer(data) {
  if (data.waveform) {
    audioData.waveform = data.waveform;
  }

  if (data.pitch) {
    audioData.pitch = data.pitch;
  }

  if (data.level !== undefined) {
    audioData.level = data.level;
  }
}
