function showScreen(screenId) {
            document.querySelectorAll("main section").forEach(section => {
                section.style.display = "none";
            });

            document.getElementById(screenId).style.display = "block";
        }
        
       // Show the login screen by default
        showScreen('login');