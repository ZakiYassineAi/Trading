process.env.NODE_ENV = 'test';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import { createRequire } from 'module';

const filename = fileURLToPath(import.meta.url);
const backendDir = path.dirname(filename);

// Load Jest securely in an ESM environment
const require = createRequire(import.meta.url);
const { runCLI } = require('jest');

// Optional pattern to run a single test: node run-tests.mjs path/to/file.test.ts
const testPattern = process.argv[2] ? path.resolve(process.argv[2]) : undefined;

// Embedded Jest configuration
const jestConfig = {
  rootDir: backendDir,
  testEnvironment: 'node',
  moduleNameMapper: {
    '^redis$': path.resolve(backendDir, 'tests/mocks/redis.js'),
  },
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

// Run Jest
const cliConfig = {
  config: JSON.stringify(jestConfig),
  runInBand: true
};

runCLI(cliConfig, [backendDir]).then(({ results }) => {
  process.exit(results.success ? 0 : 1);
}).catch((err) => {
  console.error(err);
  process.exit(1);
});
