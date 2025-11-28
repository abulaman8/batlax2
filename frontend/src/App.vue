<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4" v-if="isLoggedIn">
      <div class="container-fluid px-5">
        <a class="navbar-brand" href="#">HMS</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    
    const isLoggedIn = computed(() => store.getters.isLoggedIn);
    
    const logout = () => {
      store.dispatch('logout');
      router.push('/login');
    };
    
    return { isLoggedIn, logout };
  }
};
</script>

<style>
body {
  background-color: #f8f9fa;
}
</style>
