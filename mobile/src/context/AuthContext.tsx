import React, { createContext, useState, useEffect, ReactNode } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";
import { API_BASE_URL } from "../config/api";

const api = axios.create({
  baseURL: API_BASE_URL,
});

interface User {
  username: string;
  email: string;
  role: string;
}

export interface AuthContextData {
  user: User | null;
  userToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isLoading: boolean;
}

export const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [userToken, setUserToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadToken = async () => {
      try {
        const token = await AsyncStorage.getItem("userToken");
        if (token) {
          setUserToken(token);
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          try {
            const response = await api.get("/api/auth/me/");
            setUser(response.data);
          } catch (error) {
            console.error("Error fetching user profile:", error);
            // Token might be invalid, log out the user
            await logout();
          }
        }
      } catch (err) {
        console.error("Error loading token:", err);
      } finally {
        setIsLoading(false);
      }
    };
    loadToken();
  }, []);

  const login = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await api.post("/api/auth/token/", { username, password });
      const token = response.data.access;
      await AsyncStorage.setItem("userToken", token);
      setUserToken(token);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const userResponse = await api.get("/api/auth/me/");
      setUser(userResponse.data);
    } catch (err: any) {
      console.error("Login failed:", err.response?.data || err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await AsyncStorage.removeItem("userToken");
      setUserToken(null);
      setUser(null);
      delete api.defaults.headers.common['Authorization'];
    } catch (err) {
      console.error("Logout failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, userToken, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};