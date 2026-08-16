import aspectRatio from "@tailwindcss/aspect-ratio";
import forms from "@tailwindcss/forms";
import typography from "@tailwindcss/typography";
import type { Config } from "tailwindcss";
import plugin from "tailwindcss/plugin";

const color = (name: string) => `rgb(var(--color-${name}) / <alpha-value>)`;

const preset = {
  darkMode: ["class", '[data-theme="dark"]'],
  theme: {
    screens: {
      xs: "30rem",
      sm: "40rem",
      md: "48rem",
      lg: "64rem",
      xl: "80rem",
      "2xl": "96rem",
    },
    container: {
      center: true,
      padding: {
        DEFAULT: "1rem",
        sm: "1.5rem",
        lg: "2rem",
        xl: "2.5rem",
      },
      screens: {
        "2xl": "90rem",
      },
    },
    extend: {
      colors: {
        canvas: color("canvas"),
        surface: color("surface"),
        elevated: color("elevated"),
        ink: color("ink"),
        muted: color("muted"),
        border: color("border"),
        primary: {
          DEFAULT: color("primary-500"),
          50: color("primary-50"),
          100: color("primary-100"),
          200: color("primary-200"),
          300: color("primary-300"),
          400: color("primary-400"),
          500: color("primary-500"),
          600: color("primary-600"),
          700: color("primary-700"),
          800: color("primary-800"),
          900: color("primary-900"),
          950: color("primary-950"),
        },
        success: color("success"),
        warning: color("warning"),
        danger: color("danger"),
        info: color("info"),
      },
      fontFamily: {
        sans: ["Inter Variable", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        display: [
          "Atkinson Hyperlegible",
          "Inter Variable",
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
        ],
        mono: ["JetBrains Mono Variable", "JetBrains Mono", "ui-monospace", "monospace"],
      },
      fontSize: {
        "display-2xl": [
          "clamp(3.5rem, 8vw, 8rem)",
          { lineHeight: "0.92", letterSpacing: "-0.055em" },
        ],
        "display-xl": [
          "clamp(2.75rem, 6vw, 6rem)",
          { lineHeight: "0.96", letterSpacing: "-0.045em" },
        ],
        "display-lg": [
          "clamp(2.25rem, 5vw, 4.5rem)",
          { lineHeight: "1", letterSpacing: "-0.04em" },
        ],
      },
      borderRadius: {
        xs: "var(--radius-xs, 0.25rem)",
        sm: "var(--radius-sm, 0.5rem)",
        md: "var(--radius-md, 0.75rem)",
        lg: "var(--radius-lg, 1rem)",
        xl: "var(--radius-xl, 1.5rem)",
        full: "9999px",
      },
      boxShadow: {
        soft: "0 10px 30px rgb(15 23 42 / 0.08)",
        lifted: "0 24px 60px rgb(15 23 42 / 0.16)",
        focus: "0 0 0 4px rgb(var(--color-primary-500) / 0.28)",
      },
      spacing: {
        18: "4.5rem",
        22: "5.5rem",
        30: "7.5rem",
        34: "8.5rem",
      },
      maxWidth: {
        prose: "72ch",
        reading: "82ch",
        screen: "90rem",
      },
      transitionTimingFunction: {
        productive: "cubic-bezier(0.2, 0, 0, 1)",
        expressive: "cubic-bezier(0.4, 0, 0.2, 1)",
      },
      keyframes: {
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "slide-up": {
          from: { opacity: "0", transform: "translateY(0.75rem)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          from: { backgroundPosition: "200% 0" },
          to: { backgroundPosition: "-200% 0" },
        },
      },
      animation: {
        "fade-in": "fade-in 180ms ease-out both",
        "slide-up": "slide-up 240ms cubic-bezier(0.2, 0, 0, 1) both",
        shimmer: "shimmer 2s linear infinite",
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "72ch",
            color: "rgb(var(--color-ink))",
            a: {
              color: "rgb(var(--color-primary-600))",
              textDecorationThickness: "0.08em",
              textUnderlineOffset: "0.18em",
            },
          },
        },
      },
    },
  },
  plugins: [
    forms({ strategy: "class" }),
    typography,
    aspectRatio,
    plugin(({ addBase, addUtilities }) => {
      addBase({
        ":focus-visible": {
          outline: "2px solid rgb(var(--color-primary-500))",
          outlineOffset: "3px",
        },
        "::selection": {
          backgroundColor: "rgb(var(--color-primary-200))",
          color: "rgb(var(--color-primary-950))",
        },
      });
      addUtilities({
        ".content-auto": { contentVisibility: "auto" },
        ".text-balance": { textWrap: "balance" },
        ".text-pretty": { textWrap: "pretty" },
      });
    }),
  ],
} satisfies Omit<Config, "content">;

export default preset;
