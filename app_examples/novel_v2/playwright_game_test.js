const { chromium } = require('playwright');

async function testGameFlow() {
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
  
  console.log('=== Testing Game Flow ===');
  
  // Start game
  await test('Can start game', async () => {
    await page.goto(`${baseUrl}/play/demo`);
    await page.waitForTimeout(2000); // Wait for API call
    return true;
  });
  
  // Check first dialogue is shown
  await test('First dialogue is shown', async () => {
    await page.waitForTimeout(500);
    const content = await page.content();
    return content.includes('You wake up') || content.includes('narrator');
  });
  
  // Advance dialogue
  await test('Can advance to second dialogue', async () => {
    await page.click('body');
    await page.waitForTimeout(500);
    return true;
  });
  
  // Check second dialogue text
  await test('Second dialogue text visible', async () => {
    await page.waitForTimeout(500);
    const content = await page.content();
    return content.includes('dense forest') || content.includes('middle of a');
  });
  
  // Check choices are shown after dialogues
  await test('Choices are shown after dialogues', async () => {
    await page.waitForTimeout(500);
    const content = await page.content();
    return content.includes('Look around') || content.includes('Call out');
  });
  
  // Make a choice
  await test('Can make a choice', async () => {
    // Find and click the first choice
    const choice = await page.$('text=Look around');
    if (choice) {
      await choice.click();
      await page.waitForTimeout(2000); // Wait for scene transition
      return true;
    }
    return false;
  });
  
  // Verify scene changed
  await test('Scene changed after choice', async () => {
    const content = await page.content();
    // New scene should have different content
    return content.includes('carefully') || content.includes('clearing') || content.includes('shining');
  });
  
  // Check background image is displayed
  await test('Background image is visible in game', async () => {
    const bgImg = await page.$('.background-layer img, .game-screen img, [class*="background"] img');
    return bgImg !== null;
  });
  
  // Check music is set
  await test('Music element exists', async () => {
    const audio = await page.$('audio');
    return audio !== null;
  });
  
  console.log('\n=== Summary ===');
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(`${passed}/${total} tests passed`);
  
  await browser.close();
  process.exit(passed === total ? 0 : 1);
}

testGameFlow().catch(e => {
  console.error('Test runner error:', e);
  process.exit(1);
});