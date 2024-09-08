const { argv } = require('node:process');
import { exec, execSync, spawn } from 'child_process';
import { join } from 'path';

const path = join('terminal');
console.log(path);

async function run() {
  console.log(argv);
  try {
    execSync(`py -3.8 -m ${path}`);
  } catch (error) {
    console.log(error);
  } finally {
    console.log('done');
  }
}

run();
