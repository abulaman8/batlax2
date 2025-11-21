import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import DoctorDashboard from '../views/DoctorDashboard.vue';
import PatientDashboard from '../views/PatientDashboard.vue';

const routes = [
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    {
        path: '/admin',
        component: AdminDashboard,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/doctor',
        component: DoctorDashboard,
        meta: { requiresAuth: true, role: 'doctor' }
    },
    {
        path: '/patient',
        component: PatientDashboard,
        meta: { requiresAuth: true, role: 'patient' }
    },
    { path: '/', redirect: '/login' }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// Navigation Guard
// Runs before every route change to check authentication
router.beforeEach((to, from, next) => {
    const isLoggedIn = store.getters.isLoggedIn;
    const userRole = store.getters.userRole;

    if (to.meta.requiresAuth) {
        if (!isLoggedIn) {
            // Redirect to login if not authenticated
            next('/login');
        } else if (to.meta.role && to.meta.role !== userRole) {
            // Redirect if role doesn't match (e.g., patient trying to access admin)
            next('/login');
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;
