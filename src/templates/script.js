let papers = [];
let savedPapers = [];
function loadMockData() {
    papers = [
        {
            title: "AI in Modern Research",
            link: "https://example.com/ai-research",
            author: "John Doe",
            year: 2022,
            journal: "Tech Journal",
            citations: 1625,
            score: 4.5
        },
        {
            title: "Cybersecurity Trends",
            link: "https://example.com/cybersecurity-trends",
            author: "Jane Smith",
            year: 2021,
            journal: "Security Today",
            citations: 890,
            score: 4.0
        },
        {
            title: "Machine Learning Basics",
            link: "https://example.com/machine-learning-basics",
            author: "Mike Brown",
            year: 2020,
            journal: "AI Journal",
            citations: 1200,
            score: 4.2
        }
    ];
}
function showScreen(screenId) {
            document.querySelectorAll("main section").forEach(section => {
                section.style.display = "none";
            });

            document.getElementById(screenId).style.display = "block";
        }
        
       // Show the login screen by default
        showScreen('login');


// Navigation link event listeners
const searchLink = document.getElementById('search-link');
searchLink.addEventListener('click', (event) => {
    event.preventDefault();
    showScreen('search');
});

const aboutLink = document.getElementById('about-link');
aboutLink.addEventListener('click', (event) => {
    event.preventDefault();
    showScreen('about');
});

const resultsLink = document.getElementById('results-link');
resultsLink.addEventListener('click', (event) => {
    event.preventDefault();
    showScreen('results');
});

const savedLink = document.getElementById('saved-papers-link');
savedLink.addEventListener('click', (event) => {
    event.preventDefault();
    displaySavedPapers();
    showScreen('saved-papers');
});

const loginLink = document.getElementById('login-link');
loginLink.addEventListener('click', (event) => {
    event.preventDefault();
    showScreen('login');
});

const aboutLink2 = document.getElementById('about-link2');
aboutLink2.addEventListener('click', (event) => {
    event.preventDefault();
    showScreen('about');
});

const searchLink2 = document.getElementById('search-link2');
searchLink2.addEventListener('click', (event) => {
    event.preventDefault();
    showScreen('search');
});


// Login form event listener
let usernameInput = document.getElementById('username');
let login = document.getElementById('login-form');
login.addEventListener('submit', (event) => {
    event.preventDefault();
    let usernamevalue = usernameInput.value.trim();
    if (usernamevalue) {
        alert(`Welcome, ${usernamevalue}! You are now logged in.`);
        showScreen('search');
    } else {
        alert('Please enter a username.');
    }
});

// Function to display search results
function displayResults(data) { 
    const tbody = document.querySelector(".results-table tbody"); 
    tbody.innerHTML = ""; 

    data.forEach((paper, index )=> { 
        const row = document.createElement("tr"); 

        row.innerHTML = ` 
            <td>${paper.title}</td>
            <td><a href="#">View</a></td>
            <td>${paper.author}</td>
            <td>${paper.year}</td>
            <td>${paper.journal}</td>
            <td>${paper.citations}</td>
            <td>${paper.score}</td>
            <td><button class="save-btn" data-index="${index}" >Save</button></td>
            
        `;

        tbody.appendChild(row); 
    });

     document.querySelectorAll(".save-btn").forEach(button => {
        button.addEventListener("click", function () {
            const index = this.getAttribute("data-index");
            savePaper(data[index]); 
        });
    });
}

// Function to save a paper to the saved papers list
function savePaper(paper) {

    const exists = savedPapers.some(p => p.title === paper.title);

    if (!exists) {
        savedPapers.push(paper);
        alert("Paper saved!");
    } else {
        alert("Already saved!");
    }
}
// Funtion to saved papers
function displaySavedPapers() { 
    const tbody = document.getElementById("saved-body"); 
    tbody.innerHTML = ""; 

    savedPapers.forEach(paper => { 
        const row = document.createElement("tr"); 

        row.innerHTML = `
            <td>${paper.title}</td>
            <td><a href="#">View</a></td>
            <td>${paper.author}</td>
            <td>${paper.year}</td>
            <td>${paper.journal}</td>
            <td>${paper.citations}</td>
            <td>${paper.score}</td>
        `;

        tbody.appendChild(row); 
    });
}


// Function to filter papers based on search query
function filterPapers(query) { 
    return papers.filter(paper => 
        paper.title.toLowerCase().includes(query) || 
        paper.author.toLowerCase().includes(query) 
    );
}

// Search form event listener
const searchForm = document.querySelector('.search-form'); 
const searchInput = document.getElementById('search-input'); 

searchForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const queryValue = searchInput.value.toLowerCase().trim();

     if (!queryValue) { 
        displayResults(papers); 
    } else {
        const results = filterPapers(queryValue); 
        displayResults(results); 
    }

    showScreen('results');
});


 // Filter dropdown event listener
const filterSelect = document.getElementById('filter');
filterSelect.addEventListener('change', function () {
    console.log("Filter changed to:", this.value);
});

// Input change event listener for debugging.
searchInput.addEventListener('change', function () {
    console.log("Final input value:", this.value);
});


// Load mock data on page load
loadMockData();




