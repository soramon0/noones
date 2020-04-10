const purgecss = require('@fullhuman/postcss-purgecss');

const prod = process.env.NODE_ENV == 'production';

module.exports = {
  syntax: 'postcss-scss',
  plugins: [
    require("postcss-import"),
    require('tailwindcss'),
    require('autoprefixer'),
    require('cssnano'),
    prod &&
    purgecss({
      content: ['../templates/**/*.html', './src/svelte/**/*.svelte'],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
      whitelistPatterns: [/simplebar/, /scrollbar/]
    })
  ]
};
