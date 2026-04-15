function showScreen(screenId) {
            document.querySelectorAll("main section").forEach(section => {
                section.style.display = "none";
            });

            document.getElementById(screenId).style.display = "block";
        }
        
       // Show the login screen by default
        showScreen('login');



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

