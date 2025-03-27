// Microphone calibration module
import { appState } from "./app.js";

// Calibration state data
const calibrationState = {
  isCalibrating: false,
  threshold: 0,
  maxLevel: 0,
  samples: [],
  interval: null,
};

// Initialize the calibration system
export function setupCalibration() {
  // Add custom event listeners beyond what's in ui.js
  const startCalibrationBtn = document.getElementById("start-calibration-btn");

  if (startCalibrationBtn) {
    startCalibrationBtn.addEventListener("click", () => {
      if (!calibrationState.isCalibrating) {
        startCalibration();
      }
    });
  }
}

// Start the calibration process
function startCalibration() {
  calibrationState.isCalibrating = true;
  calibrationState.samples = [];
  calibrationState.maxLevel = 0;

  // Reset the UI
  const calibrationMeterFill = document.getElementById(
    "calibration-meter-fill"
  );
  const calibrationStatus = document.getElementById("calibration-status");

  if (calibrationMeterFill) {
    calibrationMeterFill.style.width = "0%";
  }

  if (calibrationStatus) {
    calibrationStatus.textContent =
      "Calibrating... please sing or hum a steady note.";
  }

  // Start the audio analysis
  startAudioAnalysis();

  // Start collecting samples
  collectSamples();
}

// Start audio analysis for calibration
function startAudioAnalysis() {
  // In a real application, this would start the audio input and analysis
  // For demonstration, we'll simulate audio input
  simulateAudioInput();
}

// Collect audio samples
function collectSamples() {
  // Sample collection timer - collect for 3 seconds
  setTimeout(() => {
    // End the calibration process
    finishCalibration();
  }, 3000);

  // Collect samples at intervals
  calibrationState.interval = setInterval(() => {
    // Get the current audio level
    const level = appState.audioLevel;

    // Add to our samples
    calibrationState.samples.push(level);

    // Update the max level
    if (level > calibrationState.maxLevel) {
      calibrationState.maxLevel = level;
    }

    // Update the UI
    updateCalibrationUI(level);
  }, 50);
}

// Update the calibration UI
function updateCalibrationUI(level) {
  const calibrationMeterFill = document.getElementById(
    "calibration-meter-fill"
  );

  if (calibrationMeterFill) {
    calibrationMeterFill.style.width = `${level * 100}%`;
  }
}

// Finish the calibration process
function finishCalibration() {
  // Stop collecting samples
  if (calibrationState.interval) {
    clearInterval(calibrationState.interval);
    calibrationState.interval = null;
  }

  // Calculate the threshold
  calculateThreshold();

  // Update UI
  const calibrationStatus = document.getElementById("calibration-status");

  if (calibrationStatus) {
    calibrationStatus.textContent = "Calibration complete!";
  }

  // Apply the calibration settings
  applyCalibration();

  // Reset calibration state
  calibrationState.isCalibrating = false;
}

// Calculate the threshold from collected samples
function calculateThreshold() {
  if (calibrationState.samples.length === 0) {
    calibrationState.threshold = 0.1; // Default threshold
    return;
  }

  // Sort samples
  const sortedSamples = [...calibrationState.samples].sort((a, b) => a - b);

  // Remove the lowest and highest 10% of samples
  const trimStart = Math.floor(sortedSamples.length * 0.1);
  const trimEnd = Math.floor(sortedSamples.length * 0.9);
  const trimmedSamples = sortedSamples.slice(trimStart, trimEnd);

  // Calculate average
  const sum = trimmedSamples.reduce((acc, val) => acc + val, 0);
  const avg = sum / trimmedSamples.length;

  // Set threshold to 50% of the average level
  calibrationState.threshold = avg * 0.5;

  console.log("Calibration threshold calculated:", calibrationState.threshold);
}

// Apply the calibration settings
function applyCalibration() {
  // In a real application, this would send the threshold to the backend
  // For demonstration, we'll just log it
  console.log(
    `Applying calibration with threshold: ${calibrationState.threshold}`
  );

  // This would typically be an API call:
  // window.api.setInputThreshold(calibrationState.threshold);
}

// Simulate audio input for demonstration
function simulateAudioInput() {
  // This is just a simulation - in a real app, we'd use the microphone
  let time = 0;
  const simulationInterval = setInterval(() => {
    time += 0.05;

    // Generate a simulated audio level
    // Start quiet, then get louder, then stabilize
    let level = 0;

    if (time < 0.5) {
      // Ramp up
      level = time * 0.8;
    } else if (time < 1.0) {
      // Peak
      level = 0.4 + Math.sin(time * 10) * 0.1;
    } else {
      // Stable with slight variations
      level = 0.6 + Math.sin(time * 5) * 0.1;
    }

    // Add some random noise
    level += (Math.random() - 0.5) * 0.1;

    // Clamp between 0 and 1
    level = Math.max(0, Math.min(1, level));

    // Update app state
    appState.audioLevel = level;

    // Stop after 3 seconds
    if (time > 3) {
      clearInterval(simulationInterval);
    }
  }, 50);
}
