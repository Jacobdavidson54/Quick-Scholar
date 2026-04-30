//scripts.js

/* =========================
   1. GLOBAL STATE
========================= */
let state = {
    user: localStorage.getItem("user"), // now stores user_id
    username: null,
    papers: [],
    savedPapers: []
};

/* =========================
   UI MESSAGE SYSTEM
========================= */
function showToast(type, message) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const MAX_TOASTS = 4;

    // Limit stack
    if (container.children.length >= MAX_TOASTS) {
        container.removeChild(container.firstChild);
    }

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    toast.innerHTML = `
        <span>${message}</span>
        <button>&times;</button>
    `;

    const closeBtn = toast.querySelector("button");

    const removeToast = () => {
        toast.style.animation = "toastOut 0.3s ease forwards";
        setTimeout(() => toast.remove(), 300);
    };

    closeBtn.addEventListener("click", removeToast);

    container.appendChild(toast);

    // Auto remove
    setTimeout(removeToast, 4000);
}

function clearLocalSaved() {
    // REMOVED LOGIC (kept for safety fallback)
}


/* =========================
   3. UI HELPERS
========================= */
function showScreen(screenId) {
    document.querySelectorAll("main section").forEach(section => {
        section.style.display = "none";
    });
    document.getElementById(screenId).style.display = "block";
}

function updateNav() {
    const loginLink = document.getElementById("login-link");
    const logoutLink = document.getElementById("logout-link");

    if (state.user) {
        loginLink.style.display = "none";
        logoutLink.style.display = "inline";
    } else {
        loginLink.style.display = "inline";
        logoutLink.style.display = "none";
    }
}


/* =========================
   4. AUTH LOGIC 
========================= */
async function loginUser(username) {

    try {
        const res = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ username })
        });

        const data = await res.json();

        state.user = data.user_id;
        state.username = data.username;

        localStorage.setItem("user", data.user_id);

        updateNav();
        showToast("success", "Logged in successfully");
        showScreen("search");

    } catch (err) {
        console.error(err);
        showToast("error","login failed");
    }
}

function logoutUser() {
    localStorage.removeItem("user");

    state.user = null;
    state.username = null;
    state.savedPapers = [];

    updateNav();
    showToast("success", "Logged out successfully");
    showScreen("login");
}

function requireLogin() {
    if (!state.user) {
        showScreen("login");
        return false;
    }
    return true;
}


/* =========================
   5. PAPERS LOGIC 
========================= */
async function savePaper(paper) {

    try {
        const res = await fetch("http://127.0.0.1:5000/save", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                user_id: state.user,
                query: state.lastQuery || "",
                papers: [paper]
            })
        });

        const data = await res.json();

        showToast("success",data.message || "saved");

    } catch (err) {
        console.error(err);
        showToast("error","save failed");
    }
}


/* =========================
 LOAD SAVED PAPERS 
========================= */
async function loadSavedPapers() {

    try {
        const res = await fetch(
            `http://127.0.0.1:5000/saved/${state.user}`
        );

        const data = await res.json();

        state.savedPapers = data;

        displaySavedPapers();

    } catch (err) {
        console.error(err);
        showToast("error","failed to load saved papers");
    }
}


/* =========================
 DISPLAY SAVED PAPERS
========================= */
function displaySavedPapers() {

    const tbody = document.getElementById("saved-body");
    if (!tbody) return;

    tbody.innerHTML = "";

    state.savedPapers.forEach((paper, index) => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${paper.title}</td>
            <td><a href="${paper.link}" target="_blank">View</a></td>
            <td>${paper.year}</td>
            <td>${paper.citations}</td>
            <td>${paper.source}</td>
            <td>
                <button class="unsave-btn" data-id="${paper.id}">
                    Unsave
                </button>
            </td>
        `;

        tbody.appendChild(row);
    });

    document.querySelectorAll(".unsave-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const id = parseInt(this.dataset.id);
        unsavePaper(id);
    });
});
}


/* =========================
 UNSAVE FUNCTION
========================= */
async function unsavePaper(id) {

    try {
        
        const res = await fetch(`http://127.0.0.1:5000/papers/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            throw new Error("Delete failed");
        }

       
        state.savedPapers = state.savedPapers.filter(p => p.id != id);

        displaySavedPapers();

        showToast("success","paper removed");

    } catch (err) {
        console.error(err);
        showToast("error","failed to remove paper");
    }
}

/* =========================
   6. RESULTS UI
========================= */
function displayResults(data) {
    const tbody = document.querySelector(".results-table tbody");
    tbody.innerHTML = "";

    data.forEach((paper, index) => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${paper.title}</td>
            <td><a href="${paper.link}" target="_blank">View</a></td>
            <td>${paper.year}</td>
            <td>${paper.citations}</td>
            <td>${paper.source}</td>
            <td><button class="save-btn" data-index="${index}">Save</button></td>
        `;

        tbody.appendChild(row);
    });

    document.querySelectorAll(".save-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            savePaper(data[this.dataset.index]);
        });
    });
}


/* =========================
   7. API LOGIC
========================= */
async function searchPapers(query) {

    state.lastQuery = query; // IMPORTANT for DB saving

    try {
        showScreen("status");

        const res = await fetch(
            `http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`
        );

        if (!res.ok) throw new Error("API error");

        const data = await res.json();

        if (!data.length) {
            showToast("error","no results");
            showScreen("search");
            return;
        }

        state.papers = data;

        displayResults(data);
        showToast("success", "Results loaded");
        showScreen("results");

    } catch (err) {
        console.error(err);
        showToast("error","fetch failed");
        showScreen("search");
    }
}


/* =========================
   8. EVENT LISTENERS
========================= */
function setupEventListeners() {

    document.getElementById('search-link')?.addEventListener('click', e => {
        e.preventDefault();
        if (!requireLogin()) return;
        showScreen('search');
    });

    document.getElementById('about-link')?.addEventListener('click', e => {
        e.preventDefault();
        showScreen('about');
    });

    document.getElementById('results-link')?.addEventListener('click', e => {
        e.preventDefault();
        if (!requireLogin()) return;
        showScreen('results');
    });

    document.getElementById('saved-papers-link')?.addEventListener('click', async e => {
        e.preventDefault();
        if (!requireLogin()) return;

        await loadSavedPapers();
        showScreen('saved-papers');
    });

    document.getElementById('login-link')?.addEventListener('click', e => {
        e.preventDefault();
        showScreen('login');
    });

    document.getElementById('logout-link')?.addEventListener('click', e => {
        e.preventDefault();
        logoutUser();
    });

    document.getElementById('login-form')?.addEventListener('submit', e => {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();

        if (!username) return showToast("error","enter username");

        loginUser(username);
    });

    document.querySelector('.search-form')?.addEventListener('submit', e => {
        e.preventDefault();

        if (!requireLogin()) return;

        const query = document.getElementById('search-input').value.trim();

        if (!query) return showToast("error","enter search");

        searchPapers(query);
    });

    document.getElementById('filter')?.addEventListener('change', function () {
        console.log("Filter:", this.value);
    });
}


/* =========================
   9. INIT
========================= */
document.addEventListener("DOMContentLoaded", () => {

    if (state.user) {
        showScreen("search");
    } else {
        showScreen("login");
    }

    updateNav();
    setupEventListeners();
});