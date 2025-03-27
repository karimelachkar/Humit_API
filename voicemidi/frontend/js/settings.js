// Settings management module
import { appState } from "./app.js";

// Initialize the settings functionality
export function setupSettings() {
  // Set up the interface elements that weren't handled in ui.js
  setupAdvancedSettings();

  // Apply current settings to all components
  applySettings(appState.settings);
}

// Set up advanced settings
function setupAdvancedSettings() {
  // Buffer size setting
  const bufferSizeSelect = document.getElementById("buffer-size-select");
  if (bufferSizeSelect) {
    bufferSizeSelect.addEventListener("change", () => {
      const bufferSize = parseInt(bufferSizeSelect.value, 10);
      appState.settings.bufferSize = bufferSize;
    });
  }

  // Pitch bend toggle
  const pitchBendToggle = document.getElementById("pitch-bend-toggle");
  if (pitchBendToggle) {
    pitchBendToggle.addEventListener("change", () => {
      appState.settings.pitchBend = pitchBendToggle.checked;
    });
  }
}

// Apply settings to the UI and functionality
function applySettings(settings) {
  // Apply each setting
  if (settings.bufferSize) {
    applyBufferSize(settings.bufferSize);
  }

  if (settings.theme) {
    applyTheme(settings.theme);
  }

  // Log the applied settings
  console.log("Applied settings:", settings);
}

// Apply buffer size setting
function applyBufferSize(bufferSize) {
  // In a real app, we'd communicate with the audio engine
  console.log(`Setting buffer size to ${bufferSize}`);

  // This would typically be an API call:
  // window.api.setBufferSize(bufferSize);
}

// Apply theme setting
function applyTheme(theme) {
  document.body.className = theme === "light" ? "light-theme" : "dark-theme";

  // Set the theme select value
  const themeSelect = document.getElementById("theme-select");
  if (themeSelect) {
    themeSelect.value = theme;
  }
}

// Save all current settings
export async function saveSettings() {
  try {
    const result = await window.api.saveSettings(appState.settings);
    console.log("Settings saved:", result);
    return result;
  } catch (error) {
    console.error("Error saving settings:", error);
    throw error;
  }
}

// Load settings from storage
export async function loadSettings() {
  try {
    const settings = await window.api.getSettings();
    if (settings) {
      // Update app state with loaded settings
      Object.assign(appState.settings, settings);

      // Apply the loaded settings
      applySettings(appState.settings);
    }
    return settings;
  } catch (error) {
    console.error("Error loading settings:", error);
    throw error;
  }
}

// Reset settings to defaults
export async function resetSettings() {
  // Default settings
  const defaultSettings = {
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
  };

  // Update app state with default settings
  Object.assign(appState.settings, defaultSettings);

  // Apply the default settings
  applySettings(appState.settings);

  // Save the default settings
  try {
    const result = await saveSettings();
    console.log("Settings reset to defaults:", result);
    return result;
  } catch (error) {
    console.error("Error resetting settings:", error);
    throw error;
  }
}
