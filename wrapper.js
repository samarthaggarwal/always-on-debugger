#!/usr/bin/env node

const { argv } = require('node:process');
const { exec, execSync, spawn, spawnSync } = require('child_process');
const { join } = require('path');

const path = join('terminal');
// console.log(path);

// npm run start -- "py -3.8 -m terminal"
// npm pack
// npm i -g aod-0.1.tgz
//

async function run() {
  // console.log(argv);
  const [, , ...args] = argv;
  const command = args.join(' ');

  try {
    // const child = execSync(`py -3.8 -m ${path}`, { stdio: 'inherit' });
    const child = execSync(`py -3.8 -m terminal "${command}"`, { stdio: 'inherit' });
  } catch (error) {
    console.log('Error happened', error);
  }

  // const child = execSync(`node somethinsg.js`, { stdio: 'inherit' });

  // child.on('exit', () => {
  //   console.log('exited now');
  // });

  // child.on('error', (error) => {
  //   console.log('Error happened!', error);
  // });
}

run();
