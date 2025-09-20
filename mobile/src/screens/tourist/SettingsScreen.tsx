import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { SettingsStackParamList } from '../../navigation/TouristTabNavigator'; // Assuming TouristTabNavigator defines the stack

type SettingsScreenNavigationProp = StackNavigationProp<SettingsStackParamList, 'SettingsMain'>; // Define a type for this screen in the stack

const SettingsScreen = () => {
  const navigation = useNavigation<SettingsScreenNavigationProp>();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Settings</Text>

      <TouchableOpacity
        style={styles.settingItem}
        onPress={() => navigation.navigate('Profile', { screen: 'EditProfile' })} // Navigate to EditProfile within ProfileStack
      >
        <Text style={styles.settingItemText}>Edit Profile</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.settingItem}
        onPress={() => navigation.navigate('ApiSettings')} // Navigate to the new ApiSettingsScreen
      >
        <Text style={styles.settingItemText}>API Settings</Text>
      </TouchableOpacity>

      {/* Add more settings options here */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f8f8f8',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
    textAlign: 'center',
    color: '#333',
  },
  settingItem: {
    backgroundColor: '#fff',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 10,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  settingItemText: {
    fontSize: 18,
    color: '#555',
  },
});

export default SettingsScreen;
