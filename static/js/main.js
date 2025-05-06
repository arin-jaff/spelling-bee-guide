document.addEventListener('DOMContentLoaded', function() {
    // if we're on a learn page, we engage interactivity
    if (document.querySelector('.lesson-content')) {
        createInteractiveElements();
    }
});

function createInteractiveElements() {
    const lessonContent = document.querySelector('.lesson-content');
    const lessonText = lessonContent.textContent.trim();
    
    lessonContent.innerHTML = '';
    
    // we separate content for cards via . delimiter splits
    const sentences = lessonText.split('.').filter(sentence => sentence.trim().length > 0);
    
    // cards + container for each sentence
    const cardsContainer = document.createElement('div');
    cardsContainer.className = 'interactive-cards';

    sentences.forEach((sentence, index) => {
        const card = document.createElement('div');
        card.className = 'interactive-card';
        card.setAttribute('data-index', index);
        
        // Add number to card
        const number = document.createElement('div');
        number.className = 'card-number';
        number.textContent = index + 1;
        number.style.position = 'absolute';
        number.style.top = '8px';
        number.style.left = '12px';
        number.style.fontWeight = 'bold';
        number.style.background = 'rgba(255,255,255,0.8)';
        number.style.borderRadius = '50%';
        number.style.width = '24px';
        number.style.height = '24px';
        number.style.display = 'flex';
        number.style.alignItems = 'center';
        number.style.justifyContent = 'center';
        number.style.zIndex = '2';
        
        // making hexagon
        const icon = document.createElement('div');
        icon.className = 'card-icon';
        icon.innerHTML = '<svg viewBox="0 0 100 100"><polygon points="50 0, 93.3 25, 93.3 75, 50 100, 6.7 75, 6.7 25" fill="gold" stroke="black" /></svg>';
        
        // card content + content goes into card
        const content = document.createElement('div');
        content.className = 'card-content';
        content.textContent = sentence.trim() + '.';
        // content is hidden by default, shown on hover
        content.style.opacity = '0';
        content.style.transition = 'opacity 0.3s';
        content.style.pointerEvents = 'none';
        
        card.appendChild(number);
        card.appendChild(icon);
        card.appendChild(content);
        cardsContainer.appendChild(card);
        
        // on hover
        card.addEventListener('mouseenter', function() {
            content.style.opacity = '1';
        });
        
        // off hover
        card.addEventListener('mouseleave', function() {
            content.style.opacity = '0';
        });
        
        // on click
        card.addEventListener('click', function() {
            this.classList.toggle('active');
            document.querySelectorAll('.interactive-card.active').forEach(activeCard => {
                if (activeCard !== this) {
                    activeCard.classList.remove('active');
                }
            });
        });
    });
    
    // cards container goes to the lesson content
    lessonContent.appendChild(cardsContainer);
}