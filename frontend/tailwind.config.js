/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'risk-approve': '#16a34a',
        'risk-refer': '#d97706',
        'risk-reject': '#dc2626',
      }
    },
  },
  plugins: [],
}
