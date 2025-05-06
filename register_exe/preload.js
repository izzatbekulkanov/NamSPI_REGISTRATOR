// === preload.js ===
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getPrinters: () => ipcRenderer.invoke('get-printers'),
  getSavedPrinter: () => ipcRenderer.invoke('get-saved-printer'),
  saveSelectedPrinter: (printerName) => ipcRenderer.invoke('save-selected-printer', printerName),
  printTicket: (html, options) => ipcRenderer.invoke('print-ticket', html, options), // options qo‘shildi
  onShowPrinterModal: (callback) => ipcRenderer.on('show-printer-modal', callback),
  logToFile: (message, level) => ipcRenderer.invoke('log-to-file', message, level),
});