/* -------------------------------------------------------------
 * High-Performance HTML5 Canvas Multicolor Particle Universe
 * ------------------------------------------------------------- */

(function () {
    const canvas = document.getElementById('universe-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    let particles = [];
    let mouse = { x: null, y: null, radius: 150 };
    
    // Colorful cosmic palette
    const colors = [
        'rgba(139, 92, 246, 0.65)',  /* Purple */
        'rgba(6, 182, 212, 0.65)',   /* Cyan */
        'rgba(245, 158, 11, 0.55)',   /* Amber */
        'rgba(236, 72, 153, 0.55)',   /* Pink */
    ];
    
    // Handle Window Resizing
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        initParticles();
    }
    
    window.addEventListener('resize', resizeCanvas);
    
    // Mouse Coordinates Tracking
    window.addEventListener('mousemove', function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    
    window.addEventListener('mouseleave', function () {
        mouse.x = null;
        mouse.y = null;
    });
    
    // Particle Blueprints
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5; // Small, elegant size
            this.baseSize = this.size;
            
            // Floating speed
            this.vx = (Math.random() - 0.5) * 0.4;
            this.vy = (Math.random() - 0.5) * 0.4;
            
            // Random color from theme
            this.color = colors[Math.floor(Math.random() * colors.length)];
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
        
        update() {
            // Collision boundary wrap
            if (this.x < 0 || this.x > canvas.width) this.vx = -this.vx;
            if (this.y < 0 || this.y > canvas.height) this.vy = -this.vy;
            
            // Core coordinate movement
            this.x += this.vx;
            this.y += this.vy;
            
            // Mouse Interaction (Dynamic repulsion/attraction)
            if (mouse.x !== null && mouse.y !== null) {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < mouse.radius) {
                    let forceDirectionX = dx / distance;
                    let forceDirectionY = dy / distance;
                    
                    // Simple repel force
                    let force = (mouse.radius - distance) / mouse.radius;
                    let directionX = forceDirectionX * force * 1.5;
                    let directionY = forceDirectionY * force * 1.5;
                    
                    this.x -= directionX;
                    this.y -= directionY;
                    
                    // Slightly expand when near mouse
                    this.size = this.baseSize * 1.5;
                } else {
                    if (this.size > this.baseSize) {
                        this.size -= 0.05;
                    }
                }
            } else {
                if (this.size > this.baseSize) {
                    this.size -= 0.05;
                }
            }
            
            this.draw();
        }
    }
    
    // Seed Particle List
    function initParticles() {
        particles = [];
        // Adaptive density based on display resolution
        const numberOfParticles = Math.min((canvas.width * canvas.height) / 11000, 120);
        for (let i = 0; i < numberOfParticles; i++) {
            particles.push(new Particle());
        }
    }
    
    // Inter-particle Connecting Vectors (Constellation Lines)
    function connectParticles() {
        let maxDistance = 110;
        let isLightTheme = document.documentElement.classList.contains('light');
        let strokeColor = isLightTheme ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.035)';
        
        for (let a = 0; a < particles.length; a++) {
            for (let b = a + 1; b < particles.length; b++) {
                let dx = particles[a].x - particles[b].x;
                let dy = particles[a].y - particles[b].y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < maxDistance) {
                    // Line opacity scales based on distance
                    let opacity = (1 - (distance / maxDistance)) * 0.25;
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    
                    // Mix matching gradient color
                    ctx.strokeStyle = isLightTheme 
                        ? `rgba(139, 92, 246, ${opacity * 0.3})`
                        : `rgba(6, 182, 212, ${opacity * 0.35})`;
                        
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
    }
    
    // High-Performance Engine Loop
    function animateUniverse() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
        }
        
        connectParticles();
        requestAnimationFrame(animateUniverse);
    }
    
    // Kick-Off Initialization
    resizeCanvas();
    animateUniverse();
})();
