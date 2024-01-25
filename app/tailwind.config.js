const { addDynamicIconSelectors } = require("@iconify/tailwind");

module.exports = {
  content: ["**/*.html"],
  theme: {
    extend: {
      colors: {
        whitesmoke: "#f1edee",
        azure: {
          100: "#C5DFFF",
          200: "#83BBFF",
          300: "#4C9CFF",
          400: "#3185FC",
          500: "#0066FF",
          600: "#0056F1",
          700: "#0049CD",
          800: "#003EAE",
          900: "#003594",
          950: "#002D7E",
        },
        byzantium: {
          50: "#FF6EE3",
          100: "#FF18D2",
          200: "#FF00BB",
          300: "#D00095",
          400: "#A50076",
          500: "#770058",
          600: "#610045",
          700: "#480033",
          800: "#350026",
          900: "#27001C",
          950: "#1D0015",
        },
      },
    },
  },
  plugins: [addDynamicIconSelectors()],
};
