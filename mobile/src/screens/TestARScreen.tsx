import React, { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";
import { API_BASE_URL } from "../config/api";

// Define the AR Scene data structure based on your Django serializer
interface ARScene {
  id: number;
  name: string;
  description: string;
  latitude: number;
  longitude: number;
}

export default function TestARScenes() {
  const [loading, setLoading] = useState<boolean>(true);
  const [scenes, setScenes] = useState<ARScene[]>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/scenes/nearby/?lat=13.6205&lon=123.1948`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data: ARScene[]) => {
        setScenes(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch AR scenes:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <ActivityIndicator style={{ marginTop: 50 }} size="large" color="#0000ff" />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Nearby AR Scenes</Text>
      <FlatList
        data={scenes}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.name}>{item.name}</Text>
            <Text style={styles.desc}>{item.description}</Text>
            <Text style={styles.coords}>
              📍 Lat: {item.latitude}, Lon: {item.longitude}
            </Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: "#fff" },
  header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
  card: { backgroundColor: "#f9f9f9", padding: 12, marginBottom: 8, borderRadius: 6 },
  name: { fontSize: 16, fontWeight: "bold" },
  desc: { fontSize: 14, color: "#555" },
  coords: { fontSize: 12, color: "#777" },
});
