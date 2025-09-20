import React, { useState, useContext, FC } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { TextInput, Button, Card, Title, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { AuthContext } from '../../context/AuthContext';

const EditProfileScreen: FC = () => {
  console.log('Rendering EditProfileScreen');
  const navigation = useNavigation<any>();
  const { user, updateUser } = useContext(AuthContext);

  const [fullName, setFullName] = useState<string>(user?.full_name || '');
  const [bio, setBio] = useState<string>(user?.bio || '');
  const [location, setLocation] = useState<string>(user?.location || '');

  const handleUpdate = () => {
    if (!fullName || !bio || !location) {
      Alert.alert('Validation Error', 'Please fill in all fields.');
      return;
    }
    updateUser({ fullName, bio, location });
    navigation.goBack();
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.header}>
            <IconButton icon="arrow-left" onPress={() => navigation.goBack()} />
            <Title style={styles.title}>Edit Profile</Title>
          </View>

          <TextInput
            label="Full Name"
            value={fullName}
            onChangeText={setFullName}
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Bio"
            value={bio}
            onChangeText={setBio}
            mode="outlined"
            style={styles.input}
            multiline
            numberOfLines={4}
          />

          <TextInput
            label="Location"
            value={location}
            onChangeText={setLocation}
            mode="outlined"
            style={styles.input}
          />

          <Button
            mode="contained"
            onPress={handleUpdate}
            style={styles.updateButton}
          >
            Update Profile
          </Button>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

export default EditProfileScreen;

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f0f4f8',
  },
  card: {
    padding: 20,
    borderRadius: 15,
    elevation: 5,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  input: {
    marginBottom: 15,
  },
  updateButton: {
    marginTop: 10,
  },
});
