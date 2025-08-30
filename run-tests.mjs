import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import { createRequire } from 'module';

const filename = fileURLToPath(import.meta.url);
const dirname = path.dirname(filename);

// The backend directory
const backendDir = path.resolve(dirname, 'crypto-trading-education-platform', 'backend');

// Load Jest securely in an ESM environment
const require = createRequire(import.meta.url);
const { runCLI } = require('jest');

// Optional pattern to run a single test: node run-tests.mjs path/to/file.test.ts
const testPattern = process.argv[2] ? path.resolve(process.argv[2]) : undefined;

// Embedded Jest configuration (ESM/TS via babel-jest)
const jestConfig = {
  rootDir: backendDir,
  testEnvironment: 'node',
  transform: {
    '^.+\\.(mjs|cjs|js|ts)$': [
      require.resolve('babel-jest'),
      {
        presets: [
          ['@babel/preset-env', { targets: { node: 'current' } }],
          '@babel/preset-typescript'
        ]
      }
    ]
  },
  moduleFileExtensions: ['js', 'mjs', 'cjs', 'ts', 'json'],
  testMatch: testPattern ? [pathToFileURL(testPattern).pathname] : ['**/__tests__/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[jt]s?(x)'],
};

// Run Jest without relying on cwd
const cliConfig = {
  // Passing the config as a JSON string is safest with runCLI
  config: JSON.stringify(jestConfig),
  runInBand: true
};

runCLI(cliConfig, [backendDir]).then(({ results }) => {
  process.exit(results.success ? 0 : 1);
}).catch((err) => {
  console.error(err);
  process.exit(1);
});
