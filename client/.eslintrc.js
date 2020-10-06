module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: [
    'plugin:react/recommended',
    'standard'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    },
    ecmaVersion: 12,
    sourceType: 'module'
  },
  plugins: [
    'react',
    '@typescript-eslint'
  ],
  rules: {
    'no-use-before-define': 'off',
    '@typescript-eslint/no-use-before-define': ['error'],
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': ['error']
  },
  overrides: [{
    files: [
      'packages/**/__tests__/**/*.{js,ts,jsx,tsx}'
    ],
    env: {
      jest: true
    },
    plugins: [
      'jest'
    ],
    rules: {
      'jest/no-disabled-tests': ['warn'],
      'jest/no-focused-tests': ['error'],
      'jest/no-identical-title': ['error'],
      'jest/valid-expect': ['error']
    }
  }]
}
