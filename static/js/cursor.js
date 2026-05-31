/* -------------------------------------------------------------
 * Custom Magnetic Lag Cursor & Interactive Hover Triggers
 * ------------------------------------------------------------- */

(function () {
    // Disable on mobile/touch viewports
    if (window.matchMedia('(max-width: 768px)').matches) return;
    
    const cursor = document.getElementById('custom-cursor');
    const cursorDot = document.getElementById('custom-cursor-dot');
    if (!cursor || !cursorDot) return;
    
    let mouse = { x: 0, y: 0 }; // Actual mouse positions
    let cursorRing = { x: 0, y: 0 }; // Trailing ring position
    
    // Linear Interpolation factor for smooth lag (lag multiplier)
    const lerp = (start, end, amt) => (1 - amt) * start + amt * end;
    
    window.addEventListener('mousemove', function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        
        // Immediate position for the absolute core dot
        cursorDot.style.left = mouse.x + 'px';
        cursorDot.style.top = mouse.y + 'px';
    });
    
    // Main Physics loop for trailing outer cursor ring
    function renderCursor() {
        // Core Lerp tracking
        cursorRing.x = lerp(cursorRing.x, mouse.x, 0.12);
        cursorRing.y = lerp(cursorRing.y, mouse.y, 0.12);
        
        cursor.style.left = cursorRing.x + 'px';
        cursor.style.top = cursorRing.y + 'px';
        
        requestAnimationFrame(renderCursor);
    }
    
    renderCursor();
    
    // Magnetic Element Tracking & Hover Expansions
    function updateTriggers() {
        const interactiveElements = document.querySelectorAll('a, button, .cursor-magnetic, [role="button"], input, textarea, select');
        
        interactiveElements.forEach(el => {
            // Standard Hover Magnifying Scale
            el.addEventListener('mouseenter', () => {
                cursor.classList.add('hovered');
                
                // Show floating text hints if specified in data attributes
                if (el.dataset.cursorText) {
                    cursor.innerText = el.dataset.cursorText;
                }
            });
            
            el.addEventListener('mouseleave', () => {
                cursor.classList.remove('hovered');
                cursor.innerText = '';
                
                // Reset magnetic element offset
                if (el.classList.contains('magnetic-active')) {
                    el.style.transform = 'translate(0px, 0px)';
                }
            });
            
            // Premium Magnetic Pull Physics
            if (el.classList.contains('cursor-magnetic')) {
                el.classList.add('magnetic-active');
                
                el.addEventListener('mousemove', (e) => {
                    const rect = el.getBoundingClientRect();
                    const elX = rect.left + rect.width / 2;
                    const elY = rect.top + rect.height / 2;
                    
                    // Distance vectors from center
                    const dx = e.clientX - elX;
                    const dy = e.clientY - elY;
                    
                    // Pull element slightly (25% displacement offset)
                    el.style.transform = `translate(${dx * 0.25}px, ${dy * 0.25}px)`;
                    
                    // Pull the outer cursor ring directly to the mouse, overriding lag slightly
                    cursorRing.x = lerp(cursorRing.x, elX + dx * 0.4, 0.2);
                    cursorRing.y = lerp(cursorRing.y, elY + dy * 0.4, 0.2);
                });
            }
        });
    }
    
    // Initialize hover triggers
    updateTriggers();
    
    // Proactively re-evaluate triggers when content updates dynamically (like AJAX)
    window.addEventListener('contentUpdated', updateTriggers);
})();
