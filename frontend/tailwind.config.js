/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'sonos-black': '#000000',
        'sonos-gray': '#1a1a1a',
        'sonos-accent': '#ff6b35',
      },
    },
  },
  plugins: [],
}
