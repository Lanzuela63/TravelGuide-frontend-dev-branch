import React, { useState, useContext, FC } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import {
  TextInput,
  Button,
  Card,
  Title,
  IconButton,
  Text,
  Checkbox,
  HelperText,
} from 'react-native-paper';
import { Picker } from '@react-native-picker/picker';
import { useNavigation } from '@react-navigation/native';
import { AuthContext } from '../context/AuthContext';

const RegisterScreen: FC = () => {
  const navigation = useNavigation<any>();
  const { register, isLoading, error } = useContext(AuthContext);

  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [role, setRole] = useState<string>('Tourist');
  const [agreedToTerms, setAgreedToTerms] = useState<boolean>(false);

  const getPasswordStrength = () => {
    if (password.length === 0) return { strength: '', color: 'transparent' };
    if (password.length < 6) return { strength: 'Weak', color: 'red' };
    if (password.length < 10) return { strength: 'Medium', color: 'orange' };
    return { strength: 'Strong', color: 'green' };
  };

  const onRegisterPress = () => {
    if (!username || !email || !password || !role || !confirmPassword) {
      Alert.alert('Validation Error', 'Please fill in all fields.');
      return;
    }
    if (password !== confirmPassword) {
      Alert.alert('Validation Error', 'Passwords do not match.');
      return;
    }
    if (!agreedToTerms) {
      Alert.alert('Validation Error', 'Please agree to the terms and conditions.');
      return;
    }
    register({ username, email, password, role, navigation });
  };

  const passwordStrength = getPasswordStrength();

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardAvoidingView}
      >
        <Card style={styles.card}>
          <Card.Content>
            <View style={styles.header}>
              <IconButton icon="arrow-left" onPress={() => navigation.goBack()} />
              <Title style={styles.title}>Create an Account</Title>
            </View>

            {error && <Text style={styles.errorText}>{error}</Text>}

            <TextInput
              label="Username"
              value={username}
              onChangeText={setUsername}
              mode="outlined"
              style={styles.input}
              left={<TextInput.Icon icon="account" />}
            />

            <TextInput
              label="Email"
              value={email}
              onChangeText={setEmail}
              mode="outlined"
              keyboardType="email-address"
              autoCapitalize="none"
              style={styles.input}
              left={<TextInput.Icon icon="email" />}
            />

            <TextInput
              label="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              mode="outlined"
              style={styles.input}
              left={<TextInput.Icon icon="lock" />}
            />
            <HelperText type="info" style={{ color: passwordStrength.color }}>
              Password Strength: {passwordStrength.strength}
            </HelperText>

            <TextInput
              label="Confirm Password"
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry
              mode="outlined"
              style={styles.input}
              left={<TextInput.Icon icon="lock-check" />}
            />

            <Text style={styles.roleLabel}>Select Role</Text>
            <View style={styles.pickerWrapper}>
              <Picker
                selectedValue={role}
                onValueChange={(itemValue: string) => setRole(itemValue)}
              >
                <Picker.Item label="Tourist" value="Tourist" />
                <Picker.Item label="Tourism Officer" value="Tourism Officer" />
                <Picker.Item label="Business Owner" value="Business Owner" />
                <Picker.Item label="Event Organizer" value="Event Organizer" />
              </Picker>
            </View>

            <View style={styles.checkboxContainer}>
              <Checkbox
                status={agreedToTerms ? 'checked' : 'unchecked'}
                onPress={() => setAgreedToTerms(!agreedToTerms)}
              />
              <Text style={styles.checkboxLabel}>I agree to the Terms and Conditions</Text>
            </View>

            <Button
              mode="contained"
              onPress={onRegisterPress}
              style={styles.registerButton}
              loading={isLoading}
              disabled={isLoading}
            >
              {isLoading ? 'Registering...' : 'Register'}
            </Button>
          </Card.Content>
        </Card>
      </KeyboardAvoidingView>
    </ScrollView>
  );
};

export default RegisterScreen;

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f0f4f8',
  },
  keyboardAvoidingView: {
    flex: 1,
    justifyContent: 'center',
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
    marginBottom: 12,
  },
  roleLabel: {
    marginTop: 16,
    marginBottom: 4,
    fontSize: 16,
  },
  pickerWrapper: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    overflow: 'hidden',
    marginBottom: 12,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  checkboxLabel: {
    marginLeft: 8,
  },
  registerButton: {
    marginTop: 10,
    paddingVertical: 8,
  },
  errorText: {
    color: 'red',
    textAlign: 'center',
    marginBottom: 10,
  },
});
