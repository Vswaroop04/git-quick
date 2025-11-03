#!/usr/bin/env node

/**
 * Git Quick - NPM wrapper for Python CLI
 * This is a Node.js wrapper that calls the Python implementation
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Check if Python is available
function checkPython() {
  const pythonCommands = ['python3', 'python'];

  for (const cmd of pythonCommands) {
    try {
      const result = spawn(cmd, ['--version'], { stdio: 'pipe' });
      if (result) {
        return cmd;
      }
    } catch (e) {
      continue;
    }
  }

  console.error('Error: Python 3.8+ is required but not found.');
  console.error('Please install Python from https://www.python.org/');
  process.exit(1);
}

// Check if git-quick Python package is installed
function checkGitQuickInstalled(pythonCmd) {
  const check = spawn(pythonCmd, ['-c', 'import git_quick'], { stdio: 'pipe' });

  return new Promise((resolve) => {
    check.on('close', (code) => {
      resolve(code === 0);
    });
  });
}

// Install git-quick Python package
function installGitQuick(pythonCmd) {
  console.log('Installing git-quick Python package...');

  const install = spawn(pythonCmd, ['-m', 'pip', 'install', 'git-quick'], {
    stdio: 'inherit'
  });

  return new Promise((resolve, reject) => {
    install.on('close', (code) => {
      if (code === 0) {
        console.log('✓ git-quick installed successfully');
        resolve();
      } else {
        console.error('✗ Failed to install git-quick');
        reject(new Error('Installation failed'));
      }
    });
  });
}

// Run the Python CLI
async function runGitQuick() {
  const pythonCmd = checkPython();

  // Check if git-quick is installed
  const isInstalled = await checkGitQuickInstalled(pythonCmd);

  if (!isInstalled) {
    console.log('git-quick Python package not found.');
    try {
      await installGitQuick(pythonCmd);
    } catch (e) {
      console.error('\nManual installation:');
      console.error('  pip install git-quick');
      process.exit(1);
    }
  }

  // Run git-quick with all arguments
  const args = process.argv.slice(2);
  const gitQuick = spawn(pythonCmd, ['-m', 'git_quick.cli', ...args], {
    stdio: 'inherit'
  });

  gitQuick.on('close', (code) => {
    process.exit(code);
  });
}

// Main
runGitQuick().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
