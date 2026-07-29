const examples = {
  get: 'ntn pages get <page-id>',
  create: 'ntn pages create --parent page:<id> --content "# Title\n\nBody"',
  edit: 'ntn pages edit <page-id> --content "## Updated\n\nNew body"',
  trash: 'ntn pages trash <page-id> --yes'
};
console.log(JSON.stringify(examples, null, 2));
