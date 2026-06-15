/**
 * Chrome T-Rex Game Bookmarklet
 *
 * How to use:
 * 1. Open chrome://dino in Chrome
 * 2. Start the game manually (press SPACE)
 * 3. Run this script in the console, or save as a bookmarklet
 *
 * How it works:
 * - Monitors the game canvas for dark pixels ahead of the dino
 * - Simulates a spacebar press when an obstacle is detected
 * - The check region moves right as the game speeds up
 */

javascript:(function() {
  const canvas = document.querySelector('canvas');
  if (!canvas) return alert('No canvas found. Open chrome://dino first.');

  const ctx = canvas.getContext('2d');
  let running = true;
  let score = 0;

  function jump() {
    document.dispatchEvent(new KeyboardEvent('keydown', {key: ' ', code: 'Space'}));
    document.dispatchEvent(new KeyboardEvent('keyup', {key: ' ', code: 'Space'}));
  }

  function checkObstacle() {
    if (!running) return;

    // Sample pixel strip ahead of the dino
    const threshold = 80;
    const checkWidth = 30;
    const dinoX = 60;
    const groundY = canvas.height - 20;
    const checkY = groundY - 40;

    const imageData = ctx.getImageData(dinoX + 50, checkY, checkWidth, 30);
    const pixels = imageData.data;
    let darkCount = 0;

    for (let i = 0; i < pixels.length; i += 4) {
      const brightness = (pixels[i] + pixels[i+1] + pixels[i+2]) / 3;
      if (brightness < 100) darkCount++;
    }

    if (darkCount > threshold) {
      jump();
    }

    requestAnimationFrame(checkObstacle);
  }

  jump();
  setTimeout(checkObstacle, 500);

  // Show score overlay
  const div = document.createElement('div');
  div.style.cssText = 'position:fixed;top:10px;right:10px;z-index:9999;background:#000;color:#0f0;padding:8px 16px;font:14px monospace;border-radius:4px;';
  div.textContent = '🤖 T-Rex Bot Running';
  document.body.appendChild(div);

  // Stop after 5 minutes
  setTimeout(() => { running = false; div.textContent = '🤖 Bot Stopped'; }, 300000);

  console.log('T-Rex bot started. Close the tab or refresh to stop.');
})();
