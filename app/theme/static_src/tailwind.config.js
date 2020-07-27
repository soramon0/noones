module.exports = {
  theme: {
    extend: {
      inset: {
        '1/2': '50%',
      },
      spacing: {
        '68': '17rem',
        '72': '18rem',
        '76': '19rem',
        '80': '20rem',
        '95': '95%',
        '500': '500px',
      },
    },
    customForms: (theme) => ({
      default: {
        'input, select': {
          borderRadius: theme('borderRadius.lg'),
          focusBorderColor: 'transparent',
          lineHeight: theme('lineHeight.snug'),
          borderColor: theme('colors.gray.400'),
          focusShadow: 'none',
          color: theme('colors.gray.900'),
          width: theme('width.full'),
        },
        select: {
          icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#000"><path d="M15.3 9.3a1 1 0 0 1 1.4 1.4l-4 4a1 1 0 0 1-1.4 0l-4-4a1 1 0 0 1 1.4-1.4l3.3 3.29 3.3-3.3z"/></svg>`,
        },
        textarea: {
          width: theme('spacing.95'),
          borderColor: theme('colors.gray.400'),
        },
        'radio, checkbox': {
          color: theme('colors.gray.900'),
          display: 'inline-block',
          borderColor: theme('colors.gray.500'),
        },
      },
    }),
  },
  variants: {},
  plugins: [require('@tailwindcss/custom-forms')],
};
