const purgecss = require('@fullhuman/postcss-purgecss')
const cssnano = require('cssnano')

module.exports = {
  syntax: 'postcss-scss',
  plugins: [
    require('tailwindcss'),
    require('autoprefixer'),
    cssnano({preset: 'default'}),
    purgecss({
      content: ['../templates/**/*.html'],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
    })
  ]
}