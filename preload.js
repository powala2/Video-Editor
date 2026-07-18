// Preload runs before the renderer with contextIsolation enabled.
//
// Video Studio's renderer is a self-contained web app that needs no bridge
// into Node — screen capture, file import, playback, and download all use
// standard web APIs. This file is intentionally minimal; it exists so the
// window has a defined (empty) preload boundary and is the place to expose a
// vetted `window.videoStudio` API later if native features are added.

window.addEventListener('DOMContentLoaded', () => {
  // Marker so page code / debugging can tell it's running inside the shell.
  document.documentElement.setAttribute('data-runtime', 'electron');
});
