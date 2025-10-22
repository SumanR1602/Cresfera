import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated, Easing } from 'react-native';
import { useRouter } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';

// Prevent native splash from auto-hiding before animation runs
SplashScreen.preventAutoHideAsync();

const SplashScreenPage: React.FC = () => {
  const router = useRouter();

  // Animated values
  const logoScale = useRef(new Animated.Value(0.2)).current;
  const logoOpacity = useRef(new Animated.Value(0)).current;
  const textFade = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Run logo animations in parallel
    Animated.parallel([
      Animated.spring(logoScale, {
        toValue: 1,
        useNativeDriver: true,
        friction: 4,
        tension: 60,
      }),
      Animated.timing(logoOpacity, {
        toValue: 1,
        duration: 1200,
        easing: Easing.inOut(Easing.ease),
        useNativeDriver: true,
      }),
    ]).start(() => {
      // Fade in text after logo animation finishes
      Animated.timing(textFade, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }).start(async () => {
        // Hide native splash screen after animations
        await SplashScreen.hideAsync();

        // Navigate smoothly after fade-in completes
        router.replace('/login');
      });
    });
  }, []);

  return (
    <View style={styles.container}>
      <Animated.Image
        source={require('../assets/logo.png')} // Make sure path is correct
        style={[
          styles.logo,
          {
            transform: [{ scale: logoScale }],
            opacity: logoOpacity,
          },
        ]}
        resizeMode="contain"
      />
      <Animated.Text style={[styles.title, { opacity: textFade }]}>
        Welcome to Cresfera
      </Animated.Text>
      <Animated.Text style={[styles.subtitle, { opacity: textFade }]}>
        Empowering your financial decisions with AI
      </Animated.Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#181A20',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    height: 140,
    width: 140,
    marginBottom: 24,
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 16,
    shadowOffset: { width: 0, height: 4 },
    backgroundColor: 'white',
    borderRadius: 30,
  },
  title: {
    fontSize: 28,
    color: '#5bbcff',
    fontWeight: 'bold',
    letterSpacing: 2,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    color: '#A0A0A0',
    marginTop: 8,
    textAlign: 'center',
    paddingHorizontal: 40,
  },
});

export default SplashScreenPage;
