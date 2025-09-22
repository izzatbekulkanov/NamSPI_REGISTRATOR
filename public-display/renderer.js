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
            announcementQueue.push(...newTickets);
            if (!isAnnouncing) announceNextTicket(); // Agar e’lon jarayoni boshlanmagan bo‘lsa, darhol boshlash
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

    // E’lon matnini darhol yangilash
    announcementText.textContent = `Navbat: ${ticket.ticket_number} | Oyna: ${ticket.window_number || "—"}`;
    announcement.classList.add("active");

    // Ovoz fayllarini ketma-ket o‘ynatish
    const dingDongAudio = new Audio("assets/sound/ding-dong.mp3");
    const voiceMaftunaAudio = new Audio("assets/sound/voice_maftuna.wav");

    dingDongAudio.play().catch(error => console.error("❌ Ding-dong ovoz xatolik:", error));

    // Ding-dong tugagach, voice_maftuna o‘ynaydi
    dingDongAudio.onended = () => {
        voiceMaftunaAudio.play().catch(error => console.error("❌ Voice_maftuna ovoz xatolik:", error));
    };

    // E’lonni 7 soniya ko‘rsatish (ding-dong ~2s + voice_maftuna ~5s uchun yetarli vaqt)
    setTimeout(() => {
        announcement.classList.remove("active");
        isAnnouncing = false;
        announceNextTicket(); // Keyingi e’lonni ko‘rsatish
    }, 7000);
}

// Har 3 soniyada yangilash (tezroq yangilash uchun 5s dan 3s ga kamaytirdim)
setInterval(fetchServingTickets, 3000);
fetchServingTickets();