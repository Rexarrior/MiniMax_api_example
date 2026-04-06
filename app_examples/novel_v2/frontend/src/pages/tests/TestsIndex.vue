<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { novelApi } from '../../api/novelApi'

const stories = ref<any[]>([])
const selectedStory = ref('demo')
const testResults = ref<Record<string, { pass: boolean; message: string }>>({})

onMounted(async () => {
  try {
    stories.value = await novelApi.listStories()
    if (stories.value.length > 0) {
      selectedStory.value = stories.value[0].id
    }
  } catch (e) {
    console.error('Failed to load stories:', e)
  }
})

function navigateTo(path: string) {
  window.location.href = path
}

async function runTest(name: string, testFn: () => Promise<boolean>) {
  try {
    const result = await testFn()
    testResults.value[name] = { pass: result, message: result ? 'PASS' : 'FAIL' }
  } catch (e: any) {
    testResults.value[name] = { pass: false, message: `ERROR: ${e.message}` }
  }
}

async function testApiHealth() {
  const res = await novelApi.healthCheck()
  return res.status === 'ok'
}

async function testListStories() {
  const s = await novelApi.listStories()
  return s.length > 0
}

async function testStartGame() {
  const session = await novelApi.startGame({ story_id: selectedStory.value })
  return !!session.session_id
}

async function testGetScene() {
  const session = await novelApi.startGame({ story_id: selectedStory.value })
  const scene = await novelApi.getScene(session.session_id)
  return scene && scene.dialogues && scene.dialogues.length > 0
}

async function testBackgroundImage() {
  const session = await novelApi.startGame({ story_id: selectedStory.value })
  const scene = await novelApi.getScene(session.session_id)
  return !!scene.background_url
}

async function testMusicUrl() {
  const session = await novelApi.startGame({ story_id: selectedStory.value })
  const scene = await novelApi.getScene(session.session_id)
  return !!scene.music_url
}

async function testAdvanceDialogue() {
  const session = await novelApi.startGame({ story_id: selectedStory.value })
  await novelApi.advanceDialogue()
  const scene = await novelApi.getScene(session.session_id)
  // After advance, dialogue_index should be 1
  return scene.dialogues.length >= 1
}

async function testChoiceTransition() {
  const session = await novelApi.startGame({ story_id: selectedStory.value })
  const scene1 = await novelApi.getScene(session.session_id)
  const firstChoice = scene1.choices?.[0]
  if (!firstChoice) return false
  
  await novelApi.makeChoice(0)
  const scene2 = await novelApi.getScene(session.session_id)
  // Should transition to different scene
  return scene2.current_scene_id !== scene1.scene_id
}

async function runAllTests() {
  testResults.value = {}
  await runTest('API Health', testApiHealth)
  await runTest('List Stories', testListStories)
  await runTest('Start Game', testStartGame)
  await runTest('Get Scene', testGetScene)
  await runTest('Background Image URL', testBackgroundImage)
  await runTest('Music URL', testMusicUrl)
  await runTest('Advance Dialogue', testAdvanceDialogue)
  await runTest('Choice Transition', testChoiceTransition)
}
</script>

<template>
  <div class="tests-page">
    <h1>🧪 Visual Novel Tests</h1>
    
    <div class="nav-links">
      <router-link to="/tests/image">📷 Image Test</router-link>
      <router-link to="/tests/video">🎬 Video Test</router-link>
      <router-link to="/tests/soundtrack">🎵 Soundtrack Test</router-link>
      <router-link to="/tests/replica">🎤 Replica Test</router-link>
    </div>

    <div class="test-section">
      <h2>Automated API Tests</h2>
      <p>Story: <select v-model="selectedStory">
        <option v-for="s in stories" :key="s.id" :value="s.id">{{ s.title }}</option>
      </select></p>
      
      <button @click="runAllTests" class="run-btn">▶️ Run All Tests</button>
      
      <div class="results">
        <div 
          v-for="(result, name) in testResults" 
          :key="name"
          class="result-item"
          :class="{ pass: result.pass, fail: !result.pass }"
        >
          <span class="status">{{ result.pass ? '✅' : '❌' }}</span>
          <span class="name">{{ name }}</span>
          <span class="message">{{ result.message }}</span>
        </div>
      </div>
    </div>

    <div class="manual-section">
      <h2>Manual Browser Tests</h2>
      <p>Open these pages in browser to test manually:</p>
      <ul>
        <li><a href="/tests/image" target="_blank">/tests/image</a> - Background and character images</li>
        <li><a href="/tests/video" target="_blank">/tests/video</a> - Video playback</li>
        <li><a href="/tests/soundtrack" target="_blank">/tests/soundtrack</a> - Background music</li>
        <li><a href="/tests/replica" target="_blank">/tests/replica</a> - Voice/dialogue audio</li>
      </ul>
      <p>Or play the actual game:</p>
      <ul>
        <li><a :href="`/?story=${selectedStory}`" target="_blank">Play Game</a></li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.tests-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  color: #fff;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.nav-links {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.nav-links a {
  padding: 10px 20px;
  background: #333;
  border-radius: 8px;
  color: #fff;
  text-decoration: none;
}

.nav-links a:hover {
  background: #555;
}

.test-section, .manual-section {
  background: #1a1a1a;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.run-btn {
  padding: 12px 24px;
  background: #4CAF50;
  border: none;
  border-radius: 6px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  margin: 15px 0;
}

.run-btn:hover {
  background: #45a049;
}

.results {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 15px;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 6px;
}

.result-item.pass {
  background: rgba(76, 175, 80, 0.2);
}

.result-item.fail {
  background: rgba(244, 67, 54, 0.2);
}

.status {
  font-size: 18px;
}

.name {
  font-weight: bold;
  flex: 1;
}

.message {
  color: #888;
  font-size: 14px;
}

.manual-section ul {
  list-style: none;
  padding: 0;
}

.manual-section li {
  padding: 8px 0;
}

.manual-section a {
  color: #4CAF50;
}
</style>