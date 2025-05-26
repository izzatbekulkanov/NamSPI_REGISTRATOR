const API_URL = "https://navbat.namspi.uz/api/tickets/serving/";

// Oldingi navbatlar ro‘yxatini saqlash
let previousTickets = [];

// E’lonlar navbati
let announcementQueue = [];
let isAnnouncing = false;

async function fetchServingTickets() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        const tbody = document.getElementById("ticket-body");

        // Yangi navbatlarni aniqlash
        const newTickets = data.serving_tickets.filter(ticket =>
            !previousTickets.some(prev => prev.ticket_number === ticket.ticket_number)
        );

        // Yangi navbatlarni e’lonlar navbatiga qo‘shish
        if (newTickets.length > 0) {
            newTickets.forEach(ticket => {
                announcementQueue.push(ticket);
            });
            announceNextTicket();
        }

        // Jadvalni yangilash
        tbody.innerHTML = "";
        data.serving_tickets.forEach(ticket => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${ticket.ticket_number}</td>
                <td>${ticket.window_number || "—"}</td>
            `;
            tbody.appendChild(row);
        });

        // Oldingi navbatlarni yangilash
        previousTickets = [...data.serving_tickets];

    } catch (error) {
        console.error("❌ API xatolik:", error);
    }
}

// E’lon qilish funksiyasi
function announceNextTicket() {
    if (isAnnouncing || announcementQueue.length === 0) return;

    isAnnouncing = true;
    const ticket = announcementQueue.shift();

    const announcement = document.getElementById("announcement");
    const announcementText = document.getElementById("announcement-text");

    // E’lon matni
    announcementText.textContent = `Navbat: ${ticket.ticket_number} | Oyna: ${ticket.window_number || "—"}`;
    announcement.classList.add("active");

    // Ovoz o‘ynatish
    const audio = new Audio("assets/sound/ding-dong.mp3");
    audio.play().catch(error => console.error("❌ Ovoz xatolik:", error));

    // 5 soniyadan so‘ng e’lonni yashirish
    setTimeout(() => {
        announcement.classList.remove("active");
        isAnnouncing = false;
        announceNextTicket(); // Keyingi e’lonni ko‘rsatish
    }, 5000);
}

// Har 5 soniyada yangilash
setInterval(fetchServingTickets, 5000);
fetchServingTickets();