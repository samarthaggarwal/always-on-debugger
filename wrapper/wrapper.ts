const { argv } = require('node:process');
import { exec, execSync, spawn, spawnSync } from 'child_process';
import { join } from 'path';

const path = join('terminal');
console.log(path);

async function run() {
  console.log(argv);

  const child = execSync(`py -3.8 -m ${path}`, { stdio: 'inherit' });
  // const child = execSync(`node somethinsg.js`, { stdio: 'inherit' });

  // child.on('exit', () => {
  //   console.log('exited now');
  // });

  // child.on('error', (error) => {
  //   console.log('Error happened!', error);
  // });
}

run();
