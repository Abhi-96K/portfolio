/* -------------------------------------------------------------
 * Theme Controller (Dark/Light Modes & Persistent Preferences)
 * ------------------------------------------------------------- */

(function () {
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (!themeToggleBtn) return;
    
    // Evaluate initial theme
    const userPref = localStorage.getItem('color-theme');
    const systemPref = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (userPref === 'light' || (!userPref && !systemPref)) {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
    } else {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    }
    
    themeToggleBtn.addEventListener('click', function () {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
        
        // Dispatch theme changed event for canvas particle adaptations
        window.dispatchEvent(new Event('themeChanged'));
    });
})();
