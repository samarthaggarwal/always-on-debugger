#!/usr/bin/env node

const { argv } = require('node:process');
const { exec, execSync, spawn, spawnSync } = require('child_process');
const { join } = require('path');

// npm run start -- "py -3.8 -m terminal"
// npm pack
// npm i -g aod-0.1.tgz
// $env:ANTHROPIC_API_KEY = "<key>"

async function run() {
  const [, , ...args] = argv;
  const command = args.join(' ');

  try {
    const child = execSync(`py -3.8 -m terminal "${command}"`, { stdio: 'inherit' });
  } catch (error) {
    console.log('Error happened', error);
  }
}

run();