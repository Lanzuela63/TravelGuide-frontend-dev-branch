// src/navigation/AppNavigator.tsx
import React, { useContext, ComponentType } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { ActivityIndicator, View } from "react-native";

// Auth context
import { AuthContext, AuthContextData } from "../context/AuthContext";

// Navigators
import TouristTabNavigator from "./TouristTabNavigator";

// Dashboards
import TouristDashboard from "../screens/dashboards/TouristDashboard";
import TourismDashboard from "../screens/dashboards/TourismDashboard";
import BusinessDashboard from "../screens/dashboards/BusinessDashboard";
import EventDashboard from "../screens/dashboards/EventDashboard";
import AdminDashboard from "../screens/dashboards/AdminDashboard";

// Auth & General Screens
import HomeScreen from "../screens/HomeScreen";
import LoginScreen from "../screens/LoginScreen";
import RegisterScreen from "../screens/RegisterScreen";
import WelcomeScreen from "../screens/WelcomeScreen";
import TestARScreen from "../screens/TestARScreen";

// ---------------- PARAM LISTS ----------------
export type RootStackParamList = {
  Welcome: undefined;
  Home: undefined;
  Login: undefined;
  Register: undefined;
  Dashboard: undefined;
  TestAR: undefined;
};

export type TouristStackParamList = {
  TouristDashboardMain: undefined;
  ProfileSettings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const TouristStack = createNativeStackNavigator<TouristStackParamList>();

// ---------------- APP NAVIGATOR ----------------
const AppNavigator: React.FC = () => {
  const { user, isLoading } = useContext<AuthContextData>(AuthContext);

  // 🌀 Loading state
  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  // ✅ Nested stack for Tourist role
  function TouristStackScreen() {
    return (
      <TouristStack.Navigator screenOptions={{ headerShown: false }}>
        <TouristStack.Screen
          name="TouristDashboardMain"
          component={TouristDashboard}
        />
        {/* Later we can add Profile/Settings here if needed */}
      </TouristStack.Navigator>
    );
  }

  // 🎯 Determine which dashboard to show
  const getDashboardScreen = (): ComponentType => {
    switch (user?.role) {
      case "Admin":
        return AdminDashboard;
      case "Tourist":
        return TouristTabNavigator; // ✅ Using Tab Navigator for Tourist
      case "Tourism Officer":
        return TourismDashboard;
      case "Business Owner":
        return BusinessDashboard;
      case "Event Organizer":
        return EventDashboard;
      default:
        return LoginScreen; // fallback
    }
  };

  const DashboardComponent = getDashboardScreen();

  return (
    <SafeAreaProvider>
      <SafeAreaView style={{ flex: 1 }}>
        <NavigationContainer>
          <Stack.Navigator screenOptions={{ headerShown: false }}>
            <Stack.Screen name="Dashboard" component={TouristTabNavigator} />
      </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaView>
  </SafeAreaProvider>
  );
};

export default AppNavigator;
