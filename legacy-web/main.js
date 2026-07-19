// Electron main process for Video Studio.
//
// The renderer is the exact same static app that runs in a browser
// (index.html + support.js + vendor/React + the _ds design system). This
// process just hosts it in a native window and wires up the two things the
// browser gives you for free but Electron does not: a handler for
// getDisplayMedia (screen capture) and media (microphone) permissions.

const { app, BrowserWindow, session, desktopCapturer, shell } = require('electron');
const path = require('node:path');

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 960,
    minHeight: 640,
    backgroundColor: '#f4f1e8',
    title: 'Video Studio',
    show: false,
    icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      // Screen capture + camera/mic live entirely in the renderer's own
      // web APIs; no Node access is exposed to page code.
      sandbox: false,
    },
  });

  mainWindow.loadFile('index.html');

  mainWindow.once('ready-to-show', () => mainWindow.show());

  // Open any external links (e.g. the React error-decoder URL) in the
  // user's real browser rather than inside the app window.
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('http://') || url.startsWith('https://')) {
      shell.openExternal(url);
      return { action: 'deny' };
    }
    return { action: 'allow' };
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Screen / window capture. Electron requires the app to service
// getDisplayMedia() itself. On platforms with a native picker (macOS 15+,
// Windows) we defer to it; everywhere else we grant the primary screen so
// "New recording" still produces a real capture.
function wireDisplayMedia() {
  session.defaultSession.setDisplayMediaRequestHandler(
    (request, callback) => {
      desktopCapturer
        .getSources({ types: ['screen', 'window'] })
        .then((sources) => {
          const screenSource =
            sources.find((s) => s.id.startsWith('screen:')) || sources[0];
          if (!screenSource) {
            // Nothing to capture — let the renderer fall back to its sample.
            callback({});
            return;
          }
          // 'loopback' pulls system audio on Windows; ignored elsewhere.
          callback({ video: screenSource, audio: 'loopback' });
        })
        .catch(() => callback({}));
    },
    // Prefer the OS picker when the platform provides one.
    { useSystemPicker: true }
  );

  // Grant microphone / camera prompts triggered by getUserMedia.
  session.defaultSession.setPermissionRequestHandler(
    (webContents, permission, callback) => {
      const allowed = ['media', 'display-capture', 'audioCapture', 'videoCapture'];
      callback(allowed.includes(permission));
    }
  );
}

app.whenReady().then(() => {
  wireDisplayMedia();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  // Standard behavior: stay resident on macOS, quit elsewhere.
  if (process.platform !== 'darwin') app.quit();
});
