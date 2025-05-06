// === render.js ===

const API = "https://webtest.namspi.uz/api/";

// Log yozish funksiyasi
function logToFile(message, level = 'INFO') {
  try {
    window.electronAPI.logToFile(message, level);
    console.log(`${new Date().toISOString()} [${level}] ${message}`);
  } catch (err) {
    console.error('❌ Log yozishda xato:', err.message);
  }
}

// Dinamik tugma yaratish
function createBtn(text, onClick) {
  try {
    const btn = document.createElement("button");
    btn.textContent = text;
    btn.onclick = () => {
      logToFile(`Tugma bosildi: ${text}`);
      onClick();
    };
    logToFile(`Tugma yaratildi: ${text}`);
    return btn;
  } catch (err) {
    logToFile(`Tugma yaratishda xato: ${err.message}`, 'ERROR');
    throw err;
  }
}

// Bo‘limlarni yuklash
function loadSections() {
  logToFile('Bo‘limlarni yuklash boshlandi');
  fetch(API + "sections/")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP xato: ${res.status}`);
        return res.json();
      })
      .then((sections) => {
        const box = document.getElementById("sections");
        if (!box) throw new Error('sections elementi topilmadi');
        sections.forEach((sec) => {
          box.appendChild(createBtn(sec.name, () => loadSubservices(sec.id, sec.name)));
        });
        logToFile(`Bo‘limlar yuklandi: ${sections.length} ta`);
      })
      .catch((err) => {
        logToFile(`Bo‘limlarni yuklashda xato: ${err.message}`, 'ERROR');
      });
}

// Xizmatlarni yuklash
function loadSubservices(sectionId, sectionName) {
  try {
    logToFile(`Xizmatlarni yuklash boshlandi: sectionId=${sectionId}, sectionName=${sectionName}`);
    document.getElementById("subTitle").innerText = `${sectionName} xizmatlari:`;
    const box = document.getElementById("subservices");
    if (!box) throw new Error('subservices elementi topilmadi');
    box.innerHTML = "";

    fetch(API + `subservices/${sectionId}/`)
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP xato: ${res.status}`);
          return res.json();
        })
        .then((subs) => {
          subs.forEach((sub) => {
            box.appendChild(createBtn(sub.name, () => createTicket(sub.id)));
          });
          logToFile(`Xizmatlar yuklandi: ${subs.length} ta`);
        })
        .catch((err) => {
          logToFile(`Xizmatlarni yuklashda xato: ${err.message}`, 'ERROR');
        });
  } catch (err) {
    logToFile(`Xizmatlarni yuklashda xato: ${err.message}`, 'ERROR');
  }
}

// Chipta yaratish
function createTicket(subId) {
  logToFile(`Chipta yaratish boshlandi: subId=${subId}`);
  fetch(API + `ticket/create/${subId}/`, {
    method: "POST",
    headers: { "X-Requested-With": "XMLHttpRequest" },
  })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP xato: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (data.success) {
          logToFile(`Chipta yaratildi: ${data.ticket_number}`);
          printTicket(data);
        } else {
          throw new Error('Chipta yaratish muvaffaqiyatsiz');
        }
      })
      .catch((err) => {
        logToFile(`Chipta yaratishda xato: ${err.message}`, 'ERROR');
      });
}

// Chipta chop etish
async function printTicket(data) {
  try {
    logToFile(`Chipta chop etish boshlandi: ticket_number=${data.ticket_number}`);
    const savedPrinter = await window.electronAPI.getSavedPrinter();
    if (!savedPrinter) {
      logToFile('Printer tanlanmagan', 'WARNING');
      throw new Error('Printer tanlanmagan');
    }

    const now = new Date();
    const time = now.toLocaleTimeString("uz-UZ");
    const date = now.toLocaleDateString("uz-UZ");

    const html = `
      <html>
        <head>
          <style>
            body { font-family: monospace; font-size: 12px; text-align: center; margin: 0; padding: 0; }
            .line { margin: 3px 0; font-size: 12px; }
            .logo { width: 50px; height: auto; margin-top: 2px; }
            .title { font-size: 14px; font-weight: bold; margin: 2px 0; }
            .web { font-size: 11px; margin: 0 0 3px 0; }
            .ticket { font-size: 48px; font-weight: bold; margin: 0px 0; }
            .datetime { font-size: 11px; margin-top: 2px; }
          </style>
        </head>
        <body>
          <div class="line">────────────</div>
          <img class="logo" src="file://${__dirname}/assets/logo.png" alt="logo"><br>
          <div class="title">NamDPI | RTTM</div>
          <div class="web">www.namspi.uz</div>
          <div class="ticket">${data.ticket_number}</div>
          <div class="datetime">${time} ${date}</div>
          <div class="line">────────────</div>
        </body>
      </html>
    `;

    await window.electronAPI.printTicket(html);
    logToFile(`Chipta chop etildi: ${data.ticket_number}`);
  } catch (err) {
    logToFile(`Chipta chop etishda xato: ${err.message}`, 'ERROR');
    throw err;
  }
}

// renderAPI ni global qilish
window.renderAPI = {
  printTicket,
};

// DOM yuklanganda
document.addEventListener("DOMContentLoaded", () => {
  try {
    logToFile('DOM yuklandi, render.js ishga tushdi');
    loadSections();
  } catch (err) {
    logToFile(`render.js ishga tushirishda xato: ${err.message}`, 'ERROR');
  }
});