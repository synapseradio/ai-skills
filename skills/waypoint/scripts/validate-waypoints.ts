import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { $ } from 'bun';

const WAYPOINTS_DIR = '.ai/waypoints';
const WAYPOINT_PATTERN = /Waypoint\s+([0-9a-f]{8})/g;

interface ManifestEntry {
  id: string;
  file: string;
  pipeline: string;
}

// Parse the manifest table for waypoint IDs and file paths.
// Expects rows like: | `a1b2c3d4` | path/to/file | role |
function parseManifest(content: string, pipeline: string): ManifestEntry[] {
  const entries: ManifestEntry[] = [];
  for (const line of content.split('\n')) {
    const match = line.match(/\|\s*`([0-9a-f]{8})`\s*\|\s*(\S+)\s*\|/);
    if (match) {
      entries.push({ id: match[1], file: match[2], pipeline });
    }
  }
  return entries;
}

async function findManifests(): Promise<string[]> {
  try {
    const files = await readdir(WAYPOINTS_DIR);
    return files.filter(f => f.endsWith('.md')).map(f => join(WAYPOINTS_DIR, f));
  } catch {
    return [];
  }
}

async function findWaypointBlocks(): Promise<Map<string, string[]>> {
  // Map of waypoint ID → list of files containing it
  const blocks = new Map<string, string[]>();
  try {
    const result = await $`grep -r "Waypoint [0-9a-f]\\{8\\}" --include="*" -l .`.text();
    const files = result.trim().split('\n').filter(Boolean);

    for (const file of files) {
      // Skip manifest files
      if (file.startsWith(`./${WAYPOINTS_DIR}/`) || file.startsWith(`${WAYPOINTS_DIR}/`)) continue;

      const content = await readFile(file, 'utf-8');
      for (const match of content.matchAll(WAYPOINT_PATTERN)) {
        const id = match[1];
        const existing = blocks.get(id) ?? [];
        existing.push(file.replace(/^\.\//, ''));
        blocks.set(id, existing);
      }
    }
  } catch {
    // grep returns exit code 1 when no matches — not an error
  }
  return blocks;
}

async function main() {
  const manifestPaths = await findManifests();

  if (manifestPaths.length === 0) {
    console.log('No waypoint manifests found. Nothing to validate.');
    process.exit(0);
  }

  const allManifestEntries: ManifestEntry[] = [];
  const manifestIds = new Set<string>();
  let hasDrift = false;

  // Parse all manifests
  for (const path of manifestPaths) {
    const content = await readFile(path, 'utf-8');
    const pipeline = path.replace(`${WAYPOINTS_DIR}/`, '').replace('.md', '');
    const entries = parseManifest(content, pipeline);
    allManifestEntries.push(...entries);
    for (const e of entries) manifestIds.add(e.id);
  }

  // Find all waypoint comment blocks in the codebase
  const blocks = await findWaypointBlocks();

  // Group entries by pipeline for reporting
  const byPipeline = new Map<string, ManifestEntry[]>();
  for (const entry of allManifestEntries) {
    const list = byPipeline.get(entry.pipeline) ?? [];
    list.push(entry);
    byPipeline.set(entry.pipeline, list);
  }

  for (const [pipeline, entries] of byPipeline) {
    const stale: string[] = [];
    let verified = 0;

    for (const entry of entries) {
      const files = blocks.get(entry.id);
      if (!files || !files.some(f => f === entry.file || f === `./${entry.file}`)) {
        stale.push(entry.id);
      } else {
        verified++;
      }
    }

    console.log(`\n${pipeline}:`);
    console.log(`  verified: ${verified}/${entries.length}`);

    if (stale.length > 0) {
      hasDrift = true;
      console.log(`  stale IDs (in manifest but not found in expected file):`);
      for (const id of stale) {
        const entry = entries.find(e => e.id === id)!;
        console.log(`    ${id}  ${entry.file}`);
      }
    }
  }

  // Find orphaned waypoint blocks — present in files but not in any manifest
  const orphaned: { id: string; files: string[] }[] = [];
  for (const [id, files] of blocks) {
    if (!manifestIds.has(id)) {
      orphaned.push({ id, files });
    }
  }

  if (orphaned.length > 0) {
    hasDrift = true;
    console.log('\norphaned (in files but not in any manifest):');
    for (const { id, files } of orphaned) {
      console.log(`  ${id}  ${files.join(', ')}`);
    }
  }

  if (hasDrift) {
    console.log('\ndrift detected.');
    process.exit(1);
  } else {
    console.log('\nall waypoints valid.');
    process.exit(0);
  }
}

main();
