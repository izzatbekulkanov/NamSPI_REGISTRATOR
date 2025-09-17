const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getPrinters: () => ipcRenderer.invoke('get-printers'),
  getSavedPrinter: () => ipcRenderer.invoke('get-saved-printer'),
  saveSelectedPrinter: (printerName) => ipcRenderer.invoke('save-selected-printer', printerName),
  printTicket: (html, options) => ipcRenderer.invoke('print-ticket', html, options),
  onShowPrinterModal: (callback) => ipcRenderer.on('show-printer-modal', callback),
  onRefreshData: (callback) => ipcRenderer.on('refresh-data', callback),
  onReprintTicket: (callback) => ipcRenderer.on('reprint-ticket', callback), // Yangi
  onRestartApp: (callback) => ipcRenderer.on('restart-app', callback), // Yangi
  logToFile: (message, level) => ipcRenderer.invoke('log-to-file', message, level),
});