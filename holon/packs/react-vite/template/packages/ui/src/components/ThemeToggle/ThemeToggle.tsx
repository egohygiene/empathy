import { Icon } from "@egohygiene/icons";
import { themeNames, useTheme } from "@egohygiene/themes";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <label className="eh-theme-toggle">
      <span className="eh-theme-toggle__label">Theme</span>
      <select
        aria-label="Theme"
        className="eh-select"
        onChange={(event) => setTheme(event.target.value as typeof theme)}
        value={theme}
      >
        {themeNames.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <Icon
        decorative
        name={theme === "dark" ? "moon" : theme === "high-contrast" ? "contrast" : "sun"}
      />
    </label>
  );
}
