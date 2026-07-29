const catalog = {
  install: ['curl -fsSL https://ntn.dev | bash', 'ntn --version'],
  auth: {
    oauth: ['ntn login', 'ntn login --no-browser', 'ntn login poll', 'ntn doctor', 'ntn logout'],
    env: ['NOTION_API_TOKEN', 'NOTION_KEYRING', 'NOTION_WORKSPACE_ID', 'NOTION_WORKERS_CONFIG_FILE', 'NOTION_API_VERSION']
  },
  api: ['ntn api <path>', 'ntn api ls'],
  datasources: ['ntn datasources resolve <database-id>', 'ntn datasources query <data-source-id>'],
  pages: ['ntn pages get <page-id>', 'ntn pages create --parent <ref>', 'ntn pages edit <page-id>', 'ntn pages trash <page-id>'],
  files: ['ntn files create', 'ntn files get <upload-id>', 'ntn files list'],
  workers: ['ntn workers deploy', 'ntn workers exec <key>', 'ntn workers sync status', 'ntn workers env list', 'ntn workers runs list']
};
if (process.argv.includes('--json')) {
  console.log(JSON.stringify(catalog, null, 2));
} else {
  for (const [group, items] of Object.entries(catalog)) {
    console.log(`[${group}]`);
    if (Array.isArray(items)) {
      for (const item of items) console.log(`- ${item}`);
      continue;
    }
    for (const [subgroup, values] of Object.entries(items)) {
      console.log(`  ${subgroup}:`);
      for (const value of values) console.log(`  - ${value}`);
    }
  }
}
