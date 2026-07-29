const fs = require('fs');

const raw = fs.readFileSync(0, 'utf8').trim();

if (!raw) {
  console.log('# Notion JSON\n\n_No input provided._');
  process.exit(0);
}

let data;
try {
  data = JSON.parse(raw);
} catch (err) {
  console.error('Input was not valid JSON');
  process.exit(1);
}

if (Array.isArray(data)) {
  console.log('# Notion JSON Summary\n');
  data.forEach((item, idx) => {
    console.log(`## Item ${idx + 1}`);
    console.log('```json');
    console.log(JSON.stringify(item, null, 2));
    console.log('```\n');
  });
  process.exit(0);
}

console.log('# Notion JSON Summary\n');
console.log('```json');
console.log(JSON.stringify(data, null, 2));
console.log('```');
