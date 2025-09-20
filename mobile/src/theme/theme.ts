import { DefaultTheme, MD3DarkTheme } from 'react-native-paper';

declare global {
  namespace ReactNativePaper {
    interface ThemeColors {
      accent: string;
    }
  }
}

export const lightTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#65c0ba',
    accent: '#ffcc00',
    background: '#ffffff',
    surface: '#f8f9fa',
    text: '#212529',
    placeholder: '#6c757d',
  },
};

export const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: '#65c0ba',
    accent: '#ffcc00',
    background: '#121212',
    surface: '#1e1e1e',
    text: '#ffffff',
    placeholder: '#6c757d',
  },
};
