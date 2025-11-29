import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import DoctorDashboard from '../views/DoctorDashboard.vue';
import PatientDashboard from '../views/PatientDashboard.vue';
import LandingPage from '../views/LandingPage.vue';
const routes = [
    { path: '/', component: LandingPage },
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
    }
];
const router = createRouter({
    history: createWebHistory(),
    routes
});
router.beforeEach((to, from, next) => {
    const isLoggedIn = store.getters.isLoggedIn;
    const userRole = store.getters.userRole;
    if (to.meta.requiresAuth) {
        if (!isLoggedIn) {
            next('/login');
        } else if (to.meta.role && to.meta.role !== userRole) {
            next('/login');
        } else {
            next();
        }
    } else {
        next();
    }
});
export default router;
