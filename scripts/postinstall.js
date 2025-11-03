#!/usr/bin/env node

/**
 * Post-install script for npm package
 * Ensures Python package is installed
 */

const { execSync } = require('child_process');
const os = require('os');

console.log('');
console.log('╔═══════════════════════════════════════════════════════════╗');
console.log('║           Git Quick - Post Install                        ║');
console.log('╚═══════════════════════════════════════════════════════════╝');
console.log('');

// Check Python
function checkPython() {
  const pythonCommands = ['python3', 'python'];

  for (const cmd of pythonCommands) {
    try {
      const version = execSync(`${cmd} --version`, { encoding: 'utf8' });
      const match = version.match(/Python (\d+)\.(\d+)/);
      if (match) {
        const major = parseInt(match[1]);
        const minor = parseInt(match[2]);
        if (major >= 3 && minor >= 8) {
          console.log(`✓ Found ${version.trim()}`);
          return cmd;
        }
      }
    } catch (e) {
      continue;
    }
  }

  console.error('✗ Python 3.8+ is required');
  console.error('  Install from: https://www.python.org/');
  return null;
}

// Install Python package
function installPythonPackage(pythonCmd) {
  console.log('\nInstalling git-quick Python package...');

  try {
    // First try to install from PyPI
    execSync(`${pythonCmd} -m pip install git-quick`, {
      stdio: 'inherit',
      encoding: 'utf8'
    });
    console.log('✓ Python package installed from PyPI');
    return true;
  } catch (e) {
    // If PyPI fails, try installing from the npm package directory
    try {
      const path = require('path');
      const packageDir = path.join(__dirname, '..');
      console.log('⚠ PyPI not available, installing from local package...');
      execSync(`${pythonCmd} -m pip install "${packageDir}"`, {
        stdio: 'inherit',
        encoding: 'utf8'
      });
      console.log('✓ Python package installed from local directory');
      return true;
    } catch (e2) {
      console.warn('⚠ Could not install Python package automatically');
      console.warn('  Please run manually: pip install git-quick');
      console.warn('  Or from this directory: pip install .');
      return false;
    }
  }
}

// Main
const pythonCmd = checkPython();

if (pythonCmd) {
  installPythonPackage(pythonCmd);

  console.log('');
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║              ✨ Installation Complete! ✨                 ║');
  console.log('╚═══════════════════════════════════════════════════════════╝');
  console.log('');
  console.log('Quick Start:');
  console.log('  git-quick              # Quick commit & push');
  console.log('  git-story              # Show commit history');
  console.log('  git-time start         # Track time');
  console.log('  git-sync-all           # Sync branches');
  console.log('');
  console.log('Documentation:');
  console.log('  https://github.com/yourusername/git-quick');
  console.log('');
} else {
  console.log('');
  console.log('Please install Python 3.8+ and run:');
  console.log('  npm install -g git-quick-cli');
  console.log('');
}
