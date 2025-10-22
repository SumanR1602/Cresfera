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
    Dimensions,
    Switch,
    Alert,
} from 'react-native';

const { width } = Dimensions.get('window');

const RegisterScreen: React.FC = () => {
    const [form, setForm] = useState({
        first_name: '',
        last_name: '',
        email: '',
        mobile: '',
        password: '',
        confirm_password: '',
        dob: '',
        country: '',
        agreed: false,
    });

    const handleChange = (key: string, value: any) => {
        setForm({ ...form, [key]: value });
    };

    const GRAPHQL_ENDPOINT = 'http://localhost:8000/graphql';

    const handleRegister = async () => {
        if (!form.first_name || !form.email || !form.password) {
            Alert.alert('Error', 'Please fill all required fields');
            return;
        }
        if (form.password !== form.confirm_password) {
            Alert.alert('Error', 'Passwords do not match');
            return;
        }
        if (!form.agreed) {
            Alert.alert('Error', 'You must agree to the Terms and Privacy Policy');
            return;
        }

        const mutation = `
            mutation RegisterUser(
                $firstName: String!,
                $lastName: String!,
                $email: String!,
                $mobile: String!,
                $password: String!,
                $confirmPassword: String!,
                $dob: String!,
                $country: String!,
                $agreed: Boolean!
        ) {
            registerUser(
                firstName: $firstName,
                lastName: $lastName,
                email: $email,
                mobile: $mobile,
                password: $password,
                confirmPassword: $confirmPassword,
                dob: $dob,
                country: $country,
                agreed: $agreed
        ) {
        id
        firstName
        lastName
        email
    }
    }

    ` ;

        try {
            const response = await fetch(GRAPHQL_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: mutation,
                    variables: {
                        firstName: form.first_name,
                        lastName: form.last_name,
                        email: form.email,
                        mobile: form.mobile,
                        password: form.password,
                        confirmPassword: form.confirm_password,
                        dob: form.dob,
                        country: form.country,
                        agreed: form.agreed,
                    },
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.errors) {
                Alert.alert('Registration Error', data.errors[0].message);
                console.log('GraphQL errors:', data.errors);
                return;
            }

            Alert.alert('Success', `Welcome ${data.data.registerUser.firstName}!`);
            console.log('Registered user:', data.data.registerUser);
            router.push("/login");

        } catch (error: any) {
            console.error('Registration failed', error);
            Alert.alert('Error', error.message || 'Something went wrong. Please try again.');
        }

    };


    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        >
            <View style={styles.innerContainer}>
                <Image source={require('../assets/logo.png')} style={styles.logo} resizeMode="contain" />

                <Text style={styles.title}>Create Your Account</Text>

                {/* Name Row */}
                <View style={styles.row}>
                    <TextInput
                        style={[styles.input, styles.halfInput]}
                        placeholder="First Name"
                        value={form.first_name}
                        onChangeText={(v) => handleChange('first_name', v)}
                        placeholderTextColor="#9ca3af"
                    />
                    <TextInput
                        style={[styles.input, styles.halfInput]}
                        placeholder="Last Name"
                        value={form.last_name}
                        onChangeText={(v) => handleChange('last_name', v)}
                        placeholderTextColor="#9ca3af"
                    />
                </View>

                <TextInput
                    style={styles.input}
                    placeholder="Email Address"
                    keyboardType="email-address"
                    autoCapitalize="none"
                    value={form.email}
                    onChangeText={(v) => handleChange('email', v)}
                    placeholderTextColor="#9ca3af"
                />

                <TextInput
                    style={styles.input}
                    placeholder="Mobile Number"
                    keyboardType="phone-pad"
                    value={form.mobile}
                    onChangeText={(v) => handleChange('mobile', v)}
                    placeholderTextColor="#9ca3af"
                />

                <TextInput
                    style={styles.input}
                    placeholder="Date of Birth (YYYY-MM-DD)"
                    value={form.dob}
                    onChangeText={(v) => handleChange('dob', v)}
                    placeholderTextColor="#9ca3af"
                />

                <TextInput
                    style={styles.input}
                    placeholder="Country"
                    value={form.country}
                    onChangeText={(v) => handleChange('country', v)}
                    placeholderTextColor="#9ca3af"
                />

                <TextInput
                    style={styles.input}
                    placeholder="Password"
                    secureTextEntry
                    value={form.password}
                    onChangeText={(v) => handleChange('password', v)}
                    placeholderTextColor="#9ca3af"
                />

                <TextInput
                    style={styles.input}
                    placeholder="Confirm Password"
                    secureTextEntry
                    value={form.confirm_password}
                    onChangeText={(v) => handleChange('confirm_password', v)}
                    placeholderTextColor="#9ca3af"
                />
                {/* Terms Agreement */}
                <View style={styles.checkboxContainer}>
                    <TouchableOpacity
                        style={[styles.checkbox, form.agreed && styles.checkedBox]}
                        onPress={() => handleChange('agreed', !form.agreed)}
                    >
                        {form.agreed && <Text style={styles.checkmark}>✓</Text>}
                    </TouchableOpacity>
                    <Text style={styles.checkboxText}>I agree to the Terms and Privacy Policy</Text>
                </View>



                <TouchableOpacity style={styles.button} onPress={handleRegister}>
                    <Text style={styles.buttonText}>Register</Text>
                </TouchableOpacity>

                <Text style={styles.footerText}>
                    Already have an account?{' '}
                    <Text style={styles.link} onPress={() => console.log('Navigate to login')}>
                        Login
                    </Text>
                </Text>
            </View>
        </KeyboardAvoidingView>
    );
};

export default RegisterScreen;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8fafc',
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 20,
    },
    innerContainer: {
        width: '100%',
        maxWidth: 400,
        alignItems: 'center',
    },
    logo: {
        width: width * 0.35,
        height: width * 0.25,
        marginBottom: 10,
    },
    title: {
        fontSize: width < 400 ? 22 : 26,
        fontWeight: '700',
        color: '#172554',
        marginBottom: 20,
    },
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '100%',
    },
    input: {
        width: '100%',
        height: 46,
        backgroundColor: '#ffffff',
        borderColor: '#e5e7eb',
        borderWidth: 1,
        borderRadius: 10,
        paddingHorizontal: 14,
        fontSize: width < 400 ? 14 : 15,
        marginBottom: 12,
        color: '#111827',
    },
    halfInput: {
        width: '48%',
    },
    checkboxContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        width: '100%',
        marginVertical: 12,
    },
    checkbox: {
        width: 20,
        height: 20,
        borderRadius: 5,
        borderWidth: 1.5,
        borderColor: '#2563eb',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 10,
        backgroundColor: '#fff',
    },
    checkedBox: {
        backgroundColor: '#2563eb',
    },
    checkmark: {
        color: '#fff',
        fontSize: 14,
        fontWeight: 'bold',
    },
    checkboxText: {
        fontSize: width < 400 ? 13 : 14,
        color: '#374151',
        flexShrink: 1,
    },

    button: {
        width: '100%',
        backgroundColor: '#2563eb',
        borderRadius: 10,
        paddingVertical: 14,
        alignItems: 'center',
        shadowColor: '#2563eb',
        shadowOpacity: 0.2,
        shadowRadius: 4,
        shadowOffset: { width: 0, height: 2 },
    },
    buttonText: {
        color: '#ffffff',
        fontWeight: '600',
        fontSize: width < 400 ? 15 : 16,
    },
    footerText: {
        marginTop: 14,
        fontSize: width < 400 ? 13 : 14,
        color: '#334155',
    },
    link: {
        color: '#2563eb',
        fontWeight: '500',
    },
});
