// Keyboard visualization module
import { appState } from "./app.js";

// Note data for generating the keyboard
const NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const MIDI_OFFSET = 21; // MIDI note number for A0
const START_OCTAVE = 2;
const END_OCTAVE = 6;

// Initialize the keyboard
export function setupKeyboard() {
  const keyboardContainer = document.getElementById("piano-keyboard");
  if (!keyboardContainer) {
    console.error("Piano keyboard container not found");
    return;
  }

  // Clear any existing keys
  keyboardContainer.innerHTML = "";

  // Generate the keyboard
  generateKeyboard(keyboardContainer, START_OCTAVE, END_OCTAVE);

  // Add event listeners for keyboard interaction
  setupKeyboardEvents(keyboardContainer);
}

// Generate the keyboard layout
function generateKeyboard(container, startOctave, endOctave) {
  // Create key elements for each octave
  for (let octave = startOctave; octave <= endOctave; octave++) {
    for (let i = 0; i < NOTES.length; i++) {
      const note = NOTES[i];
      const isBlack = note.includes("#");
      const midiNote = octave * 12 + i + MIDI_OFFSET;

      // Create the key element
      const keyElement = document.createElement("div");
      keyElement.className = `piano-key ${isBlack ? "black-key" : "white-key"}`;
      keyElement.dataset.note = note;
      keyElement.dataset.octave = octave;
      keyElement.dataset.midi = midiNote;

      // Add a label for certain keys (C, middle C, etc.)
      if (!isBlack && (note === "C" || note === "F")) {
        const keyLabel = document.createElement("div");
        keyLabel.className = "key-label";
        keyLabel.textContent = `${note}${octave}`;
        keyElement.appendChild(keyLabel);

        // Add special class for C keys
        if (note === "C") {
          keyElement.classList.add("key-c");
        }
      }

      // Add the key to the container
      container.appendChild(keyElement);
    }

    // Add an octave marker
    if (octave < endOctave) {
      const markerElement = document.createElement("div");
      markerElement.className = "octave-marker";
      markerElement.textContent = `C${octave + 1}`;
      markerElement.style.left = `${container.childElementCount * 40 - 20}px`;
      container.appendChild(markerElement);
    }
  }
}

// Set up event listeners for keyboard interaction
function setupKeyboardEvents(container) {
  // MIDI notes can be played by clicking keys
  container.addEventListener("mousedown", (event) => {
    const keyElement = event.target.closest(".piano-key");
    if (!keyElement) return;

    const midiNote = parseInt(keyElement.dataset.midi, 10);
    const note = keyElement.dataset.note;
    const octave = parseInt(keyElement.dataset.octave, 10);

    // Simulate note on event
    noteOn(midiNote, 100); // Default velocity of 100

    // Visually activate the key
    keyElement.classList.add("key-active");
  });

  // Stop playing when the mouse is released
  container.addEventListener("mouseup", (event) => {
    const keyElement = event.target.closest(".piano-key");
    if (!keyElement) return;

    const midiNote = parseInt(keyElement.dataset.midi, 10);

    // Simulate note off event
    noteOff(midiNote);

    // Visually deactivate the key
    keyElement.classList.remove("key-active");
  });

  // Handle mouse leaving the key
  container.addEventListener("mouseleave", (event) => {
    const keyElement = event.target.closest(".piano-key");
    if (!keyElement) return;

    const midiNote = parseInt(keyElement.dataset.midi, 10);

    // Simulate note off event
    noteOff(midiNote);

    // Visually deactivate the key
    keyElement.classList.remove("key-active");
  });
}

// Send MIDI note on message
function noteOn(midiNote, velocity) {
  // This would typically communicate with the backend
  console.log(`Note On: ${midiNote} with velocity ${velocity}`);

  // If we were connected to the backend, we would do something like:
  // window.api.sendMidiMessage({ type: 'note-on', note: midiNote, velocity: velocity });
}

// Send MIDI note off message
function noteOff(midiNote) {
  // This would typically communicate with the backend
  console.log(`Note Off: ${midiNote}`);

  // If we were connected to the backend, we would do something like:
  // window.api.sendMidiMessage({ type: 'note-off', note: midiNote, velocity: 0 });
}

// Highlight a specific note and octave on the keyboard
export function highlightNote(note, octave) {
  const keyElement = document.querySelector(
    `.piano-key[data-note="${note}"][data-octave="${octave}"]`
  );
  if (keyElement) {
    keyElement.classList.add("key-active");
  }
}

// Remove highlight from a specific note and octave on the keyboard
export function unhighlightNote(note, octave) {
  const keyElement = document.querySelector(
    `.piano-key[data-note="${note}"][data-octave="${octave}"]`
  );
  if (keyElement) {
    keyElement.classList.remove("key-active");
  }
}

// Highlight a MIDI note on the keyboard
export function highlightMidiNote(midiNote) {
  const keyElement = document.querySelector(
    `.piano-key[data-midi="${midiNote}"]`
  );
  if (keyElement) {
    keyElement.classList.add("key-active");
  }
}

// Remove highlight from a MIDI note on the keyboard
export function unhighlightMidiNote(midiNote) {
  const keyElement = document.querySelector(
    `.piano-key[data-midi="${midiNote}"]`
  );
  if (keyElement) {
    keyElement.classList.remove("key-active");
  }
}

// Scroll to center the active note in view
export function scrollToNote(midiNote) {
  const keyElement = document.querySelector(
    `.piano-key[data-midi="${midiNote}"]`
  );
  if (!keyElement) return;

  const container = document.querySelector(".keyboard-visual");
  if (!container) return;

  const containerRect = container.getBoundingClientRect();
  const keyRect = keyElement.getBoundingClientRect();

  // Calculate the center position for the key
  const targetScrollLeft =
    keyElement.offsetLeft - containerRect.width / 2 + keyRect.width / 2;

  // Smooth scroll to the position
  container.scrollTo({
    left: targetScrollLeft,
    behavior: "smooth",
  });
}
