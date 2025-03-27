// UI initialization module
import { appState } from "./app.js";

// Initialize the UI components
export function initUI(state) {
  // Set up theme based on user settings
  applyTheme(state.settings.theme);

  // Set up theme switcher
  const themeSelect = document.getElementById("theme-select");
  if (themeSelect) {
    themeSelect.addEventListener("change", () => {
      const theme = themeSelect.value;
      applyTheme(theme);
      state.settings.theme = theme;
    });
  }

  // Initialize settings dialog
  initSettingsDialog();

  // Initialize calibration dialog
  initCalibrationDialog();

  // Set up custom scale selector
  initCustomScaleSelector();
}

// Apply the selected theme
function applyTheme(theme) {
  document.body.className = theme === "light" ? "light-theme" : "dark-theme";

  // Update theme-specific icon colors
  updateIconColors(theme);
}

// Update icon colors based on theme
function updateIconColors(theme) {
  const isDark = theme === "dark";
  const iconColor = isDark ? "%23ffffff" : "%23333333";

  // CSS variable approach would be better, but this is a simple solution
  document.querySelectorAll(".icon").forEach((icon) => {
    // Get the current background image URL
    const bgImage = window.getComputedStyle(icon).backgroundImage;

    // Replace the color in the SVG fill parameter
    if (bgImage.includes("svg")) {
      const newBgImage = bgImage.replace(
        /fill='%23[0-9a-f]{6}'/i,
        `fill='${iconColor}'`
      );
      icon.style.backgroundImage = newBgImage;
    }
  });
}

// Initialize settings dialog
function initSettingsDialog() {
  const settingsDialog = document.getElementById("settings-dialog");
  const closeSettingsBtn = document.getElementById("close-settings-btn");
  const saveSettingsBtn = document.getElementById("save-settings-btn");

  if (!settingsDialog || !closeSettingsBtn || !saveSettingsBtn) {
    console.error("Settings dialog elements not found");
    return;
  }

  // Close dialog on cancel button click
  closeSettingsBtn.addEventListener("click", () => {
    settingsDialog.classList.add("hidden");
  });

  // Save settings and close dialog
  saveSettingsBtn.addEventListener("click", () => {
    // Collect settings from form elements
    const settings = {
      theme: document.getElementById("theme-select").value,
      bufferSize: parseInt(
        document.getElementById("buffer-size-select").value,
        10
      ),
      pitchBend: document.getElementById("pitch-bend-toggle").checked,
    };

    // Update app state with new settings
    Object.assign(appState.settings, settings);

    // Save settings via API
    window.api
      .saveSettings(settings)
      .then(() => {
        console.log("Settings saved");
        settingsDialog.classList.add("hidden");
      })
      .catch((error) => {
        console.error("Error saving settings:", error);
      });
  });

  // Close dialog when clicking outside of it
  settingsDialog.addEventListener("click", (event) => {
    if (event.target === settingsDialog) {
      settingsDialog.classList.add("hidden");
    }
  });
}

// Initialize calibration dialog
function initCalibrationDialog() {
  const calibrationDialog = document.getElementById("calibration-dialog");
  const startCalibrationBtn = document.getElementById("start-calibration-btn");
  const closeCalibrationBtn = document.getElementById("close-calibration-btn");

  if (!calibrationDialog || !startCalibrationBtn || !closeCalibrationBtn) {
    console.error("Calibration dialog elements not found");
    return;
  }

  // Close dialog on cancel button click
  closeCalibrationBtn.addEventListener("click", () => {
    calibrationDialog.classList.add("hidden");
  });

  // Start calibration process
  startCalibrationBtn.addEventListener("click", async () => {
    // Update UI to show calibration in progress
    startCalibrationBtn.disabled = true;
    closeCalibrationBtn.disabled = true;

    const calibrationStatus = document.getElementById("calibration-status");
    const calibrationMeterFill = document.getElementById(
      "calibration-meter-fill"
    );

    if (calibrationStatus) {
      calibrationStatus.textContent =
        "Calibrating... please sing or hum a steady note.";
    }

    try {
      // Simulate a calibration process with progress updates
      await simulateCalibration((progress) => {
        if (calibrationMeterFill) {
          calibrationMeterFill.style.width = `${progress}%`;
        }
      });

      if (calibrationStatus) {
        calibrationStatus.textContent = "Calibration complete!";
      }

      // In a real application, we would call the API to perform calibration
      // await window.api.calibrateMicrophone();

      // Close the dialog after a delay
      setTimeout(() => {
        calibrationDialog.classList.add("hidden");

        // Reset the UI
        startCalibrationBtn.disabled = false;
        closeCalibrationBtn.disabled = false;

        if (calibrationStatus) {
          calibrationStatus.textContent = "Ready to calibrate...";
        }

        if (calibrationMeterFill) {
          calibrationMeterFill.style.width = "0%";
        }
      }, 1500);
    } catch (error) {
      console.error("Calibration error:", error);

      if (calibrationStatus) {
        calibrationStatus.textContent = "Calibration failed. Please try again.";
      }

      // Reset the UI
      startCalibrationBtn.disabled = false;
      closeCalibrationBtn.disabled = false;
    }
  });

  // Close dialog when clicking outside of it
  calibrationDialog.addEventListener("click", (event) => {
    if (event.target === calibrationDialog) {
      calibrationDialog.classList.add("hidden");
    }
  });
}

// Simulate a calibration process for demonstration
async function simulateCalibration(progressCallback) {
  let progress = 0;

  return new Promise((resolve) => {
    const interval = setInterval(() => {
      progress += 5;
      progressCallback(progress);

      if (progress >= 100) {
        clearInterval(interval);
        resolve();
      }
    }, 100);
  });
}

// Initialize the custom scale selector
function initCustomScaleSelector() {
  const scaleSelect = document.getElementById("scale-select");
  const customScaleSelector = document.getElementById("custom-scale-selector");

  if (!scaleSelect || !customScaleSelector) {
    return;
  }

  // Show/hide custom scale selector based on selection
  scaleSelect.addEventListener("change", () => {
    const isCustom = scaleSelect.value === "custom";
    customScaleSelector.classList.toggle("hidden", !isCustom);

    // Generate note checkboxes if needed
    if (isCustom && customScaleSelector.children.length === 0) {
      generateNoteCheckboxes(customScaleSelector);
    }
  });
}

// Generate checkboxes for custom scale selection
function generateNoteCheckboxes(container) {
  const noteNames = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
  ];

  // Create a container for the checkboxes
  const noteContainer = document.createElement("div");
  noteContainer.className = "note-checkbox-container";

  // Create a checkbox for each note
  noteNames.forEach((note) => {
    const noteLabel = document.createElement("label");
    noteLabel.className = "note-checkbox-label";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "note-checkbox";
    checkbox.checked = true; // Default to all notes selected
    checkbox.dataset.note = note;

    noteLabel.appendChild(checkbox);
    noteLabel.appendChild(document.createTextNode(note));

    noteContainer.appendChild(noteLabel);
  });

  // Add the note checkboxes to the container
  container.appendChild(noteContainer);

  // Add a helper message
  const helperText = document.createElement("div");
  helperText.className = "helper-text";
  helperText.textContent = "Select the notes to include in your custom scale.";
  container.appendChild(helperText);
}
