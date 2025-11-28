<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <header class="hero-section">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-lg-6 hero-content px-5">
            <h1 class="display-4 fw-bold mb-4 text-white">Modern Healthcare for a Better Tomorrow</h1>
            <p class="lead mb-4 text-white opacity-90">Experience the future of hospital management. Streamlined appointments, secure records, and world-class care at your fingertips.</p>
            <div class="d-flex gap-3">
              <router-link to="/login" class="btn btn-light btn-lg px-4 text-primary fw-bold">Login</router-link>
              <router-link to="/register" class="btn btn-outline-light btn-lg px-4">Register Patient</router-link>
            </div>
          </div>
          <div class="col-lg-6 hero-image-container p-0">
             <img src="@/assets/hero-illustration.jpg" alt="Healthcare Illustration" class="img-fluid w-100 h-100 object-fit-cover hero-image" />
          </div>
        </div>
      </div>
    </header>

    <!-- Services Section -->
    <section class="services-section py-5">
      <div class="container">
        <h2 class="text-center mb-5 section-title">Our Services</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="card service-card h-100">
              <div class="card-body text-center">
                <div class="icon-wrapper mb-3">
                  <i class="bi bi-calendar-check fs-1 text-primary"></i>
                </div>
                <h5 class="card-title">Easy Booking</h5>
                <p class="card-text">Schedule appointments with top specialists in seconds. No waiting lines, no hassle.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card service-card h-100">
              <div class="card-body text-center">
                <div class="icon-wrapper mb-3">
                  <i class="bi bi-file-earmark-medical fs-1 text-primary"></i>
                </div>
                <h5 class="card-title">Digital Records</h5>
                <p class="card-text">Access your complete medical history, prescriptions, and doctor's notes securely from anywhere.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card service-card h-100">
              <div class="card-body text-center">
                <div class="icon-wrapper mb-3">
                  <i class="bi bi-shield-check fs-1 text-primary"></i>
                </div>
                <h5 class="card-title">Secure & Private</h5>
                <p class="card-text">Your health data is protected with state-of-the-art encryption and role-based access control.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer py-4 text-center text-white">
      <div class="container">
        <p class="mb-0">&copy; 2023 Hospital Management System. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing-page {
  font-family: 'Inter', sans-serif;
}

.hero-section {
  background: linear-gradient(135deg, var(--primary-color) 0%, #00251a 100%); /* Darker gradient end */
  color: white;
  padding: 100px 0;
  position: relative;
  overflow: hidden;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3); /* Add text shadow for contrast */
}

.hero-content {
  z-index: 2;
}

.hero-image {
  min-height: 500px;
  mask-image: linear-gradient(to right, transparent 0%, black 20%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 20%);
}

.section-title {
  color: var(--primary-dark);
  font-weight: 700;
}

.service-card {
  border: none;
  border-radius: 15px;
  box-shadow: var(--card-shadow);
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-10px);
}

.icon-wrapper {
  height: 80px;
  width: 80px;
  background-color: var(--bg-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.footer {
  background-color: var(--primary-dark);
}
</style>
