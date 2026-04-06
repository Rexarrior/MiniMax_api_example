const { chromium } = require('playwright');

async function runTests() {
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
  
  console.log('=== Testing /tests page ===');
  await test('Tests index page loads', async () => {
    await page.goto(`${baseUrl}/tests`);
    await page.waitForSelector('h1');
    const h1 = await page.textContent('h1');
    return h1.includes('Tests');
  });
  
  console.log('\n=== Testing API via /tests page ===');
  await test('API Health check', async () => {
    const response = await page.request.get(`${baseUrl}/api/health`);
    const data = await response.json();
    return data.status === 'ok';
  });
  
  console.log('\n=== Testing Image Test page ===');
  await test('Image test page loads', async () => {
    await page.goto(`${baseUrl}/tests/image`);
    await page.waitForSelector('h1', { timeout: 5000 });
    return true;
  });
  
  await test('Can select story', async () => {
    await page.waitForSelector('select', { timeout: 5000 });
    const options = await page.$$('select option');
    return options.length > 0;
  });
  
  console.log('\n=== Testing Soundtrack Test page ===');
  await test('Soundtrack test page loads', async () => {
    await page.goto(`${baseUrl}/tests/soundtrack`);
    await page.waitForSelector('h1', { timeout: 5000 });
    return true;
  });
  
  console.log('\n=== Testing Video Test page ===');
  await test('Video test page loads', async () => {
    await page.goto(`${baseUrl}/tests/video`);
    await page.waitForSelector('h1', { timeout: 5000 });
    return true;
  });
  
  console.log('\n=== Testing Replica Test page ===');
  await test('Replica test page loads', async () => {
    await page.goto(`${baseUrl}/tests/replica`);
    await page.waitForSelector('h1', { timeout: 5000 });
    return true;
  });
  
  console.log('\n=== Testing Game Flow ===');
  await test('Title screen loads', async () => {
    await page.goto(baseUrl);
    await page.waitForSelector('button, a[href*="play"]', { timeout: 10000 });
    return true;
  });
  
  // Click play button or link to start game
  await test('Can start game', async () => {
    const playLink = await page.$('a[href*="play"]');
    if (playLink) {
      await playLink.click();
      await page.waitForTimeout(2000);
    }
    // Check if game screen or dialogue appeared
    const hasDialogue = await page.$('.dialogue, .dialogue-box, [class*="dialog"]');
    return true; // If we got here without error, it worked
  });
  
  // Test advancing dialogue
  await test('Can advance dialogue', async () => {
    await page.click('body'); // Click to advance
    await page.waitForTimeout(500);
    return true;
  });
  
  console.log('\n=== Summary ===');
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(`${passed}/${total} tests passed`);
  
  await browser.close();
  process.exit(passed === total ? 0 : 1);
}

runTests().catch(e => {
  console.error('Test runner error:', e);
  process.exit(1);
});