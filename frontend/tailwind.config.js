/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        teal: { DEFAULT: '#00d4aa', dark: '#00a884' },
        brand: {
          purple: '#7c3aed',
          pink: '#f472b6',
          bg: '#0a0a12',
          card: '#0f0f1e',
          border: 'rgba(255,255,255,0.08)',
        },
      },
      fontFamily: {
        mono: ['"Space Mono"', 'monospace'],
        sans: ['"DM Sans"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
