import { exec } from 'child_process';

exec('npm test', { cwd: '/app/crypto-trading-education-platform/backend' }, (err, stdout, stderr) => {
  if (err) {
    console.error(`exec error: ${err}`);
    console.error(stderr);
    return;
  }
  console.log(stdout);
});
