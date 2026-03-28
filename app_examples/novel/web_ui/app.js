class NovelGame {
    constructor() {
        this.currentScene = null;
        this.lastTimestamp = 0;
        this.dialogues = [];
        this.choices = [];
        this.isEnding = false;
        this.isWaitingForChoice = false;
        this.soundEnabled = true;
        this.currentMusicSrc = null;
        this.isSkipping = false;
        this.cachedDurations = new Map();
        this.userInteracted = false;
        
        this.titleScreen = document.getElementById('title-screen');
        this.gameScreen = document.getElementById('game-screen');
        this.endingScreen = document.getElementById('ending-screen');
        this.bgLayer = document.getElementById('background-layer');
        this.charLayer = document.getElementById('character-layer');
        this.speakerEl = document.getElementById('speaker-name');
        this.dialogueEl = document.getElementById('dialogue-text');
        this.choicesEl = document.getElementById('choices-container');
        this.musicEl = document.getElementById('bg-music');
        this.voiceEl = document.getElementById('voice-audio');
        this.soundBtn = document.getElementById('sound-btn');
        
        this.setupEventListeners();
        this.startPolling();
    }

    setupEventListeners() {
        document.getElementById('start-btn').addEventListener('click', () => {
            this.showSoundPrompt();
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

        this.gameScreen.addEventListener('click', () => {
            if (this.dialogueIndex < this.dialogues.length) {
                this.isSkipping = true;
                this.voiceEl.pause();
                this.voiceEl.currentTime = 0;
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

    showSoundPrompt() {
        const modal = document.getElementById('sound-prompt');
        modal.classList.remove('hidden');
        
        const handleSoundChoice = (enable) => {
            modal.classList.add('hidden');
            this.soundEnabled = enable;
            this.updateSoundButton();
            this.titleScreen.classList.add('hidden');
            this.gameScreen.classList.remove('hidden');
            
            if (enable) {
                this.userInteracted = true;
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/api/scene', false);
                xhr.send(null);
                if (xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText);
                    if (data.music_url) {
                        this.playMusic(data.music_url);
                    }
                }
            }
            
            this.fetchScene();
        };
        
        document.getElementById('sound-yes').onclick = () => handleSoundChoice(true);
        document.getElementById('sound-no').onclick = () => handleSoundChoice(false);
    }

    startPolling() {
        setInterval(() => this.poll(), 500);
    }

    async getAudioDuration(audioUrl) {
        if (this.cachedDurations.has(audioUrl)) {
            return this.cachedDurations.get(audioUrl);
        }
        try {
            const response = await fetch(audioUrl);
            const arrayBuffer = await response.arrayBuffer();
            const audioContext = new AudioContext();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            const durationMs = audioBuffer.duration * 1000;
            this.cachedDurations.set(audioUrl, durationMs);
            return durationMs;
        } catch {
            return null;
        }
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
            this.isSkipping = false;
            
            if (data.title) {
                document.getElementById('game-title').textContent = data.title;
            }
            
            if (data.background_url) {
                this.bgLayer.style.backgroundImage = `url('${data.background_url}')`;
                this.bgLayer.classList.remove('loading');
            }
            
            if (data.music_url) {
                this.playMusic(data.music_url);
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

    playMusic(musicUrl) {
        if (musicUrl === this.currentMusicSrc && !this.musicEl.paused) {
            return;
        }
        this.currentMusicSrc = musicUrl;
        this.musicEl.src = musicUrl;
        this.musicEl.load();
        if (this.soundEnabled) {
            const tryPlay = () => {
                this.musicEl.play().catch((err) => {
                    console.warn('Music play failed:', err);
                });
            };
            if (this.userInteracted) {
                this.userInteracted = false;
                tryPlay();
            } else if (this.musicEl.readyState >= 3) {
                tryPlay();
            } else {
                const onCanPlay = () => {
                    this.musicEl.removeEventListener('canplay', onCanPlay);
                    tryPlay();
                };
                this.musicEl.addEventListener('canplay', onCanPlay);
            }
        }
    }

    setCharacterImage(imageUrl) {
        if (this.charLayer.style.backgroundImage === `url('${imageUrl}')`) {
            this.charLayer.classList.add('visible');
            return;
        }
        this.charLayer.classList.remove('visible');
        setTimeout(() => {
            this.charLayer.style.backgroundImage = `url('${imageUrl}')`;
            this.charLayer.classList.add('visible');
        }, 50);
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
            this.setCharacterImage(d.character_image_url);
        } else {
            this.charLayer.classList.remove('visible');
        }
        
        this.dialogueEl.textContent = '';
        this.choicesEl.innerHTML = '';
        
        if (this.isSkipping) {
            this.voiceEl.pause();
            this.voiceEl.currentTime = 0;
            this.typeText(d.text, () => {
                this.isSkipping = false;
                this.dialogueIndex++;
                setTimeout(() => this.showNextDialogue(), 100);
            });
        } else if (d.voice_url && this.soundEnabled) {
            this.playVoiceWithSync(d);
        } else {
            this.typeText(d.text, () => {
                this.dialogueIndex++;
                setTimeout(() => this.showNextDialogue(), 500);
            });
        }
    }

    async playVoiceWithSync(dialogue) {
        const voiceDuration = dialogue.voice_duration_ms || dialogue.text.length * 50;
        const charDuration = voiceDuration / dialogue.text.length;
        
        const onReady = () => {
            this.voiceEl.play().catch((err) => {
                console.warn('Voice play failed:', err);
            });
            this.typeTextSync(dialogue.text, charDuration, () => {
                this.dialogueIndex++;
                setTimeout(() => this.showNextDialogue(), 300);
            });
        };
        
        this.voiceEl.src = dialogue.voice_url;
        
        if (this.voiceEl.readyState >= 4) {
            onReady();
        } else {
            const onCanPlayThrough = () => {
                this.voiceEl.removeEventListener('canplaythrough', onCanPlayThrough);
                onReady();
            };
            this.voiceEl.addEventListener('canplaythrough', onCanPlayThrough);
        }
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

    typeTextSync(text, charDuration, callback) {
        let i = 0;
        
        const type = () => {
            if (i < text.length) {
                this.dialogueEl.textContent += text.charAt(i);
                i++;
                setTimeout(type, charDuration);
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