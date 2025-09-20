//mobile/src/screens/dashboards/TouristDashboard.tsx
import React, { useContext, useEffect, useState, FC } from 'react';
import {
  StyleSheet,
  FlatList,
  TouchableOpacity,
  View,
  Alert,
} from 'react-native';
import {
  ActivityIndicator,
  Card,
  Title,
  Paragraph,
  Button,
  useTheme,
  Text,
} from 'react-native-paper';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';
import { AuthContext } from '../../context/AuthContext';
import { ThemeContext } from '../../context/ThemeContext';
import { API_BASE_URL, AR_BASE_URL } from '../../config/api';
import  Icon  from 'react-native-vector-icons/MaterialCommunityIcons';

// Define interfaces for data structures
interface Location {
  name: string;
  region: string;
  province: string;
}

interface TouristSpot {
  id: number;
  name: string;
  location?: Location;
  description: string;
  image?: string;
  average_rating?: number;
}

const TouristDashboard: FC = () => {
  const navigation = useNavigation<any>();
  const { userToken: accessToken } = useContext(AuthContext);
  const { toggleTheme, isDark } = useContext(ThemeContext);
  const theme = useTheme();

  const [spots, setSpots] = useState<TouristSpot[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTouristSpots();
  }, []);

  const fetchTouristSpots = async () => {
    try {
      const response = await axios.get<TouristSpot[]>(
        `${API_BASE_URL}/api/tourism/spots/`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      setSpots(response.data);
    } catch (error: any) {
      console.error('Failed to load tourism spots:', error.message);
      setError('Failed to load tourist spots. Please try again later.');
      Alert.alert(
        'Error',
        'Failed to load tourist spots. Please try again later.'
      );
    } finally {
      setLoading(false);
    }
  };

  const renderSpot = ({ item }: { item: TouristSpot }) => (
    <Card style={styles.card}>
      <Card.Cover source={{ uri: item.image || 'https://via.placeholder.com/300x200' }} />
      <Card.Content>
        <Title>{item.name}</Title>
        <View style={styles.ratingContainer}>
          <Icon name="star" color={theme.colors.accent} size={20} />
          <Text style={styles.ratingText}>
            {item.average_rating?.toFixed(1) || 'N/A'}
          </Text>
        </View>
        <Paragraph numberOfLines={2}>{item.description}</Paragraph>
        <Text style={styles.distanceText}>2.5 km away</Text>
      </Card.Content>
      <Card.Actions>
        <Button
          mode="contained"
          onPress={() =>
            navigation.navigate('AR', {
              screen: 'ARView',
              params: {
                spot_id: item.id,
                arUrl: `${AR_BASE_URL}/webar/${item.id}/`,
              },
            })
          }
        >
          Explore in AR
        </Button>
      </Card.Actions>
    </Card>
  );

  if (loading) {
    return (
      <View style={[styles.centered, { backgroundColor: theme.colors.background }]}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text>Loading tourist spots...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={[styles.centered, { backgroundColor: theme.colors.background }]}>
        <Text style={{ color: theme.colors.error }}>{error}</Text>
      </View>
    );
  }

  return (
    <FlatList
      data={spots}
      keyExtractor={(item) => item.id.toString()}
      renderItem={renderSpot}
      contentContainerStyle={[
        styles.container,
        { backgroundColor: theme.colors.background },
      ]}
      ListHeaderComponent={
        <>
          <View style={styles.header}>
            <Title style={styles.heading}>🏞 Featured Tourist Spots</Title>
            <Button onPress={toggleTheme}>
              {isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            </Button>
          </View>
          <Button
            mode="contained"
            style={styles.locationArButton}
            onPress={() =>
              navigation.navigate('AR', {
                screen: 'LocationARView',
                params: { arUrl: `${AR_BASE_URL}/location/` },
              })
            }
          >
            Open Location AR
          </Button>
        </>
      }
    />
  );
};

export default TouristDashboard;

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    paddingTop: 20,
    paddingHorizontal: 10,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  heading: {
    fontSize: 22,
    fontWeight: 'bold',
  },
  card: {
    marginBottom: 15,
    elevation: 3,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 5,
  },
  ratingText: {
    marginLeft: 5,
    fontSize: 16,
  },
  distanceText: {
    marginTop: 5,
    fontStyle: 'italic',
  },
  locationArButton: {
    marginHorizontal: 20,
    marginBottom: 20,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
});
