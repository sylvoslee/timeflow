const colors = require('tailwindcss/colors')

module.exports = {
  content: ["site/*.{html,js}"],
  theme: {
    colors: {
      'primary-100': '#A29AC7',
      'primary-300': '#52448A',
      'primary-400': '#362870',
      'primary-500': '#1F1254',
      'primary-600': '#100639',
      'primary-700': '#080220',
      'secondary-200': '#E3DEFC',
      'secondary-300': '#E3DEFC',
      'secondary-400': '#BAAEF2',
      'secondary-500': '#9484E3',
      'secondary-600': '#7360D0',
      'secondary-700': '#5541B7',
      content: colors.white,
      black: colors.black,
      gray: colors.gray,
      white: colors.white,
    },
    extend: {
      // ...
    },
  },
  plugins: [],
}
