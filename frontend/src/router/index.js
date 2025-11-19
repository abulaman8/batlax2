import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import DoctorDashboard from '../views/DoctorDashboard.vue';
import PatientDashboard from '../views/PatientDashboard.vue';

const routes = [
    { path: '/', redirect: '/login' },
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
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.getters.isLoggedIn) {
            next('/login');
            return;
        }
        if (to.meta.role && store.getters.userRole !== to.meta.role) {
            next('/login'); // Or unauthorized page
            return;
        }
    }
    next();
});

export default router;
