import React, { useContext, FC } from 'react';
import { View, StyleSheet, Image } from 'react-native';
import { AuthContext } from '../../context/AuthContext';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { TouristStackParamList } from '../../navigation/TouristTabNavigator';

type ProfileScreenNavigationProp = StackNavigationProp<TouristStackParamList, 'ProfileMain'>;

const ProfileScreen: FC = () => {
  console.log('Rendering ProfileScreen');
  const { user, logout } = useContext(AuthContext);
  const navigation = useNavigation<ProfileScreenNavigationProp>();

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content style={styles.cardContent}>
          <Avatar.Image
            size={100}
            source={{ uri: user?.profile_image || 'https://via.placeholder.com/100' }}
            style={styles.avatar}
          />
          <Title style={styles.username}>{user?.username}</Title>
          <Paragraph style={styles.email}>{user?.email}</Paragraph>
          <Paragraph style={styles.role}>{user?.role}</Paragraph>

          <Button
            mode="contained"
            onPress={() => navigation.navigate('EditProfile')}
            style={styles.editButton}
          >
            Edit Profile
          </Button>

          <Button
            mode="outlined"
            onPress={logout}
            style={styles.logoutButton}
          >
            Logout
          </Button>
        </Card.Content>
      </Card>
    </View>
  );
};

export default ProfileScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f0f4f8',
  },
  card: {
    borderRadius: 15,
    elevation: 5,
  },
  cardContent: {
    alignItems: 'center',
    padding: 20,
  },
  avatar: {
    marginBottom: 20,
  },
  username: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  email: {
    fontSize: 16,
    color: '#666',
    marginBottom: 5,
  },
  role: {
    fontSize: 16,
    color: '#666',
    marginBottom: 20,
  },
  editButton: {
    marginTop: 10,
  },
  logoutButton: {
    marginTop: 10,
    borderColor: '#007AFF',
  },
});