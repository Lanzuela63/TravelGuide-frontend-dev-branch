// src/screens/AppSettingsScreen.tsx
import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { getBaseUrl, setBaseUrl } from "../config/api";

const AppSettingsScreen: React.FC = () => {
  const [baseUrl, setUrl] = useState("");

  useEffect(() => {
    const loadUrl = async () => {
      const url = await getBaseUrl();
      setUrl(url);
    };
    loadUrl();
  }, []);

  const handleSave = async () => {
    await setBaseUrl(baseUrl);
    Alert.alert("Base URL saved!", "Restart the app to apply.");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>API Base URL</Text>
      <TextInput
        style={styles.input}
        value={baseUrl}
        onChangeText={setUrl}
        placeholder="http://192.168.x.x:8000"
      />
      <Button title="Save" onPress={handleSave} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  label: { fontSize: 16, marginBottom: 10 },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    marginBottom: 20,
    borderRadius: 5,
  },
});

export default AppSettingsScreen;
