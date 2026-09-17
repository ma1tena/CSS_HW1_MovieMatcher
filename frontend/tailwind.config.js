/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0F0F12", // page background — warm near-black, not pure black
        surface: "#17171C", // card / panel background
        surfaceRaised: "#1D1D24", // slightly lighter surface for selected states
        hairline: "rgba(237, 234, 227, 0.10)", // subtle borders instead of shadows
        paper: "#EDEAE3", // primary text — warm off-white
        muted: "#8B8B94", // secondary text
        marquee: "#E3B23C", // single accent: cinema-marquee gold
        marqueeDim: "rgba(227, 178, 60, 0.15)",
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
