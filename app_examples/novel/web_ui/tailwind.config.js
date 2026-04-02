/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          start: '#667eea',
          end: '#764ba2'
        },
        dark: {
          bg: '#1a1a2e',
          surface: '#2a2a3e'
        }
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient-dark': 'linear-gradient(180deg, #1a1a2e 0%, #2a2a3e 100%)'
      }
    }
  },
  plugins: []
}