/* -------------------------------------------------------------
 * Dynamic Cinematic Reveals, Orbiting Skill Galaxy & GSAP Scroll
 * ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. Cinematic Page Loader & Count-Up Reveal
    // ==========================================
    const loader = document.getElementById('loader');
    const percentText = document.getElementById('loader-percent');
    
    let count = 0;
    const countInterval = setInterval(() => {
        count += Math.floor(Math.random() * 8) + 3; // Random speed increment
        if (count >= 100) {
            count = 100;
            clearInterval(countInterval);
            triggerOpeningReveal();
        }
        if (percentText) {
            percentText.innerText = count.toString().padStart(2, '0');
        }
    }, 45);
    
    function triggerOpeningReveal() {
        if (typeof gsap !== 'undefined') {
            // Exit count elements
            gsap.to('#loader svg, #loader div', {
                opacity: 0,
                y: -20,
                duration: 0.5,
                stagger: 0.1,
                ease: 'power3.in'
            });
            
            // Split-screen sliding panels
            gsap.to('.loader-split-top', {
                y: '-100%',
                duration: 0.8,
                delay: 0.4,
                ease: 'power4.inOut'
            });
            
            gsap.to('.loader-split-bottom', {
                y: '100%',
                duration: 0.8,
                delay: 0.4,
                ease: 'power4.inOut',
                onComplete: () => {
                    if (loader) loader.style.display = 'none';
                    initScrollTriggerAnimations();
                }
            });
            
            // Immersive camera zoom-out Hero reveal
            gsap.from('#hero-container', {
                scale: 1.15,
                opacity: 0,
                duration: 1.5,
                delay: 0.7,
                ease: 'power3.out'
            });
            
            gsap.from('#main-header', {
                y: -50,
                opacity: 0,
                duration: 1.0,
                delay: 0.9,
                ease: 'power3.out'
            });
            
            gsap.from('.hero-stagger', {
                y: 30,
                opacity: 0,
                duration: 1.0,
                stagger: 0.15,
                delay: 1.1,
                ease: 'power3.out'
            });
        } else {
            // Production Fallback in case GSAP CDN fails to load
            console.warn("GSAP CDN not loaded. Running standard CSS transitions...");
            const topSplit = document.querySelector('.loader-split-top');
            const bottomSplit = document.querySelector('.loader-split-bottom');
            const loaderTitle = document.querySelector('#loader svg');
            const loaderNum = document.querySelector('#loader div');
            
            if (loaderTitle) loaderTitle.style.opacity = '0';
            if (loaderNum) loaderNum.style.opacity = '0';
            
            if (topSplit) {
                topSplit.style.transition = 'transform 0.8s cubic-bezier(0.77, 0, 0.175, 1)';
                topSplit.style.transform = 'translateY(-100%)';
            }
            if (bottomSplit) {
                bottomSplit.style.transition = 'transform 0.8s cubic-bezier(0.77, 0, 0.175, 1)';
                bottomSplit.style.transform = 'translateY(100%)';
            }
            
            setTimeout(() => {
                if (loader) loader.style.display = 'none';
                const hero = document.getElementById('hero-container');
                const header = document.getElementById('main-header');
                if (hero) {
                    hero.style.transition = 'opacity 1s ease';
                    hero.style.opacity = '1';
                }
                if (header) {
                    header.style.transition = 'opacity 1s ease';
                    header.style.opacity = '1';
                }
            }, 600);
        }
    }

    // ==========================================
    // 2. Lenis Smooth Scrolling Setup
    // ==========================================
    let lenis;
    if (typeof Lenis !== 'undefined') {
        try {
            lenis = new Lenis({
                duration: 1.3,
                easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
                smoothWheel: true,
                orientation: 'vertical'
            });
            
            if (typeof ScrollTrigger !== 'undefined') {
                lenis.on('scroll', ScrollTrigger.update);
            }
            
            if (typeof gsap !== 'undefined') {
                gsap.ticker.add((time) => {
                    lenis.raf(time * 1000);
                });
                gsap.ticker.lagSmoothing(0);
            }
        } catch (e) {
            console.warn("Lenis initialization skipped:", e);
        }
    }

    // ==========================================
    // 3. Immersive Orbiting Skill Galaxy (3D Trig Math)
    // ==========================================
    const skills = document.querySelectorAll('.galaxy-skill-node');
    if (skills.length > 0) {
        let angles = Array.from(skills).map((_, i) => (i * (360 / skills.length)) * (Math.PI / 180));
        
        // Core orbiting loop in animation frames
        function orbitLoop() {
            skills.forEach((node, i) => {
                const distance = (parseFloat(node.dataset.distance) || 160) * 1.3;
                const rawSpeed = parseFloat(node.dataset.speed);
                const speed = isNaN(rawSpeed) ? 1.0 : rawSpeed;
                
                // Update angles based on velocity
                angles[i] += 0.003 * speed;
                
                // Calculate 3D projected coordinates
                const x = Math.cos(angles[i]) * distance;
                // Scale Y coordinates to match 75-degree rotation tilt
                const y = Math.sin(angles[i]) * distance * 0.25; 
                // Depth calculations
                const z = Math.sin(angles[i]) * distance;
                
                // Math scale factor based on Z perspective
                const scale = ((z + distance) / (distance * 2)) * 0.4 + 0.8;
                // Layer opacity
                const opacity = ((z + distance) / (distance * 2)) * 0.6 + 0.4;
                const zIndex = Math.floor(((z + distance) / (distance * 2)) * 100);
                
                // Position element
                node.style.transform = `translate3d(calc(-50% + ${x}px), calc(-50% + ${y}px), ${z}px) scale(${scale})`;
                node.style.opacity = opacity;
                node.style.zIndex = zIndex;
            });
            requestAnimationFrame(orbitLoop);
        }
        
        // Hover pause trigger
        skills.forEach((node, i) => {
            node.addEventListener('mouseenter', () => {
                node.dataset.originalSpeed = node.dataset.speed;
                node.dataset.speed = "0.0"; // Pause orbit
            });
            node.addEventListener('mouseleave', () => {
                node.dataset.speed = node.dataset.originalSpeed || "1.0"; // Resume orbit
            });
        });
        
        orbitLoop();
    }

    // ==========================================
    // 4. GSAP ScrollTrigger Animations
    // ==========================================
    function initScrollTriggerAnimations() {
        if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
            console.warn("GSAP / ScrollTrigger not loaded. Skipping scroll trigger animations.");
            return;
        }
        
        try {
            gsap.registerPlugin(ScrollTrigger);
            
            // A. Experiences Neon Timeline Laser Tracer
            const timelineTracker = document.querySelector('.timeline-laser-tracker');
            const timelineSection = document.querySelector('#timeline');
            
            if (timelineTracker && timelineSection) {
                gsap.to(timelineTracker, {
                    height: '100%',
                    ease: 'none',
                    scrollTrigger: {
                        trigger: '#timeline-content',
                        start: 'top 40%',
                        end: 'bottom 60%',
                        scrub: 0.5,
                        markers: false
                    }
                });
            }
            
            // B. Cinematic About Me Journey Storytelling scroller
            gsap.utils.toArray('.about-reveal').forEach((elem) => {
                gsap.from(elem, {
                    y: 50,
                    opacity: 0,
                    duration: 1.0,
                    scrollTrigger: {
                        trigger: elem,
                        start: 'top 80%',
                        toggleActions: 'play none none reverse'
                    }
                });
            });

            // C. Base Section Heading Cyber Staggers
            gsap.utils.toArray('.section-heading-trigger').forEach((heading) => {
                const lines = heading.querySelectorAll('.heading-line');
                gsap.from(lines, {
                    y: 40,
                    opacity: 0,
                    duration: 0.8,
                    stagger: 0.15,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: heading,
                        start: 'top 85%'
                    }
                });
            });
        } catch (e) {
            console.warn("GSAP scroll triggers failed to load:", e);
        }
    }

    // 3D Card Hover Tilts (Always works, pure JS)
    const tiltCards = document.querySelectorAll('.cyber-card');
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate percentage displacement
            const rotateX = ((y / rect.height) - 0.5) * -16; // Up to 16 deg tilt
            const rotateY = ((x / rect.width) - 0.5) * 16;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
        });
    });
});
