const { contextBridge, ipcRenderer } = require("electron");

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld("api", {
  // Settings
  getSettings: () => ipcRenderer.invoke("get-settings"),
  saveSettings: (settings) => ipcRenderer.invoke("save-settings", settings),

  // Event listeners
  on: (channel, callback) => {
    const validChannels = [
      "open-settings",
      "open-audio-devices",
      "open-midi-devices",
      "open-about",
      "midi-message",
      "audio-level",
      "pitch-detected",
    ];
    if (validChannels.includes(channel)) {
      // Deliberately strip event as it includes `sender`
      ipcRenderer.on(channel, (event, ...args) => callback(...args));
    }
  },

  // Python backend communication
  startAnalysis: () => ipcRenderer.invoke("start-analysis"),
  stopAnalysis: () => ipcRenderer.invoke("stop-analysis"),
  listAudioDevices: () => ipcRenderer.invoke("list-audio-devices"),
  listMidiDevices: () => ipcRenderer.invoke("list-midi-devices"),
  setAudioDevice: (deviceId) =>
    ipcRenderer.invoke("set-audio-device", deviceId),
  setMidiDevice: (deviceId) => ipcRenderer.invoke("set-midi-device", deviceId),
  calibrateMicrophone: () => ipcRenderer.invoke("calibrate-microphone"),
  setScale: (scale, keyCenter) =>
    ipcRenderer.invoke("set-scale", scale, keyCenter),
  setVelocitySensitivity: (sensitivity) =>
    ipcRenderer.invoke("set-velocity-sensitivity", sensitivity),
  setPitchCorrection: (amount) =>
    ipcRenderer.invoke("set-pitch-correction", amount),
});
