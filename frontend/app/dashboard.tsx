import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';

const Dashboard: React.FC = () => {
  const router = useRouter();

  const handleLogout = () => {
    // TODO: Add token removal logic
    router.replace('/login'); // Go back to login
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.welcomeText}>Welcome back,</Text>
          <Text style={styles.username}>Suman 👋</Text>
        </View>
        <TouchableOpacity onPress={handleLogout}>
          <Image
            source={require('../assets/logo.png')}
            style={styles.logoutIcon}
          />
        </TouchableOpacity>
      </View>

      {/* Overview Section */}
      <View style={styles.overviewCard}>
        <Text style={styles.cardTitle}>Your Progress</Text>
        <Text style={styles.cardSubtitle}>Keep growing each day!</Text>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: '70%' }]} />
        </View>
        <Text style={styles.progressText}>70% Complete</Text>
      </View>

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <View style={styles.actionsRow}>
          <TouchableOpacity style={styles.actionCard}>
            <Image
              source={require('../assets/logo.png')}
              style={styles.actionIcon}
            />
            <Text style={styles.actionText}>Profile</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionCard}>
            <Image
              source={require('../assets/logo.png')}
              style={styles.actionIcon}
            />
            <Text style={styles.actionText}>Tasks</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionCard}>
            <Image
              source={require('../assets/logo.png')}
              style={styles.actionIcon}
            />
            <Text style={styles.actionText}>Analytics</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Tips Section */}
      <View style={styles.tipCard}>
        <Text style={styles.tipTitle}>💡 Daily Tip</Text>
        <Text style={styles.tipText}>
          "Consistency beats intensity. Take one step every day towards your goal."
        </Text>
      </View>
    </ScrollView>
  );
};

export default Dashboard;

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#f8fafc',
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 25,
  },
  welcomeText: {
    fontSize: 16,
    color: '#64748b',
  },
  username: {
    fontSize: 24,
    fontWeight: '700',
    color: '#172554',
  },
  logoutIcon: {
    width: 26,
    height: 26,
    tintColor: '#2563eb',
  },
  overviewCard: {
    backgroundColor: '#2563eb',
    borderRadius: 15,
    padding: 20,
    marginBottom: 25,
    shadowColor: '#2563eb',
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 4,
  },
  cardTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
  },
  cardSubtitle: {
    color: '#e0f2fe',
    fontSize: 14,
    marginTop: 5,
    marginBottom: 15,
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: '#3b82f6',
    borderRadius: 5,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#93c5fd',
  },
  progressText: {
    color: '#f0f9ff',
    fontSize: 13,
    marginTop: 6,
    textAlign: 'right',
  },
  section: {
    marginBottom: 25,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#172554',
    marginBottom: 10,
  },
  actionsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    alignItems: 'center',
    width: '30%',
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  actionIcon: {
    width: 36,
    height: 36,
    marginBottom: 8,
    tintColor: '#2563eb',
  },
  actionText: {
    fontSize: 13,
    color: '#334155',
    fontWeight: '500',
  },
  tipCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 18,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    marginBottom: 20,
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#172554',
    marginBottom: 8,
  },
  tipText: {
    fontSize: 14,
    color: '#475569',
    lineHeight: 20,
  },
});
