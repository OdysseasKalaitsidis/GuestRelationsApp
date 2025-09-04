/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}", // include all React source files
  ],
  theme: {
    extend: {
      colors: {
        'main': '#042d27',
        'secondary': '#a97c5e',
        'third': '#8e9a98',
      },
    },
  },
  plugins: [],
};
