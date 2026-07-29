const payload = {
  files: [
    'ntn files create < ./photo.png',
    'ntn files get <upload-id>',
    'ntn files list'
  ],
  workers: [
    'ntn workers deploy',
    'ntn workers exec <key>',
    'ntn workers sync status',
    'ntn workers env list',
    'ntn workers runs list',
    'ntn workers webhooks list'
  ]
};
console.log(JSON.stringify(payload, null, 2));
