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

  const terminalScript = join(__dirname, 'terminal.py');

  // const terminalCommand =
  //   process.platform === 'win32' ? `py -3.11 -m terminal "${command}"` : `python terminal "${command}"`;

  const terminalCommand = `python ${terminalScript} "${command}"`;

  try {
    const child = execSync(terminalCommand, { stdio: 'inherit' });
  } catch (error) {
    console.log('Error happened', error);
  }
}

run();
