import React, { createContext, useState, useMemo } from 'react';
import { Provider as PaperProvider } from 'react-native-paper';
import { lightTheme, darkTheme } from '../theme/theme';

export const ThemeContext = createContext({
  isDark: false,
  toggleTheme: () => {},
});

export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(false);

  const toggleTheme = () => {
    setIsDark(!isDark);
  };

  const theme = isDark ? darkTheme : lightTheme;

  const themeContextValue = useMemo(
    () => ({
      isDark,
      toggleTheme,
    }),
    [isDark]
  );

  return (
    <ThemeContext.Provider value={themeContextValue}>
      <PaperProvider theme={theme}>{children}</PaperProvider>
    </ThemeContext.Provider>
  );
};
