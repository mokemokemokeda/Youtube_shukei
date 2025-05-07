import requests
import pandas as pd
import time
import os
import subprocess

# Puppeteerスクリプト
script = """
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.goto('https://subscribercounter.com/fullscreen/UCXRqdYwNwa0ZGxScFaUnStg', { waitUntil: 'domcontentloaded' });

  await page.waitForSelector('.odometer-value', { timeout: 60000 });
  await page.waitForFunction(
    'document.querySelector(".odometer-value").textContent.trim() !== "0"',
    { timeout: 60000 }
  );

  const subscriberCount = await page.$$eval('.odometer-value', elements =>
    elements.map(el => el.textContent.trim()).join('')
  );

  console.log(subscriberCount);  // 数字のみ出力
  await browser.close();
})();
"""

# スクリプトを書き込み
with open("scrape.js", "w") as file:
    file.write(script)

# 実行して登録者数を取得
result = subprocess.run(['node', 'scrape.js'], capture_output=True, text=True)
subscriber_count_str = result.stdout.strip()
