const root = document.documentElement;
const body = document.body;

const uiMessages = {
    sending: body?.dataset.sendingLabel || 'Sending...',
    copied: body?.dataset.copySuccess || 'Copied to clipboard!',
    error: body?.dataset.notificationError || 'Something went wrong. Please try again.',
    darkModeLabel: body?.dataset.darkModeLabel || 'Switch to dark mode',
    lightModeLabel: body?.dataset.lightModeLabel || 'Switch to light mode'
};

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3500);
}

// ============================================
// LANGUAGE SWITCHER
// ============================================
const languageSwitcher = document.getElementById('languageSwitcher');
if (languageSwitcher) {
    languageSwitcher.addEventListener('change', (event) => {
        const selectedLanguage = event.target.value;
        const url = new URL(window.location.href);
        url.searchParams.set('lang', selectedLanguage);
        window.location.assign(url.toString());
    });
}

// ============================================
// TYPING ANIMATION
// ============================================
const typingElement = document.querySelector('.typing-text');
if (typingElement) {
    const roles = JSON.parse(typingElement.dataset.roles || '[]').filter(Boolean);

    if (roles.length > 0) {
        let roleIndex = 0;
        let charIndex = 0;
        let isDeleting = false;

        const type = () => {
            const currentRole = roles[roleIndex];
            const nextChar = isDeleting ? charIndex - 1 : charIndex + 1;
            typingElement.textContent = currentRole.slice(0, nextChar);
            charIndex = nextChar;

            let typingSpeed = isDeleting ? 45 : 95;

            if (!isDeleting && charIndex === currentRole.length) {
                isDeleting = true;
                typingSpeed = 1500;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                roleIndex = (roleIndex + 1) % roles.length;
                typingSpeed = 350;
            }

            window.setTimeout(type, typingSpeed);
        };

        window.setTimeout(type, 700);
    }
}

// ============================================
// DARK MODE TOGGLE
// ============================================
const darkModeToggle = document.getElementById('darkModeToggle');

function updateThemeToggle(theme) {
    if (!darkModeToggle) {
        return;
    }

    const icon = theme === 'dark' ? 'fa-sun' : 'fa-moon';
    const label = theme === 'dark' ? uiMessages.lightModeLabel : uiMessages.darkModeLabel;

    darkModeToggle.innerHTML = `<i class="fas ${icon}" aria-hidden="true"></i>`;
    darkModeToggle.setAttribute('aria-label', label);
}

const storedTheme = localStorage.getItem('theme');
const prefersDarkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
const initialTheme = storedTheme || (prefersDarkTheme ? 'dark' : 'light');
root.setAttribute('data-theme', initialTheme);
updateThemeToggle(initialTheme);

if (darkModeToggle) {
    darkModeToggle.addEventListener('click', () => {
        const currentTheme = root.getAttribute('data-theme') || 'light';
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';

        root.setAttribute('data-theme', nextTheme);
        localStorage.setItem('theme', nextTheme);
        updateThemeToggle(nextTheme);

        darkModeToggle.classList.add('is-rotating');
        window.setTimeout(() => darkModeToggle.classList.remove('is-rotating'), 280);
    });
}

// ============================================
// SCROLL PROGRESS INDICATOR
// ============================================
window.addEventListener('scroll', () => {
    const scrollProgress = document.getElementById('scrollProgress');
    if (!scrollProgress) {
        return;
    }

    const scrollableHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    if (scrollableHeight <= 0) {
        scrollProgress.style.width = '0%';
        return;
    }

    const scrolled = (window.scrollY / scrollableHeight) * 100;
    scrollProgress.style.width = `${Math.min(Math.max(scrolled, 0), 100)}%`;
});

// ============================================
// SCROLL ANIMATIONS (INTERSECTION OBSERVER)
// ============================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach((element) => observer.observe(element));

// ============================================
// SKILL BAR ANIMATION
// ============================================
const skillBars = document.querySelectorAll('.skill-progress');
const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            const percentage = entry.target.getAttribute('data-percentage');
            entry.target.style.width = `${percentage}%`;
        }
    });
}, { threshold: 0.5 });

skillBars.forEach((bar) => skillObserver.observe(bar));

// ============================================
// TIMELINE ANIMATION
// ============================================
const timelineItems = document.querySelectorAll('.timeline-item');
const timelineObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('timeline-visible');
        }
    });
}, { threshold: 0.2 });

timelineItems.forEach((item) => timelineObserver.observe(item));

// ============================================
// PROJECT FILTER
// ============================================
const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card[data-category]');

filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const filter = button.getAttribute('data-filter');

        filterButtons.forEach((btn) => btn.classList.remove('active'));
        button.classList.add('active');

        projectCards.forEach((card) => {
            const categories = (card.getAttribute('data-category') || '').split(' ');

            if (filter === 'all' || categories.includes(filter)) {
                card.style.display = 'grid';
                window.setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                }, 10);
            } else {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.96)';
                window.setTimeout(() => {
                    card.style.display = 'none';
                }, 220);
            }
        });
    });
});

// ============================================
// COPY TO CLIPBOARD
// ============================================
const copyButtons = document.querySelectorAll('.copy-btn');
copyButtons.forEach((button) => {
    button.addEventListener('click', async () => {
        const textToCopy = button.getAttribute('data-copy') || '';

        try {
            await navigator.clipboard.writeText(textToCopy);
            showNotification(uiMessages.copied, 'success');
        } catch (error) {
            showNotification(uiMessages.error, 'error');
        }
    });
});

// ============================================
// CARD TILT EFFECT
// ============================================
const tiltCards = document.querySelectorAll('.tilt-card');
tiltCards.forEach((card) => {
    card.addEventListener('mousemove', (event) => {
        const rect = card.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 16;
        const rotateY = (centerX - x) / 16;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.01, 1.01, 1.01)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    });
});

// ============================================
// SMOOTH SCROLL FOR SAME PAGE LINKS
// ============================================
document.querySelectorAll('a[href*="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
        const anchorUrl = new URL(anchor.href, window.location.origin);

        if (
            anchorUrl.pathname !== window.location.pathname ||
            anchorUrl.search !== window.location.search ||
            !anchorUrl.hash
        ) {
            return;
        }

        const target = document.querySelector(anchorUrl.hash);
        if (!target) {
            return;
        }

        event.preventDefault();
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

// ============================================
// PARALLAX ORBS
// ============================================
window.addEventListener('mousemove', (event) => {
    const orbs = document.querySelectorAll('.bg-orb');
    if (!orbs.length) {
        return;
    }

    const mouseX = event.clientX / window.innerWidth;
    const mouseY = event.clientY / window.innerHeight;

    orbs.forEach((orb, index) => {
        const speed = (index + 1) * 20;
        const x = (mouseX - 0.5) * speed;
        const y = (mouseY - 0.5) * speed;
        orb.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// ============================================
// STATS COUNTER ANIMATION
// ============================================
const stats = document.querySelectorAll('.stat-number');
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) {
            return;
        }

        const target = entry.target;
        const finalValue = Number(target.getAttribute('data-value') || '0');
        const suffix = target.getAttribute('data-suffix') || '';
        const duration = 1400;
        const increment = finalValue / (duration / 16);
        let currentValue = 0;

        const updateCounter = () => {
            currentValue += increment;
            if (currentValue < finalValue) {
                target.textContent = `${Math.floor(currentValue)}${suffix}`;
                requestAnimationFrame(updateCounter);
                return;
            }
            target.textContent = `${finalValue}${suffix}`;
        };

        updateCounter();
        statsObserver.unobserve(target);
    });
}, { threshold: 0.5 });

stats.forEach((stat) => statsObserver.observe(stat));

// ============================================
// LOADING ANIMATION
// ============================================
window.addEventListener('load', () => {
    const loader = document.querySelector('.page-loader');
    if (!loader) {
        return;
    }

    window.setTimeout(() => {
        loader.classList.add('fade-out');
        window.setTimeout(() => {
            loader.style.display = 'none';
        }, 500);
    }, 650);
});
