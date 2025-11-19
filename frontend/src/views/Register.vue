<template>
  <div class="row justify-content-center align-items-center min-vh-75">
    <div class="col-md-5 col-lg-4">
      <div class="text-center mb-4">
        <h3 class="fw-bold text-primary">Create Account</h3>
        <p class="text-muted">Join our medical platform</p>
      </div>
      
      <div class="card shadow-lg border-0 overflow-hidden">
        <div class="card-body p-5">
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label class="form-label text-uppercase small fw-bold text-muted">Username</label>
              <input v-model="username" type="text" class="form-control form-control-lg bg-light border-0" required>
            </div>
            <div class="mb-3">
              <label class="form-label text-uppercase small fw-bold text-muted">Email</label>
              <input v-model="email" type="email" class="form-control form-control-lg bg-light border-0" required>
            </div>
            <div class="mb-4">
              <label class="form-label text-uppercase small fw-bold text-muted">Password</label>
              <input v-model="password" type="password" class="form-control form-control-lg bg-light border-0" required>
            </div>
            <div class="d-grid mb-4">
              <button type="submit" class="btn btn-success btn-lg shadow-sm text-white">Create Account</button>
            </div>
          </form>
          <div class="text-center">
            <p class="text-muted mb-0">Already have an account? <router-link to="/login" class="text-primary fw-bold text-decoration-none">Login</router-link></p>
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
    const email = ref('');
    const password = ref('');

    const handleRegister = async () => {
      try {
        await store.dispatch('register', {
          username: username.value,
          email: email.value,
          password: password.value
        });
        alert('Registration successful! Please login.');
        router.push('/login');
      } catch (error) {
        alert('Registration failed');
      }
    };

    return { username, email, password, handleRegister };
  }
};
</script>

<style scoped>
.min-vh-75 { min-height: 75vh; }
</style>
