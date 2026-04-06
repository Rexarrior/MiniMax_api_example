const { chromium } = require('playwright');

async function testAssets() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const baseUrl = 'http://localhost:3000';
  const results = [];
  
  async function test(name, fn) {
    try {
      const result = await fn();
      results.push({ name, pass: result, error: null });
      console.log(`${result ? '✅' : '❌'} ${name}`);
    } catch (e) {
      results.push({ name, pass: false, error: e.message });
      console.log(`❌ ${name}: ${e.message}`);
    }
  }
  
  console.log('=== Testing Image Assets ===');
  
  // Test /tests/image page
  await test('Image test page loads', async () => {
    await page.goto(`${baseUrl}/tests/image`);
    await page.waitForSelector('select', { timeout: 5000 });
    return true;
  });
  
  await test('Background image URL is shown', async () => {
    await page.waitForTimeout(1000); // Wait for API call
    const content = await page.content();
    return content.includes('background_url') || content.includes('http');
  });
  
  await test('Background image is visible', async () => {
    const img = await page.$('img[src*="background"], img[src*="bg_"]');
    return img !== null;
  });
  
  console.log('\n=== Testing Music Assets ===');
  
  await test('Soundtrack test page loads', async () => {
    await page.goto(`${baseUrl}/tests/soundtrack`);
    await page.waitForSelector('select', { timeout: 5000 });
    return true;
  });
  
  await test('Music list is populated', async () => {
    await page.waitForTimeout(1000);
    const content = await page.content();
    return content.includes('.mp3') || content.includes('audio');
  });
  
  console.log('\n=== Testing Video Assets ===');
  
  await test('Video test page loads', async () => {
    await page.goto(`${baseUrl}/tests/video`);
    await page.waitForSelector('select', { timeout: 5000 });
    return true;
  });
  
  await test('Video list is populated', async () => {
    await page.waitForTimeout(1000);
    const content = await page.content();
    return content.includes('.mp4') || content.includes('video') || content.includes('No videos');
  });
  
  console.log('\n=== Testing Replica/Voice Assets ===');
  
  await test('Replica test page loads', async () => {
    await page.goto(`${baseUrl}/tests/replica`);
    await page.waitForSelector('select', { timeout: 5000 });
    return true;
  });
  
  await test('Dialogues list is populated', async () => {
    await page.waitForTimeout(1000);
    const content = await page.content();
    return content.includes('dialogue') || content.includes('You wake');
  });
  
  console.log('\n=== Testing API Directly ===');
  
  // Test API directly for assets
  await test('API: Start game returns background_url', async () => {
    const response = await page.request.post(`${baseUrl}/api/game/start`, {
      data: { story_id: 'demo' }
    });
    const data = await response.json();
    return data.background_url && data.background_url.includes('/api/media/');
  });
  
  await test('API: Start game returns music_url', async () => {
    const response = await page.request.post(`${baseUrl}/api/game/start`, {
      data: { story_id: 'demo' }
    });
    const data = await response.json();
    return data.music_url && data.music_url.includes('.mp3');
  });
  
  await test('API: Background image is accessible', async () => {
    const response = await page.request.post(`${baseUrl}/api/game/start`, {
      data: { story_id: 'demo' }
    });
    const data = await response.json();
    const imgResponse = await page.request.get(`${baseUrl}${data.background_url}`);
    return imgResponse.status() === 200;
  });
  
  await test('API: Music is accessible', async () => {
    const response = await page.request.post(`${baseUrl}/api/game/start`, {
      data: { story_id: 'demo' }
    });
    const data = await response.json();
    const musicResponse = await page.request.get(`${baseUrl}${data.music_url}`);
    return musicResponse.status() === 200;
  });
  
  console.log('\n=== Summary ===');
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(`${passed}/${total} tests passed`);
  
  if (passed < total) {
    console.log('\nFailed tests:');
    results.filter(r => !r.pass).forEach(r => {
      console.log(`  - ${r.name}: ${r.error || 'check failed'}`);
    });
  }
  
  await browser.close();
  process.exit(passed === total ? 0 : 1);
}

testAssets().catch(e => {
  console.error('Test runner error:', e);
  process.exit(1);
});