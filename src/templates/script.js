//scripts.js

/* =========================
   1. GLOBAL STATE
========================= */
let state = {
    user: localStorage.getItem("user"),
    papers: [],
    savedPapers: []
};

/* =========================
   2. STORAGE HELPERS
========================= */
function getSavedKey() {
    return `savedPapers_${state.user}`;
}

function loadSavedPapers() {
    if (!state.user) return [];
    const data = localStorage.getItem(getSavedKey());
    return data ? JSON.parse(data) : [];
}

function persistSavedPapers() {
    if (!state.user) return;
    localStorage.setItem(getSavedKey(), JSON.stringify(state.savedPapers));
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
function loginUser(username) {
    state.user = username;
    localStorage.setItem("user", username);

    state.savedPapers = loadSavedPapers();

    updateNav();
    showScreen("search");
}

function logoutUser() {
    localStorage.removeItem("user");

    state.user = null;
    state.savedPapers = [];

    updateNav();
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
function savePaper(paper) {
    const exists = state.savedPapers.some(p => p.title === paper.title);

    if (!exists) {
        state.savedPapers.push(paper);
        persistSavedPapers();
        alert("Saved!");
    } else {
        alert("Already saved");
    }
}

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
                <button class="unsave-btn" data-index="${index}">
                    Unsave
                </button>
            </td>
        `;

        tbody.appendChild(row);
    });

    document.querySelectorAll(".unsave-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            removeSavedPaper(this.dataset.index);
        });
    });
}


/* =========================
 UNSAVE FUNCTION
========================= */
function removeSavedPaper(index) {

  
    state.savedPapers.splice(index, 1);

    persistSavedPapers();

    displaySavedPapers();
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
    try {
        showScreen("status");

        const res = await fetch(
            `http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`
        );

        if (!res.ok) throw new Error("API error");

        const data = await res.json();

        if (!data.length) {
            alert("No results");
            showScreen("search");
            return;
        }

        state.papers = data;

        displayResults(data);
        showScreen("results");

    } catch (err) {
        console.error(err);
        alert("Fetch failed");
        showScreen("search");
    }
}

/* =========================
   8. EVENT LISTENERS
========================= */
function setupEventListeners() {

    // NAV
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

    document.getElementById('saved-papers-link')?.addEventListener('click', e => {
        e.preventDefault();
        if (!requireLogin()) return;
        state.savedPapers = loadSavedPapers(); 
        displaySavedPapers();
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

    // LOGIN
    document.getElementById('login-form')?.addEventListener('submit', e => {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();

        if (!username) return alert("Enter username");

        loginUser(username);
    });

    // SEARCH
    document.querySelector('.search-form')?.addEventListener('submit', e => {
        e.preventDefault();

        if (!requireLogin()) return;

        const query = document.getElementById('search-input').value.trim();

        if (!query) return alert("Enter search");

        searchPapers(query);
    });

    // FILTER
    document.getElementById('filter')?.addEventListener('change', function () {
        console.log("Filter:", this.value);
    });
}

/* =========================
   9. APP INIT
========================= */
document.addEventListener("DOMContentLoaded", () => {

    // Load saved papers if user exists
    if (state.user) {
        state.savedPapers = loadSavedPapers();
        showScreen("search");
    } else {
        showScreen("login");
    }

    updateNav();
    setupEventListeners();
});