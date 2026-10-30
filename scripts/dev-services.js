#!/usr/bin/env node

/**
 * Service Runner for Legal Intelligence System.
 * Starts speech-service and ml-service concurrently with prefixed colored output.
 * Gracefully terminates all services on Ctrl+C.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const ROOT_DIR = path.resolve(__dirname, '..');

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
};

function findPython(serviceDir, candidateDirs = ['venv', '.venv']) {
  for (const venv of candidateDirs) {
    const py = path.join(serviceDir, venv, 'bin', 'python');
    if (fs.existsSync(py)) {
      return py;
    }
  }
  return 'python3';
}

const services = [
  {
    name: 'ml-service',
    color: colors.cyan,
    port: 8000,
    healthUrl: 'http://localhost:8000/health',
    cwd: path.join(ROOT_DIR, 'ml-service'),
    getCommand: () => {
      const mlDir = path.join(ROOT_DIR, 'ml-service');
      const py = findPython(mlDir, ['venv', '.venv']);
      return {
        cmd: py,
        args: [
          '-m',
          'uvicorn',
          'app.main:app',
          '--app-dir',
          mlDir,
          '--host',
          '127.0.0.1',
          '--port',
          '8000',
          '--reload',
          '--reload-dir',
          path.join(mlDir, 'app'),
          '--reload-dir',
          path.join(ROOT_DIR, 'knowledge_base'),
        ],
      };
    },
  },
  {
    name: 'speech-service',
    color: colors.magenta,
    port: 8001,
    healthUrl: 'http://localhost:8001/health',
    cwd: path.join(ROOT_DIR, 'speech-service'),
    getCommand: () => {
      const speechDir = path.join(ROOT_DIR, 'speech-service');
      const py = findPython(speechDir, ['.venv', 'venv']);
      return {
        cmd: py,
        args: [
          '-m',
          'uvicorn',
          'app.main:app',
          '--app-dir',
          speechDir,
          '--host',
          '127.0.0.1',
          '--port',
          '8001',
          '--reload',
          '--reload-dir',
          path.join(speechDir, 'app'),
        ],
      };
    },
  },
];

// Optional services if user passes --all
const optionalServices = [
  {
    name: 'api-gateway',
    color: colors.green,
    port: 5000,
    healthUrl: 'http://localhost:5000/api/health',
    cwd: path.join(ROOT_DIR, 'backend'),
    getCommand: () => ({
      cmd: 'npm',
      args: ['run', 'dev'],
    }),
  },
  {
    name: 'frontend',
    color: colors.blue,
    port: 3000,
    healthUrl: 'http://localhost:3000',
    cwd: path.join(ROOT_DIR, 'frontend'),
    getCommand: () => ({
      cmd: 'npm',
      args: ['run', 'dev'],
    }),
  },
];

const args = process.argv.slice(2);
let activeServices = [...services];

if (args.includes('--all')) {
  activeServices = [...services, ...optionalServices];
} else if (args.includes('--ml-only') || args.includes('--ml')) {
  activeServices = services.filter((s) => s.name === 'ml-service');
} else if (args.includes('--speech-only') || args.includes('--speech')) {
  activeServices = services.filter((s) => s.name === 'speech-service');
}

console.log(`${colors.bold}====================================================${colors.reset}`);
console.log(`${colors.bold}   Starting Legal Intelligence System Services      ${colors.reset}`);
console.log(`${colors.bold}====================================================${colors.reset}`);
activeServices.forEach((s) => {
  console.log(` • ${s.color}${s.name.padEnd(16)}${colors.reset} -> ${colors.dim}${s.healthUrl}${colors.reset}`);
});
console.log(`${colors.dim}Press Ctrl+C to stop all services.\n${colors.reset}`);

const runningChildren = [];
let isShuttingDown = false;

function prefixStream(stream, prefix, color) {
  let buffer = '';
  stream.on('data', (data) => {
    buffer += data.toString();
    const lines = buffer.split('\n');
    buffer = lines.pop(); // keep unfinished line in buffer
    for (const line of lines) {
      if (line.trim().length > 0) {
        console.log(`${color}[${prefix}]${colors.reset} ${line}`);
      }
    }
  });
  stream.on('end', () => {
    if (buffer.trim().length > 0) {
      console.log(`${color}[${prefix}]${colors.reset} ${buffer}`);
    }
  });
}

function startService(service) {
  const { cmd, args } = service.getCommand();
  const child = spawn(cmd, args, {
    cwd: service.cwd,
    env: { ...process.env, PYTHONUNBUFFERED: '1' },
    stdio: ['inherit', 'pipe', 'pipe'],
  });

  runningChildren.push({ child, name: service.name });

  prefixStream(child.stdout, service.name, service.color);
  prefixStream(child.stderr, service.name, service.color);

  child.on('error', (err) => {
    console.error(`${service.color}[${service.name}] ERROR:${colors.reset} ${err.message}`);
  });

  child.on('exit', (code, signal) => {
    if (!isShuttingDown) {
      console.log(
        `${service.color}[${service.name}]${colors.reset} exited with code ${code ?? signal}`
      );
    }
  });
}

activeServices.forEach(startService);

function shutdown(signal) {
  if (isShuttingDown) return;
  isShuttingDown = true;
  console.log(`\n${colors.yellow}Stopping all services (${signal})...${colors.reset}`);

  runningChildren.forEach(({ child, name }) => {
    try {
      child.kill(signal || 'SIGINT');
    } catch (e) {
      // ignore
    }
  });

  // Force kill if not dead after 3 seconds
  setTimeout(() => {
    runningChildren.forEach(({ child }) => {
      try {
        child.kill('SIGKILL');
      } catch (e) {}
    });
    process.exit(0);
  }, 3000);
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
