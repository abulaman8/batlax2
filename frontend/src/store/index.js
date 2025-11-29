import { createStore } from 'vuex';
import apiClient from '../services/api';
export default createStore({
    state: {
        token: localStorage.getItem('token') || '',
        role: localStorage.getItem('role') || '',
        username: localStorage.getItem('username') || ''
    },
    mutations: {
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
        async login({ commit }, user) {
            const res = await apiClient.post('/login', user);
            const { access_token, role, username } = res.data;
            localStorage.setItem('token', access_token);
            localStorage.setItem('role', role);
            localStorage.setItem('username', username);
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
        isLoggedIn: state => !!state.token,
        userRole: state => state.role,
        currentUsername: state => state.username
    }
});
