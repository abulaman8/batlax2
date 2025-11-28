<template>
  <div class="container">
    <div class="row justify-content-center align-items-center min-vh-75">
      <div class="col-md-5 col-lg-4">
        <div class="text-center mb-4">
          <div class="icon-circle bg-primary text-white mx-auto mb-3 shadow-lg" style="width: 64px; height: 64px;">
            <i class="bi bi-hospital fs-2"></i>
          </div>
          <h3 class="fw-bold text-primary">Welcome Back</h3>
          <p class="text-muted">Sign in to your account</p>
        </div>
        
        <div class="card shadow-lg border-0 overflow-hidden">
          <div class="card-body p-5">
            <form @submit.prevent="handleLogin">
              <div class="mb-4">
                <label class="form-label text-uppercase small fw-bold text-muted">Username</label>
                <input v-model="username" type="text" class="form-control form-control-lg bg-light border-0" placeholder="Enter your username" required>
              </div>
              <div class="mb-4">
                <label class="form-label text-uppercase small fw-bold text-muted">Password</label>
                <input v-model="password" type="password" class="form-control form-control-lg bg-light border-0" placeholder="••••••••" required>
              </div>
              <div class="d-grid mb-4">
                <button type="submit" class="btn btn-primary btn-lg shadow-sm">Sign In</button>
              </div>
            </form>
            <div class="text-center">
              <p class="text-muted mb-0">Don't have an account? <router-link to="/register" class="text-primary fw-bold text-decoration-none">Register</router-link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    const username = ref('');
    const password = ref('');

    const handleLogin = async () => {
      try {
        const role = await store.dispatch('login', {
          username: username.value,
          password: password.value
        });
        
        if (role === 'admin') router.push('/admin');
        else if (role === 'doctor') router.push('/doctor');
        else router.push('/patient');
      } catch (error) {
        alert('Login failed: Invalid credentials');
      }
    };

    return { username, password, handleLogin };
  }
};
</script>

<style scoped>
.min-vh-75 { min-height: 75vh; }
.icon-circle { display: flex; align-items: center; justify-content: center; border-radius: 50%; }
</style>
