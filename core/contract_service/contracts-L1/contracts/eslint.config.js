const { FlatCompat } = require('@eslint/eslintrc');
const path = require('node:path');
const js = require('@eslint/js');

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

const legacyConfig = require(path.join(__dirname, '.eslintrc.json'));

module.exports = compat.config(legacyConfig);
