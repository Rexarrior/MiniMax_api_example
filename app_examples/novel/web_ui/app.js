class NovelGame {
    constructor() {
        this.currentScene = null;
        this.lastTimestamp = 0;
        this.dialogues = [];
        this.choices = [];
        this.isEnding = false;
        this.isWaitingForChoice = false;
        this.soundEnabled = true;
        
        this.titleScreen = document.getElementById('title-screen');
        this.gameScreen = document.getElementById('game-screen');
        this.endingScreen = document.getElementById('ending-screen');
        this.bgLayer = document.getElementById('background-layer');
        this.charLayer = document.getElementById('character-layer');
        this.speakerEl = document.getElementById('speaker-name');
        this.dialogueEl = document.getElementById('dialogue-text');
        this.choicesEl = document.getElementById('choices-container');
        this.musicEl = document.getElementById('bg-music');
        this.soundBtn = document.getElementById('sound-btn');
        
        this.setupEventListeners();
        this.startPolling();
    }

    setupEventListeners() {
        document.getElementById('start-btn').addEventListener('click', () => {
            this.titleScreen.classList.add('hidden');
            this.gameScreen.classList.remove('hidden');
            this.soundEnabled = true;
            this.updateSoundButton();
            this.fetchScene();
        });
        
        document.getElementById('restart-btn').addEventListener('click', () => {
            location.reload();
        });
        
        this.soundBtn.addEventListener('click', () => {
            this.soundEnabled = !this.soundEnabled;
            this.updateSoundButton();
            if (this.soundEnabled) {
                this.musicEl.play().catch(() => {});
            } else {
                this.musicEl.pause();
            }
        });
    }

    updateSoundButton() {
        if (this.soundEnabled) {
            this.soundBtn.textContent = '🔊';
            this.soundBtn.classList.remove('muted');
            this.musicEl.muted = false;
        } else {
            this.soundBtn.textContent = '🔇';
            this.soundBtn.classList.add('muted');
            this.musicEl.muted = true;
        }
    }

    startPolling() {
        setInterval(() => this.poll(), 500);
    }

    async fetchScene() {
        try {
            const resp = await fetch('/api/scene');
            const data = await resp.json();
            this.handleScene(data);
        } catch (err) {
            console.error('Failed to fetch scene:', err);
        }
    }

    async poll() {
        try {
            const resp = await fetch('/api/poll');
            const data = await resp.json();
            if (data.timestamp > this.lastTimestamp) {
                this.lastTimestamp = data.timestamp;
                this.handleScene(data);
            }
        } catch (err) {
            // Silent fail on poll
        }
    }

    handleScene(data) {
        if (!data.scene_id) return;

        if (data.scene_id !== this.currentScene) {
            this.currentScene = data.scene_id;
            this.dialogues = data.dialogues || [];
            this.choices = data.choices || [];
            this.isEnding = data.is_ending;
            this.dialogueIndex = 0;
            this.isWaitingForChoice = false;
            
            if (data.title) {
                document.getElementById('game-title').textContent = data.title;
            }
            
            if (data.background_url) {
                this.bgLayer.style.backgroundImage = `url('${data.background_url}')`;
                this.bgLayer.classList.remove('loading');
            }
            
            if (data.music_url) {
                this.musicEl.src = data.music_url;
                if (this.soundEnabled) {
                    this.musicEl.play().catch(() => {});
                }
            } else {
                this.musicEl.pause();
            }
            
            if (this.isEnding) {
                this.showEnding();
            } else if (this.dialogues.length > 0) {
                this.showNextDialogue();
            } else if (this.choices.length > 0) {
                this.showChoices();
            }
        }
    }

    showNextDialogue() {
        if (this.isWaitingForChoice) return;
        
        if (this.dialogueIndex >= this.dialogues.length) {
            if (this.choices.length > 0) {
                this.showChoices();
            } else {
                this.showEnding();
            }
            return;
        }
        
        const d = this.dialogues[this.dialogueIndex];
        this.speakerEl.textContent = d.speaker;
        this.speakerEl.className = d.speaker === 'narrator' ? 'narrator' : '';
        
        if (d.character_image_url) {
            this.charLayer.style.backgroundImage = `url('${d.character_image_url}')`;
            this.charLayer.classList.add('visible');
        } else {
            this.charLayer.classList.remove('visible');
        }
        
        this.dialogueEl.textContent = '';
        this.choicesEl.innerHTML = '';
        
        this.typeText(d.text, () => {
            this.dialogueIndex++;
            setTimeout(() => this.showNextDialogue(), 500);
        });
    }

    typeText(text, callback) {
        let i = 0;
        const speed = 30;
        
        const type = () => {
            if (i < text.length) {
                this.dialogueEl.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                callback();
            }
        };
        
        type();
    }

    showChoices() {
        this.choicesEl.innerHTML = '';
        this.dialogueEl.textContent = '';
        this.charLayer.classList.remove('visible');
        
        this.choices.forEach((choice) => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            btn.textContent = choice.text;
            btn.addEventListener('click', () => this.selectChoice(choice.index));
            this.choicesEl.appendChild(btn);
        });
    }

    async selectChoice(idx) {
        this.isWaitingForChoice = true;
        
        try {
            await fetch('/api/choice', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({choice_index: idx})
            });
        } catch (err) {
            console.error('Failed to send choice:', err);
        }
        
        this.choicesEl.innerHTML = '';
        this.speakerEl.textContent = '';
        this.dialogueEl.textContent = '...';
        this.charLayer.classList.remove('visible');
    }

    showEnding() {
        this.gameScreen.classList.add('hidden');
        this.endingScreen.classList.remove('hidden');
        this.musicEl.pause();
        this.charLayer.classList.remove('visible');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    new NovelGame();
});