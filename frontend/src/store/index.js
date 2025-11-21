import { createStore } from 'vuex';
import apiClient from '../services/api';

// Vuex Store
// Centralized state management for the application.
export default createStore({
    state: {
        // Initial state: Check localStorage for existing session data
        token: localStorage.getItem('token') || '',
        role: localStorage.getItem('role') || '',
        username: localStorage.getItem('username') || ''
    },
    mutations: {
        // Mutations are the ONLY way to change state
        auth_success(state, payload) {
            state.token = payload.token;
            state.role = payload.role;
            state.username = payload.username;
        },
        logout(state) {
            state.token = '';
            state.role = '';
            state.username = '';
        }
    },
    actions: {
        // Actions handle asynchronous operations (like API calls)
        async login({ commit }, user) {
            const res = await apiClient.post('/login', user);
            const { access_token, role, username } = res.data;

            // Save to localStorage for persistence
            localStorage.setItem('token', access_token);
            localStorage.setItem('role', role);
            localStorage.setItem('username', username);

            // Commit mutation to update state
            commit('auth_success', { token: access_token, role, username });
            return role;
        },
        async register({ commit }, user) {
            await apiClient.post('/register', user);
        },
        logout({ commit }) {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            localStorage.removeItem('username');
            commit('logout');
        }
    },
    getters: {
        // Getters are like computed properties for the store
        isLoggedIn: state => !!state.token,
        userRole: state => state.role,
        currentUsername: state => state.username
    }
});
