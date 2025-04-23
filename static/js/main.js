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
        
        // making hexagon
        const icon = document.createElement('div');
        icon.className = 'card-icon';
        icon.innerHTML = '<svg viewBox="0 0 100 100"><polygon points="50 0, 93.3 25, 93.3 75, 50 100, 6.7 75, 6.7 25" fill="gold" stroke="black" /></svg>';
        
        // card content + content goes into card
        const content = document.createElement('div');
        content.className = 'card-content';
        content.textContent = sentence.trim() + '.';
        
        card.appendChild(icon);
        card.appendChild(content);
        cardsContainer.appendChild(card);
        
        // on hover
        card.addEventListener('mouseenter', function() {
            this.classList.add('expanded');
        });
        
        // off hover
        card.addEventListener('mouseleave', function() {
            this.classList.remove('expanded');
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