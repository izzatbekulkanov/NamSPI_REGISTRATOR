// === print.js ===

// Log yozish funksiyasi
function logToFile(message, level = 'INFO') {
    try {
        window.electronAPI.logToFile(message, level);
        console.log(`${new Date().toISOString()} [${level}] ${message}`);
    } catch (err) {
        console.error('❌ Log yozishda xato:', err.message);
    }
}

// Chipta chop etish funksiyasi
async function printTicket(data) {
    try {
        logToFile(`📤 Chipta chop etish boshlandi: ticket_number=${data.ticket_number}`);

        const savedPrinter = await window.electronAPI.getSavedPrinter();
        if (!savedPrinter) {
            logToFile('⚠️ Printer tanlanmagan', 'WARNING');
            throw new Error('Printer tanlanmagan');
        }
        logToFile(`🖨 Tanlangan printer: ${savedPrinter}`);

        const now = new Date();
        const time = now.toLocaleTimeString("uz-UZ");
        const date = now.toLocaleDateString("uz-UZ");

        // Base64 image load (logo.png must be in assets)
        const logoBase64 = await fetch("assets/logo.png")
            .then(res => res.blob())
            .then(blob => new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            }));

        const html = `
        <html>
          <head>
            <meta charset="UTF-8">
            <style>
              body {
                font-family: monospace;
                font-size: 12px;
                text-align: center;
                width: 50mm;
                margin: 0;
                padding: 0;
              }
              .logo {
                width: 48px;
                margin: 6px auto 0;
              }
              .title {
                font-size: 13px;
                font-weight: bold;
                margin: 2px 0 6px;
              }
              .line {
                margin: 4px 0;
                font-size: 12px;
              }
              .ticket {
                font-size: 32px;
                font-weight: bold;
                margin: 8px 0;
              }
              .datetime {
                font-size: 12px;
                margin: 4px 0;
              }
              .footer {
                font-size: 10px;
                margin-top: 6px;
              }
            </style>
          </head>
          <body>
            <img class="logo" src="${logoBase64}" alt="logo" />
            <div class="title">NamDPI — Navbat Chipta</div>
            <div class="line">────────────</div>
            <div class="ticket">${data.ticket_number}</div>
            <div class="datetime">${date} | ${time}</div>
            <div class="line">────────────</div>
            <div class="footer">Xizmat navbat asosida ko‘rsatiladi</div>
            <div class="footer">www.namspi.uz</div>
          </body>
        </html>
        `;

        const ticketContent = `
Chipta tarkibi:
------------
NamDPI
${data.ticket_number}
${time} ${date}
------------
        `;
        logToFile(ticketContent);

        const printOptions = {
            silent: true,
            deviceName: savedPrinter,
            pageSize: { width: 58000, height: 100000 }, // 58mm x 100mm (mikrometr)
            margins: { marginType: 'none' },
            printBackground: true
        };

        logToFile(`🧾 Chop etish sozlamalari: ${JSON.stringify(printOptions)}`);
        await window.electronAPI.printTicket(html, printOptions);
        logToFile(`✅ Chipta chop etildi: ${data.ticket_number}`);
    } catch (err) {
        logToFile(`❌ Chipta chop etishda xato: ${err.message}`, 'ERROR');
        throw err;
    }
}


// Global qilib API ni export qilish
window.printAPI = {
    printTicket,
};

// JS fayl yuklangani haqida log
document.addEventListener("DOMContentLoaded", () => {
    logToFile('✅ print.js yuklandi');
});