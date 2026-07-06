/* 
   Project: India Vacanza Website
   Functionality: Smooth Scroll, Mobile Nav, Sticky Header, Reveal on Scroll
   WordPress Integration: Enqueue this script or include it via a Custom HTML block.
*/

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Sticky Header Logic
    const header = document.querySelector('.main-header');
    const scrollThreshold = 100;

    window.addEventListener('scroll', () => {
        if (window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Mobile Navigation Toggle
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');
    const navItems = document.querySelectorAll('.nav-links li');

    burger.addEventListener('click', () => {
        // Toggle Nav
        navLinks.classList.toggle('nav-active');

        // Animate Links
        navItems.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });

        // Burger Animation
        burger.classList.toggle('toggle');
    });

    // Handle Mobile Link Clicks (Close menu after selection)
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            if (navLinks.classList.contains('nav-active')) {
                navLinks.classList.remove('nav-active');
                burger.classList.remove('toggle');
                navItems.forEach(link => link.style.animation = '');
            }
        });
    });

    // 3. Smooth Scrolling (for all modern browsers)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            e.preventDefault();
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // 4. Reveal on Scroll (Intersection Observer)
    const revealElements = document.querySelectorAll('.dest-card, .stat-card, .tip-item, .section-title');
    
    const revealCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                observer.unobserve(entry.target);
            }
        });
    };

    const revealObserver = new IntersectionObserver(revealCallback, {
        threshold: 0.1
    });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        revealObserver.observe(el);
    });

    // Add class for active reveal in CSS via script (or just handle style here)
    window.addEventListener('scroll', () => {
        revealElements.forEach(el => {
            const speed = 0.5;
            if (el.getBoundingClientRect().top < window.innerHeight * 0.9) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    });

    // 5. International Phone Input Initialization
    const phoneInput = document.querySelector("#phone");
    let iti;
    if (phoneInput) {
        iti = window.intlTelInput(phoneInput, {
            initialCountry: "ca",
            nationalMode: false,
            autoPlaceholder: "aggressive",
            utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.10/build/js/utils.js",
        });

        // Automatically add '+' if the user starts typing or clicks the box
        phoneInput.addEventListener('focus', () => {
            if (!phoneInput.value) {
                phoneInput.value = '+';
            }
        });

        phoneInput.addEventListener('input', () => {
            let value = phoneInput.value.trim();
            if (!value.startsWith('+')) {
                phoneInput.value = '+' + value.replace(/\+/g, '');
            }
        });
    }

    // 6. Contact Form Submission (Formspree AJAX)
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button');
            const originalBtnText = submitBtn.innerText;
            
            // Get full international phone number
            const fullPhoneNumber = iti ? iti.getNumber() : "";
            
            const formData = new FormData(contactForm);
            if (fullPhoneNumber) {
                formData.set('phone', fullPhoneNumber); // Replace simple number with full international number
            }
            
            submitBtn.innerText = 'Sending...';
            submitBtn.disabled = true;

            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 'Accept': 'application/json' }
                });

                if (response.ok) {
                    // Premium Success Message
                    contactForm.innerHTML = `
                        <div class="success-message" style="text-align: center; padding: 30px; animation: fadeInUp 0.5s ease;">
                            <i class="fas fa-paper-plane" style="font-size: 3rem; color: var(--primary-color); margin-bottom: 20px;"></i>
                            <h3 style="margin-bottom: 10px;">Inquiry Sent!</h3>
                            <p style="margin-bottom: 20px;">Thank you for choosing India Vacanza. Our travel experts will get back to you within 24 hours.</p>
                            <button type="button" class="btn-outline" onclick="window.location.reload()">Send Another Inquiry</button>
                        </div>`;
                } else {
                    const data = await response.json();
                    if (Object.hasOwn(data, 'errors')) {
                        alert(data["errors"].map(error => error["message"]).join(", "));
                    } else {
                        throw new Error();
                    }
                }
            } catch (error) {
                alert('Oops! There was a problem sending your message. Please try again or contact us via phone.');
                submitBtn.innerText = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }

    // WhatsApp Welcome Bubble Timer
    setTimeout(() => {
        const welcomeBubble = document.querySelector('.whatsapp-welcome');
        if (welcomeBubble && !sessionStorage.getItem('whatsappDismissed')) {
            welcomeBubble.style.display = 'block';
        }
    }, 3000);

    // Handle Closing the Welcome Bubble
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('close-welcome')) {
            e.preventDefault();
            const bubble = document.querySelector('.whatsapp-welcome');
            if (bubble) {
                bubble.style.display = 'none';
                sessionStorage.setItem('whatsappDismissed', 'true');
            }
        }
    });

});

/* CSS Animation for Nav Links */
const style = document.createElement('style');
style.textContent = `
    @keyframes navLinkFade {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .nav-links.nav-active {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        right: 0;
        height: 92vh;
        top: 8vh;
        background-color: white;
        width: 100%;
        align-items: center;
        justify-content: space-around;
        transform: translateX(0%);
        transition: transform 0.5s ease-in;
        z-index: 999;
    }

    .burger.toggle .line1 { transform: rotate(-45deg) translate(-5px, 6px); }
    .burger.toggle .line2 { opacity: 0; }
    .burger.toggle .line3 { transform: rotate(45deg) translate(-5px, -6px); }

    /* Phone Input Fixes */
    .iti { width: 100%; display: block; }
    .iti__country-list { color: #333; text-align: left; }
`;
document.head.appendChild(style);
