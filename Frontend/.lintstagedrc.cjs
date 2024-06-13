module.exports = {
  'src/**/*.{js,jsx,ts,tsx,json,css,scss,md}': [
    'prettier --write',
    'eslint --fix',
  ],
  'src/**/*.{ts,tsx}': () => 'yarn typecheck',
};
