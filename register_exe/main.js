const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');
const fs = require('fs').promises;
const os = require('os');

const logFilePath = path.join(app.getPath('userData'), 'app.log');

async function logToFile(message, level = 'INFO') {
    const timestamp = new Date().toISOString();
    const logMessage = `${timestamp} [${level}] ${message}\n`;
    try {
        await fs.appendFile(logFilePath, logMessage);
        console.log(logMessage.trim());
    } catch (err) {
        console.error(`Failed to write to log file: ${err.message}`);
    }
}

app.whenReady().then(async () => {
    await logToFile('Ilova ishga tushmoqda');

    const userDataPath = path.join(app.getPath('userData'), 'CustomCache', 'namdpi-queue-app');
    const cachePath = path.join(app.getPath('userData'), 'CustomCache');
    app.setPath('userData', userDataPath);
    app.setPath('cache', cachePath);

    await logToFile(`Kesh yo‘li o‘zgartirildi: ${cachePath}`);
    await logToFile(`User Data Path: ${userDataPath}`);
    await logToFile(`Cache Path: ${cachePath}`);

    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            nodeIntegration: false,
        },
    });

    mainWindow.loadFile('index.html');
    await logToFile('Ilova oynasi va menyu yaratildi');

    const menu = Menu.buildFromTemplate([
        {
            label: 'Fayl',
            submenu: [
                {
                    label: 'Printer sozlamalari',
                    click: () => {
                        mainWindow.webContents.send('show-printer-modal');
                        logToFile('Printer tanlash oynasi ochildi');
                    },
                },
                { type: 'separator' },
                { role: 'quit', label: 'Chiqish' },
            ],
        },
    ]);
    Menu.setApplicationMenu(menu);

    await logToFile('Ilova muvaffaqiyatli ishga tushdi');

    ipcMain.handle('get-printers', async () => {
        try {
            const printers = await mainWindow.webContents.getPrintersAsync();
            await logToFile(`Printerlar ro‘yxati olindi: ${printers.map(p => p.name).join(', ')}`);
            return printers;
        } catch (err) {
            await logToFile(`Printerlarni olishda xato: ${err.message}`, 'ERROR');
            throw err;
        }
    });

    ipcMain.handle('get-saved-printer', async () => {
        try {
            const configPath = path.join(app.getPath('userData'), 'printer-config.json');
            const data = await fs.readFile(configPath, 'utf8');
            const config = JSON.parse(data);
            await logToFile(`Saqlangan printer so‘raldi: ${config.printerName || 'yo‘q'}`);
            return config.printerName;
        } catch (err) {
            await logToFile(`Saqlangan printerni olishda xato: ${err.message}`, 'ERROR');
            return null;
        }
    });

    ipcMain.handle('save-selected-printer', async (event, printerName) => {
        try {
            const configPath = path.join(app.getPath('userData'), 'printer-config.json');
            await fs.writeFile(configPath, JSON.stringify({ printerName }));
            await logToFile(`Tanlangan printer saqlandi: ${printerName}`);
            return true;
        } catch (err) {
            await logToFile(`Printerni saqlashda xato: ${err.message}`, 'ERROR');
            throw err;
        }
    });

    ipcMain.handle('print-ticket', async (event, html, options) => {
        try {
            await logToFile('print-ticket handler chaqirildi');
            const printer = await mainWindow.webContents.getPrintersAsync();
            const selectedPrinter = printer.find(p => p.name === (options.deviceName || ''));

            if (!selectedPrinter) {
                await logToFile(`Printer topilmadi: ${options.deviceName}`, 'ERROR');
                throw new Error(`Printer topilmadi: ${options.deviceName}`);
            }

            await logToFile(`Saqlangan printer: ${options.deviceName}`);

            // Alohida yashirin oynada HTML’ni chop etish
            const printWindow = new BrowserWindow({
                show: false, // Oynani ko‘rsatmaymiz
                webPreferences: {
                    nodeIntegration: false,
                    contextIsolation: true,
                },
            });

            // HTML’ni printWindow’da ko‘rsatish
            const htmlContent = `data:text/html;charset=UTF-8,${encodeURIComponent(html)}`;
            await printWindow.loadURL(htmlContent);
            await logToFile('Chop etish uchun HTML oynaga yuklandi');

            // Chop etish sozlamalari
            const printSettings = {
                silent: options.silent || true,
                deviceName: options.deviceName,
                pageSize: options.pageSize || { width: 58000, height: 80000 }, // Default: 58mm x 80mm
                margins: options.margins || { marginType: 'none' },
            };

            await logToFile(`Chop etish uchun sozlamalar: ${JSON.stringify(printSettings)}`);

            // Chop etish
            printWindow.webContents.print(printSettings, (success, errorType) => {
                if (!success) {
                    logToFile(`Chop etishda xato: ${errorType}`, 'ERROR');
                } else {
                    logToFile('Chop etish muvaffaqiyatli yakunlandi');
                }
                printWindow.destroy(); // Oynani yopamiz
            });

            return true;
        } catch (err) {
            await logToFile(`Chop etishda xato: ${err.message}`, 'ERROR');
            throw err;
        }
    });

    ipcMain.handle('log-to-file', async (event, message, level) => {
        await logToFile(message, level);
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});