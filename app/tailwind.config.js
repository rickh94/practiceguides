const defaultTheme = require("tailwindcss/defaultTheme");
const { addDynamicIconSelectors } = require("@iconify/tailwind");

module.exports = {
  content: ["**/*.html"],
  theme: {
    screens: {
      xs: "475px",
      ...defaultTheme.screens,
    },
    extend: {},
  },
  plugins: [addDynamicIconSelectors()],
};
