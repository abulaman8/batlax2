import { createStore } from 'vuex';
import apiClient from '../services/api';

export default createStore({
    state: {
        token: localStorage.getItem('token') || '',
        user: null,
        role: localStorage.getItem('role') || '',
    },
    mutations: {
        auth_success(state, { token, role, user }) {
            state.token = token;
            state.role = role;
            state.user = user;
        },
        logout(state) {
            state.token = '';
            state.role = '';
            state.user = null;
        },
    },
    actions: {
        async login({ commit }, user) {
            const response = await apiClient.post('/login', user);
            const token = response.data.access_token;
            const role = response.data.role;
            const username = response.data.username;

            localStorage.setItem('token', token);
            localStorage.setItem('role', role);

            commit('auth_success', { token, role, user: { username } });
            return role;
        },
        async register({ commit }, user) {
            await apiClient.post('/register', user);
        },
        logout({ commit }) {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            commit('logout');
        },
    },
    getters: {
        isLoggedIn: state => !!state.token,
        userRole: state => state.role,
    },
});
