//scripts.js

let papers = [];
let savedPapers = [];


let isLoggedIn = false; 

function showScreen(screenId) {

    document.querySelectorAll("main section").forEach(section => {
        section.style.display = "none";
    });

    document.getElementById(screenId).style.display = "block";
}


if (!isLoggedIn) {
    showScreen('login');
}



function requireLogin() {
    if (!isLoggedIn) {
        showScreen('login');
        return false;
    }
    return true;
}



const searchLink = document.getElementById('search-link');
searchLink?.addEventListener('click', (e) => {
    e.preventDefault();
    if (!requireLogin()) return;
    showScreen('search');
});

const aboutLink = document.getElementById('about-link');
aboutLink?.addEventListener('click', (e) => {
    e.preventDefault();
    showScreen('about');
});

const resultsLink = document.getElementById('results-link');
resultsLink?.addEventListener('click', (e) => {
    e.preventDefault();
    if (!requireLogin()) return;
    showScreen('results');
});

const savedLink = document.getElementById('saved-papers-link');
savedLink?.addEventListener('click', (e) => {
    e.preventDefault();
    if (!requireLogin()) return;
    displaySavedPapers();
    showScreen('saved-papers');
});

const loginLink = document.getElementById('login-link');
loginLink?.addEventListener('click', (e) => {
    e.preventDefault();
    showScreen('login');
});



const login = document.getElementById('login-form');
const usernameInput = document.getElementById('username');

login.addEventListener('submit', (e) => {
    e.preventDefault();

    const username = usernameInput.value.trim();

    if (username) {
        isLoggedIn = true; // ADDED FIX
        alert(`Welcome, ${username}!`);
        showScreen('search');
    } else {
        alert("Enter username");
    }
});


function displayResults(data) {

    const tbody = document.querySelector(".results-table tbody");
    tbody.innerHTML = "";

    data.forEach((paper, index) => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${paper.title}</td>

            <!-- FIXED: link_url → link -->
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
            const index = this.dataset.index;
            savePaper(data[index]);
        });
    });
}



function savePaper(paper) {

    const exists = savedPapers.some(p => p.title === paper.title);

    if (!exists) {
        savedPapers.push(paper);
        alert("Saved!");
    } else {
        alert("Already saved");
    }
}



function displaySavedPapers() {

    const tbody = document.getElementById("saved-body");
    tbody.innerHTML = "";

    savedPapers.forEach(paper => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${paper.title}</td>
            <td><a href="${paper.link}" target="_blank">View</a></td>
            <td>${paper.year}</td>
            <td>${paper.citations}</td>
            <td>${paper.source}</td>
        `;

        tbody.appendChild(row);
    });
}



const searchForm = document.querySelector('.search-form');
const searchInput = document.getElementById('search-input');

searchForm.addEventListener('submit', async (e) => {

    e.preventDefault();
    e.stopPropagation(); 

    const query = searchInput.value.trim();

    if (!query) return alert("Enter search");

    try {

        showScreen('status');

        const res = await fetch(
            `http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`
        );

        if (!res.ok) throw new Error("API error");

        const data = await res.json();

        if (!data || data.length === 0) {
            alert("No results");
            showScreen('search');
            return;
        }

        displayResults(data);

        showScreen('results');

    } catch (err) {
        console.error(err);
        alert("Fetch failed");

      
        showScreen('search');
    }
});



document.getElementById('filter')?.addEventListener('change', function () {
    console.log("Filter:", this.value);
});