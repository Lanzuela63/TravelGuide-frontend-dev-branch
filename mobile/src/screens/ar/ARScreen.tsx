import React from "react";
import { StyleSheet } from "react-native";
import { WebView } from "react-native-webview";
import { AR_BASE_URL } from "config/api"; // 👈 import from your api.ts

const ARScreen: React.FC = () => {
  return (
    <WebView
      source={{ uri: AR_BASE_URL }}
      style={styles.webview}
      javaScriptEnabled
      domStorageEnabled
      originWhitelist={["*"]}
      allowsInlineMediaPlayback
      mediaPlaybackRequiresUserAction={false}
    />
  );
};

const styles = StyleSheet.create({
  webview: { flex: 1 },
});

export default ARScreen;
