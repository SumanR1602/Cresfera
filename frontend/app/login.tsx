import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Image,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { useRouter } from 'expo-router';
import { GRAPHQL_ENDPOINT } from '../config/constants';

const LoginScreen: React.FC = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLoginPress = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter both email and password');
      return;
    }

    const query = `
      mutation LoginUser($email: String!, $password: String!) {
        login(loginData: { email: $email, password: $password }) {
          success
          message
          accessToken
          refreshToken
        }
      }
    `;

    try {
      const response = await fetch(GRAPHQL_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          variables: { email, password },
        }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();

      if (data.errors) {
        console.log('GraphQL errors:', data.errors);
        Alert.alert('Login Error', data.errors[0].message);
        return;
      }

      const loginResult = data.data.login;

      if (!loginResult.success) {
        Alert.alert('Login Failed', loginResult.message);
        return;
      }

      await SecureStore.setItemAsync('accessToken', loginResult.accessToken);
      await SecureStore.setItemAsync('refreshToken', loginResult.refreshToken);

      Alert.alert('Success', loginResult.message);
      router.replace('/dashboard');
    } catch (error: any) {
      console.error('Login failed', error);
      Alert.alert('Error', error.message || 'Something went wrong');
    }
  };

  const handleRegisterPress = () => {
    router.push('/register');
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={styles.headerContainer}>
        <Image
          style={styles.logo}
          source={require('../assets/logo.png')}
          resizeMode="contain"
        />
        <Text style={styles.title}>Cresfera</Text>
        <Text style={styles.subtitle}>Sphere of Growth</Text>
      </View>

      <View style={styles.formContainer}>
        <TextInput
          style={styles.input}
          placeholder="Email address"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          placeholderTextColor="#9ca3af"
        />

        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          placeholderTextColor="#9ca3af"
        />

        <TouchableOpacity style={styles.button} onPress={handleLoginPress}>
          <Text style={styles.buttonText}>Sign In</Text>
        </TouchableOpacity>

        <View style={styles.footerContainer}>
          <Text style={styles.footerText}>
            Don’t have an account?{' '}
            <Text style={styles.registerLink} onPress={handleRegisterPress}>
              Register
            </Text>
          </Text>
        </View>
      </View>

      <Text style={styles.footerLegal}>Powered by Cresfera | Privacy Policy</Text>
    </KeyboardAvoidingView>
  );
};

export default LoginScreen;

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc', alignItems: 'center', justifyContent: 'center', padding: 24 },
  headerContainer: { alignItems: 'center', marginBottom: 40 },
  logo: { width: 130, height: 130, marginBottom: 8 },
  title: { fontSize: 32, fontWeight: '700', color: '#172554', letterSpacing: 0.5 },
  subtitle: { fontSize: 15, color: '#2563eb', marginTop: 4 },
  formContainer: { width: '100%', alignItems: 'center' },
  input: { width: '100%', height: 48, borderColor: '#e5e7eb', borderWidth: 1, borderRadius: 10, paddingHorizontal: 16, backgroundColor: '#ffffff', marginBottom: 14, fontSize: 15 },
  button: { width: '100%', backgroundColor: '#2563eb', borderRadius: 10, paddingVertical: 14, alignItems: 'center', marginTop: 8, shadowColor: '#2563eb', shadowOpacity: 0.2, shadowRadius: 4, shadowOffset: { width: 0, height: 2 } },
  buttonText: { color: '#ffffff', fontWeight: '600', fontSize: 16, letterSpacing: 0.3 },
  footerContainer: { marginTop: 16 },
  footerText: { fontSize: 14, color: '#334155' },
  registerLink: { color: '#2563eb', fontWeight: '500' },
  footerLegal: { position: 'absolute', bottom: 24, fontSize: 12, color: '#94a3b8' },
});
