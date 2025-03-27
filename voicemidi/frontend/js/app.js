// Main application script for VoiceMIDI
import { initUI } from "./ui.js";
import { setupKeyboard } from "./keyboard.js";
import { setupAudioVisualizer, updateVisualizer } from "./visualizer.js";
import { setupSettings } from "./settings.js";
import { setupCalibration } from "./calibration.js";

// Application state
const appState = {
  isRunning: false,
  audioDevices: [],
  midiDevices: [],
  selectedAudioDevice: null,
  selectedMidiDevice: null,
  audioLevel: 0,
  currentNote: null,
  currentFrequency: 0,
  settings: {
    scale: "chromatic",
    keyCenter: "C",
    pitchCorrection: 0.5,
    noteDelay: 100,
    velocitySensitivity: 0.8,
    fixedVelocity: false,
    fixedVelocityValue: 100,
    midiChannel: 1,
    bufferSize: 1024,
    pitchBend: true,
    theme: "dark",
  },
};

// Initialize the application when the DOM is loaded
document.addEventListener("DOMContentLoaded", async () => {
  console.log("Initializing VoiceMIDI...");

  // Set up UI components
  initUI(appState);
  setupKeyboard(appState);
  setupAudioVisualizer(appState);
  setupSettings(appState);
  setupCalibration(appState);

  // Set up event listeners
  setupEventListeners();

  // Load settings from Electron store
  await loadSettings();

  // Initialize device lists
  await refreshDeviceLists();

  console.log("VoiceMIDI initialized!");
});

// Set up application event listeners
function setupEventListeners() {
  // Start/Stop button
  const startButton = document.getElementById("btn-start");
  startButton.addEventListener("click", toggleAnalysis);

  // Calibrate button
  const calibrateButton = document.getElementById("btn-calibrate");
  calibrateButton.addEventListener("click", showCalibrationDialog);

  // Settings button
  const settingsButton = document.getElementById("btn-settings");
  settingsButton.addEventListener("click", showSettingsDialog);

  // Audio device refresh button
  const refreshAudioButton = document.getElementById("refresh-audio-btn");
  refreshAudioButton.addEventListener("click", async () => {
    await refreshAudioDevices();
  });

  // MIDI device refresh button
  const refreshMidiButton = document.getElementById("refresh-midi-btn");
  refreshMidiButton.addEventListener("click", async () => {
    await refreshMidiDevices();
  });

  // Audio device selection
  const audioDeviceSelect = document.getElementById("audio-device-select");
  audioDeviceSelect.addEventListener("change", () => {
    const deviceId = audioDeviceSelect.value;
    setAudioDevice(deviceId);
  });

  // MIDI device selection
  const midiPortSelect = document.getElementById("midi-port-select");
  midiPortSelect.addEventListener("change", () => {
    const portId = midiPortSelect.value;
    setMidiDevice(portId);
  });

  // Scale and key selection
  const scaleSelect = document.getElementById("scale-select");
  const keySelect = document.getElementById("key-select");

  scaleSelect.addEventListener("change", () => {
    appState.settings.scale = scaleSelect.value;
    updateScaleSettings();
  });

  keySelect.addEventListener("change", () => {
    appState.settings.keyCenter = keySelect.value;
    updateScaleSettings();
  });

  // Sliders
  setupSliderControl(
    "pitch-correction-slider",
    "pitch-correction-value",
    (value) => {
      appState.settings.pitchCorrection = value;
      return Math.round(value * 100) + "%";
    }
  );

  setupSliderControl("note-delay-slider", "note-delay-value", (value) => {
    appState.settings.noteDelay = value;
    return value + "ms";
  });

  setupSliderControl(
    "velocity-sensitivity-slider",
    "velocity-sensitivity-value",
    (value) => {
      appState.settings.velocitySensitivity = value;
      return Math.round(value * 100) + "%";
    }
  );

  setupSliderControl(
    "fixed-velocity-slider",
    "fixed-velocity-value",
    (value) => {
      appState.settings.fixedVelocityValue = value;
      return value.toString();
    }
  );

  // Fixed velocity toggle
  const fixedVelocityToggle = document.getElementById("fixed-velocity-toggle");
  const fixedVelocityControl = document.getElementById(
    "fixed-velocity-control"
  );

  fixedVelocityToggle.addEventListener("change", () => {
    appState.settings.fixedVelocity = fixedVelocityToggle.checked;
    fixedVelocityControl.classList.toggle(
      "hidden",
      !fixedVelocityToggle.checked
    );
  });

  // MIDI Channel selection
  const midiChannelSelect = document.getElementById("midi-channel-select");
  midiChannelSelect.addEventListener("change", () => {
    appState.settings.midiChannel = parseInt(midiChannelSelect.value, 10);
  });

  // Listen for API events
  window.api.on("audio-level", (level) => {
    appState.audioLevel = level;
    updateAudioLevel(level);
  });

  window.api.on("pitch-detected", (data) => {
    appState.currentNote = data.note;
    appState.currentFrequency = data.frequency;
    updateNoteDisplay(data.note, data.frequency);
  });

  window.api.on("midi-message", (data) => {
    if (data.type === "note-on") {
      updateKeyboardDisplay(data.note, true, data.velocity);
    } else if (data.type === "note-off") {
      updateKeyboardDisplay(data.note, false, 0);
    }
  });
}

// Helper for setting up slider controls
function setupSliderControl(sliderId, valueId, valueFormatter) {
  const slider = document.getElementById(sliderId);
  const valueDisplay = document.getElementById(valueId);

  slider.addEventListener("input", () => {
    const value = parseFloat(slider.value);
    valueDisplay.textContent = valueFormatter(value);
  });
}

// Toggle audio analysis (start/stop)
async function toggleAnalysis() {
  const startButton = document.getElementById("btn-start");
  const startButtonText = startButton.querySelector("span:not(.icon)");
  const startButtonIcon = startButton.querySelector(".icon");

  if (appState.isRunning) {
    // Stop analysis
    try {
      await window.api.stopAnalysis();
      appState.isRunning = false;
      startButtonText.textContent = "Start";
      startButtonIcon.classList.remove("icon-stop");
      startButtonIcon.classList.add("icon-play");

      updateStatusIndicator("audio", false);
    } catch (error) {
      console.error("Error stopping analysis:", error);
    }
  } else {
    // Start analysis
    try {
      await window.api.startAnalysis();
      appState.isRunning = true;
      startButtonText.textContent = "Stop";
      startButtonIcon.classList.remove("icon-play");
      startButtonIcon.classList.add("icon-stop");

      updateStatusIndicator("audio", true);
    } catch (error) {
      console.error("Error starting analysis:", error);
    }
  }
}

// Refresh audio and MIDI device lists
async function refreshDeviceLists() {
  await refreshAudioDevices();
  await refreshMidiDevices();
}

// Refresh audio device list
async function refreshAudioDevices() {
  try {
    const devices = await window.api.listAudioDevices();
    appState.audioDevices = devices;

    const audioDeviceSelect = document.getElementById("audio-device-select");
    audioDeviceSelect.innerHTML = "";

    if (devices.length === 0) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "No microphones available";
      audioDeviceSelect.appendChild(option);
    } else {
      devices.forEach((device) => {
        const option = document.createElement("option");
        option.value = device.id;
        option.textContent = device.name;
        if (appState.selectedAudioDevice === device.id) {
          option.selected = true;
        }
        audioDeviceSelect.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Error refreshing audio devices:", error);
  }
}

// Refresh MIDI device list
async function refreshMidiDevices() {
  try {
    const devices = await window.api.listMidiDevices();
    appState.midiDevices = devices;

    const midiPortSelect = document.getElementById("midi-port-select");
    midiPortSelect.innerHTML = "";

    if (devices.length === 0) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "No MIDI ports available";
      midiPortSelect.appendChild(option);
    } else {
      devices.forEach((device) => {
        const option = document.createElement("option");
        option.value = device.id;
        option.textContent = device.name;
        if (appState.selectedMidiDevice === device.id) {
          option.selected = true;
        }
        midiPortSelect.appendChild(option);
      });
    }

    updateStatusIndicator("midi", devices.length > 0);
  } catch (error) {
    console.error("Error refreshing MIDI devices:", error);
  }
}

// Set audio device
async function setAudioDevice(deviceId) {
  if (!deviceId) return;

  try {
    await window.api.setAudioDevice(deviceId);
    appState.selectedAudioDevice = deviceId;
    console.log(`Audio device set to: ${deviceId}`);
  } catch (error) {
    console.error("Error setting audio device:", error);
  }
}

// Set MIDI device
async function setMidiDevice(deviceId) {
  if (!deviceId) return;

  try {
    await window.api.setMidiDevice(deviceId);
    appState.selectedMidiDevice = deviceId;
    console.log(`MIDI device set to: ${deviceId}`);
    updateStatusIndicator("midi", true);
  } catch (error) {
    console.error("Error setting MIDI device:", error);
    updateStatusIndicator("midi", false);
  }
}

// Update scale settings
async function updateScaleSettings() {
  try {
    await window.api.setScale(
      appState.settings.scale,
      appState.settings.keyCenter
    );
    console.log(
      `Scale set to: ${appState.settings.keyCenter} ${appState.settings.scale}`
    );
  } catch (error) {
    console.error("Error setting scale:", error);
  }
}

// Show calibration dialog
function showCalibrationDialog() {
  const dialog = document.getElementById("calibration-dialog");
  dialog.classList.remove("hidden");
}

// Show settings dialog
function showSettingsDialog() {
  const dialog = document.getElementById("settings-dialog");
  dialog.classList.remove("hidden");
}

// Update audio level display
function updateAudioLevel(level) {
  const audioLevelMeter = document.getElementById("audio-level-meter");
  audioLevelMeter.style.width = `${level * 100}%`;
}

// Update note display
function updateNoteDisplay(note, frequency) {
  const noteDisplay = document.getElementById("note-display");
  const frequencyDisplay = document.getElementById("frequency-display");

  noteDisplay.textContent = note || "--";
  frequencyDisplay.textContent = frequency
    ? `${Math.round(frequency)} Hz`
    : "0 Hz";
}

// Update keyboard display to show active notes
function updateKeyboardDisplay(midiNote, isActive, velocity) {
  const keyElement = document.querySelector(
    `.piano-key[data-midi="${midiNote}"]`
  );
  if (keyElement) {
    if (isActive) {
      keyElement.classList.add("key-active");
      // You could also adjust the opacity based on velocity
      keyElement.style.opacity = 0.5 + velocity / 254;
    } else {
      keyElement.classList.remove("key-active");
      keyElement.style.opacity = "";
    }
  }
}

// Update status indicators
function updateStatusIndicator(type, isActive) {
  if (type === "audio") {
    const audioStatusIcon = document.querySelector(".audio-status-icon");
    const audioStatusText = document.querySelector(
      "#audio-status .status-text"
    );

    audioStatusIcon.classList.toggle("active", isActive);
    audioStatusText.textContent = `Audio: ${isActive ? "Active" : "Inactive"}`;
  } else if (type === "midi") {
    const midiStatusIcon = document.querySelector(".midi-status-icon");
    const midiStatusText = document.querySelector("#midi-status .status-text");

    midiStatusIcon.classList.toggle("connected", isActive);
    midiStatusText.textContent = `MIDI: ${
      isActive ? "Connected" : "Disconnected"
    }`;
  }
}

// Load settings from Electron store
async function loadSettings() {
  try {
    const savedSettings = await window.api.getSettings();

    // Update app state with saved settings
    if (savedSettings) {
      // Merge saved settings with defaults
      Object.assign(appState.settings, savedSettings);

      // Update UI to reflect loaded settings
      updateUIFromSettings();
    }
  } catch (error) {
    console.error("Error loading settings:", error);
  }
}

// Update UI elements to match loaded settings
function updateUIFromSettings() {
  const {
    scale,
    keyCenter,
    pitchCorrection,
    noteDelay,
    velocitySensitivity,
    fixedVelocity,
    fixedVelocityValue,
    midiChannel,
    bufferSize,
    pitchBend,
    theme,
  } = appState.settings;

  // Set select elements
  setSelectValue("scale-select", scale);
  setSelectValue("key-select", keyCenter);
  setSelectValue("midi-channel-select", midiChannel.toString());
  setSelectValue("buffer-size-select", bufferSize.toString());

  // Set range sliders
  setRangeValue(
    "pitch-correction-slider",
    "pitch-correction-value",
    pitchCorrection,
    (val) => `${Math.round(val * 100)}%`
  );
  setRangeValue(
    "note-delay-slider",
    "note-delay-value",
    noteDelay,
    (val) => `${val}ms`
  );
  setRangeValue(
    "velocity-sensitivity-slider",
    "velocity-sensitivity-value",
    velocitySensitivity,
    (val) => `${Math.round(val * 100)}%`
  );
  setRangeValue(
    "fixed-velocity-slider",
    "fixed-velocity-value",
    fixedVelocityValue,
    (val) => val.toString()
  );

  // Set toggles
  setToggleValue("fixed-velocity-toggle", fixedVelocity);
  setToggleValue("pitch-bend-toggle", pitchBend);

  // Toggle dependent elements
  document
    .getElementById("fixed-velocity-control")
    .classList.toggle("hidden", !fixedVelocity);

  // Set theme
  setSelectValue("theme-select", theme);
  document.body.className = `${theme}-theme`;
}

// Helper to set select element value
function setSelectValue(elementId, value) {
  const element = document.getElementById(elementId);
  if (element) {
    element.value = value;
  }
}

// Helper to set range slider value
function setRangeValue(sliderId, valueId, value, formatter) {
  const slider = document.getElementById(sliderId);
  const valueDisplay = document.getElementById(valueId);

  if (slider && valueDisplay) {
    slider.value = value;
    valueDisplay.textContent = formatter(value);
  }
}

// Helper to set toggle value
function setToggleValue(elementId, value) {
  const element = document.getElementById(elementId);
  if (element) {
    element.checked = value;
  }
}

// Export app state and functions that might be needed by other modules
export { appState, updateAudioLevel, updateNoteDisplay, updateKeyboardDisplay };
