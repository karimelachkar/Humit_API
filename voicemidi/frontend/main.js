const { app, BrowserWindow, ipcMain, Menu } = require("electron");
const path = require("path");
const log = require("electron-log");
const Store = require("electron-store");

// Initialize the settings store
const store = new Store({
  defaults: {
    windowBounds: { width: 1000, height: 700 },
    audioDevice: null,
    midiPort: null,
    scale: "chromatic",
    keyCenter: "C",
    velocitySensitivity: 0.8,
    pitchCorrection: 0.5,
    theme: "dark",
  },
});

let mainWindow;

function createWindow() {
  const { width, height } = store.get("windowBounds");

  // Create the browser window
  mainWindow = new BrowserWindow({
    width,
    height,
    minWidth: 800,
    minHeight: 600,
    title: "VoiceMIDI",
    backgroundColor: "#2e2c29",
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  // Load the index.html file
  mainWindow.loadFile(path.join(__dirname, "index.html"));

  // Save window size when resized
  mainWindow.on("resize", () => {
    const { width, height } = mainWindow.getBounds();
    store.set("windowBounds", { width, height });
  });

  // Open DevTools in development
  if (process.env.NODE_ENV === "development") {
    mainWindow.webContents.openDevTools();
  }

  // Build the application menu
  const template = [
    {
      label: "File",
      submenu: [
        {
          label: "Settings",
          click: () => mainWindow.webContents.send("open-settings"),
        },
        { type: "separator" },
        { role: "quit" },
      ],
    },
    {
      label: "Device",
      submenu: [
        {
          label: "Audio Input",
          click: () => mainWindow.webContents.send("open-audio-devices"),
        },
        {
          label: "MIDI Output",
          click: () => mainWindow.webContents.send("open-midi-devices"),
        },
      ],
    },
    {
      label: "View",
      submenu: [
        { role: "reload" },
        { role: "forceReload" },
        { role: "toggleDevTools" },
        { type: "separator" },
        { role: "resetZoom" },
        { role: "zoomIn" },
        { role: "zoomOut" },
        { type: "separator" },
        { role: "togglefullscreen" },
      ],
    },
    {
      label: "Help",
      submenu: [
        {
          label: "About",
          click: () => mainWindow.webContents.send("open-about"),
        },
        {
          label: "Documentation",
          click: async () => {
            const { shell } = require("electron");
            await shell.openExternal(
              "https://github.com/yourusername/voice-to-midi/wiki"
            );
          },
        },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Create window when Electron is ready
app.whenReady().then(() => {
  createWindow();

  app.on("activate", function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit when all windows are closed, except on macOS
app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

// Handle IPC messages from renderer process
ipcMain.handle("get-settings", () => {
  return store.store;
});

ipcMain.handle("save-settings", (event, settings) => {
  Object.keys(settings).forEach((key) => {
    store.set(key, settings[key]);
  });
  return true;
});

// Log startup
log.info("App starting...");
