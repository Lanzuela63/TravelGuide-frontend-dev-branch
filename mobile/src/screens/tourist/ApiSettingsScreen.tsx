// src/screens/SettingsScreen.tsx
import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { getBaseUrl, setBaseUrl } from "../../config/api";

const SettingsScreen = () => {
  const [baseUrl, setBaseUrlState] = useState("");

  useEffect(() => {
    const loadBaseUrl = async () => {
      const url = await getBaseUrl();
      setBaseUrlState(url);
    };
    loadBaseUrl();
  }, []);

  const handleSave = async () => {
    await setBaseUrl(baseUrl);
    Alert.alert("Success", `Base URL updated to: ${baseUrl}`);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>API Settings</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter API Base URL"
        value={baseUrl}
        onChangeText={setBaseUrlState}
        autoCapitalize="none"
      />
      <Button title="Save" onPress={handleSave} />
    </View>
  );
};

export default SettingsScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 20, marginBottom: 20 },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    marginBottom: 15,
    borderRadius: 5,
  },
});
