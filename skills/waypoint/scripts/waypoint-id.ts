import { createHash } from 'node:crypto';

const paths = process.argv.slice(2);

if (paths.length === 0) {
  console.error('Usage: waypoint-id <path> [path...]');
  console.error('Generate 8-char waypoint IDs from file paths relative to git root.');
  process.exit(1);
}

for (const p of paths) {
  const id = createHash('sha256').update(p).digest('hex').slice(0, 8);
  console.log(`${id}  ${p}`);
}
