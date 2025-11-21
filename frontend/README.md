# Frontend Documentation

This directory contains the Vue.js 3 application for the Hospital Management System UI.

## Project Structure

- **`src/main.js`**: The entry point of the Vue application. It initializes the app, mounts the router and store, and imports global styles.
- **`src/App.vue`**: The root component. It contains the main layout (navigation bar) and the `<router-view>` where pages are rendered.
- **`src/router/index.js`**: Defines the application routes (URLs) and maps them to components. It also handles **Navigation Guards** to protect routes (e.g., redirecting unauthenticated users to login).
- **`src/store/index.js`**: Uses **Vuex** for state management. It stores the user's authentication state (token, role, username) globally so it can be accessed by any component.
- **`src/services/api.js`**: Configures **Axios**, the HTTP client used to make requests to the Backend API. It includes interceptors to automatically attach the JWT token to every request.
- **`src/views/`**: Contains the page components:
  - `Login.vue`: User login page.
  - `Register.vue`: Patient registration page.
  - `AdminDashboard.vue`: Dashboard for admins.
  - `DoctorDashboard.vue`: Dashboard for doctors.
  - `PatientDashboard.vue`: Dashboard for patients.
- **`src/assets/`**: Static assets like CSS files and images.

## Key Concepts

- **Vue 3 Composition API**: We use the `setup()` function and `ref`/`computed` for reactive state management in components.
- **Vuex**: Centralized store for data that needs to be shared across multiple components (like "Is the user logged in?").
- **Vite**: The build tool and development server. It provides fast hot module replacement (HMR).
