<template>
  <div class="fade-in">
    <div class="container">
      <h2 class="mb-4 fw-bold text-primary">Admin Dashboard</h2>
      <div class="row mb-5">
        <div class="col-md-4">
          <div class="card bg-white h-100 border-0 shadow-hover border-start border-4 border-primary">
            <div class="card-body d-flex align-items-center justify-content-between">
              <div>
                <h6 class="text-uppercase mb-2 text-muted fw-bold">Total Doctors</h6>
                <h2 class="display-4 fw-bold mb-0 text-dark">{{ stats.doctors }}</h2>
              </div>
              <div class="icon-circle bg-primary-subtle text-primary">
                <i class="bi bi-person-badge fs-2"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card bg-white h-100 border-0 shadow-hover border-start border-4 border-success">
            <div class="card-body d-flex align-items-center justify-content-between">
              <div>
                <h6 class="text-uppercase mb-2 text-muted fw-bold">Total Patients</h6>
                <h2 class="display-4 fw-bold mb-0 text-dark">{{ stats.patients }}</h2>
              </div>
              <div class="icon-circle bg-success-subtle text-success">
                <i class="bi bi-people fs-2"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card bg-white h-100 border-0 shadow-hover border-start border-4 border-info">
            <div class="card-body d-flex align-items-center justify-content-between">
              <div>
                <h6 class="text-uppercase mb-2 text-muted fw-bold">Appointments</h6>
                <h2 class="display-4 fw-bold mb-0 text-dark">{{ stats.appointments }}</h2>
              </div>
              <div class="icon-circle bg-info-subtle text-info">
                <i class="bi bi-calendar-check fs-2"></i>
              </div>
            </div>
            <div class="card-footer bg-white border-0 pt-0">
              <button class="btn btn-sm btn-outline-info w-100 rounded-pill" @click="showAppointmentsModal = true">View All</button>
            </div>
          </div>
        </div>
        <div class="col-md-4 mt-4">
          <div class="card bg-white h-100 border-0 shadow-hover border-start border-4 border-warning">
            <div class="card-body d-flex align-items-center justify-content-between">
              <div>
                <h6 class="text-uppercase mb-2 text-muted fw-bold">Departments</h6>
                <h2 class="display-4 fw-bold mb-0 text-dark">{{ departments.length }}</h2>
              </div>
              <div class="icon-circle bg-warning-subtle text-warning">
                <i class="bi bi-building fs-2"></i>
              </div>
            </div>
            <div class="card-footer bg-white border-0 pt-0">
              <button class="btn btn-sm btn-outline-warning w-100 rounded-pill" @click="showDepartmentsModal = true">Manage</button>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12 mb-4">
          <div class="card h-100">
            <div class="card-header bg-white py-3">
              <h5 class="mb-0 fw-bold">Hospital Analytics</h5>
            </div>
            <div class="card-body">
              <div style="height: 300px;">
                <Bar v-if="chartData.labels" :data="chartData" :options="chartOptions" />
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-7">
          <div class="card h-100">
            <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
              <h5 class="mb-0 fw-bold">Medical Staff</h5>
              <button class="btn btn-primary btn-sm rounded-pill px-3" @click="showAddModal = true">
                + Add Doctor
              </button>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="bg-light">
                    <tr>
                      <th class="ps-4">Doctor</th>
                      <th>Department</th>
                      <th>Status</th>
                      <th class="text-end pe-4">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="doc in doctors" :key="doc.id">
                      <td class="ps-4">
                        <div class="d-flex align-items-center">
                          <div class="avatar-circle bg-primary-subtle text-primary me-3">
                            {{ doc.username.charAt(0).toUpperCase() }}
                          </div>
                          <div>
                            <div class="fw-bold">{{ doc.username }}</div>
                            <div class="text-muted small">{{ doc.email }}</div>
                          </div>
                        </div>
                      </td>
                      <td><span class="text-muted small">{{ doc.department || 'N/A' }}</span></td>
                      <td>
                        <span v-if="doc.is_active" class="badge bg-success-subtle text-success-emphasis">Active</span>
                        <span v-else class="badge bg-danger-subtle text-danger-emphasis">Inactive</span>
                      </td>
                      <td class="text-end pe-4">
                        <button v-if="doc.is_active" @click="deleteDoctor(doc.id)" class="btn btn-link text-danger p-0">
                          Deactivate
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-5">
          <div class="card h-100">
            <div class="card-header bg-white py-3">
              <h5 class="mb-0 fw-bold">Recent Patients</h5>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li v-for="p in patients.slice(0, 5)" :key="p.id" class="list-group-item d-flex justify-content-between align-items-center px-0">
                  <div class="d-flex align-items-center">
                    <div class="avatar-circle bg-secondary-subtle text-secondary me-3">
                      {{ p.username.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <div class="fw-bold">{{ p.username }}</div>
                      <div class="text-muted small">{{ p.email }}</div>
                    </div>
                  </div>
                  <button class="btn btn-sm btn-outline-secondary rounded-pill" @click="viewPatient(p)">View</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showAddModal" class="modal-backdrop fade show"></div>
      <div v-if="showAddModal" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content border-0 shadow-lg">
            <div class="modal-header bg-primary text-white">
              <h5 class="modal-title">Add New Doctor</h5>
              <button type="button" class="btn-close btn-close-white" @click="showAddModal = false"></button>
            </div>
            <div class="modal-body p-4">
              <form @submit.prevent="addDoctor">
                <div class="mb-3">
                  <label class="form-label text-muted small text-uppercase fw-bold">Full Name</label>
                  <input v-model="newDoctor.username" class="form-control form-control-lg" required>
                </div>
                <div class="mb-3">
                  <label class="form-label text-muted small text-uppercase fw-bold">Email Address</label>
                  <input v-model="newDoctor.email" type="email" class="form-control form-control-lg" required>
                </div>
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <label class="form-label text-muted small text-uppercase fw-bold">Password</label>
                    <input v-model="newDoctor.password" type="password" class="form-control form-control-lg" required>
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label text-muted small text-uppercase fw-bold">Department</label>
                  <select v-model="newDoctor.department_id" class="form-select form-select-lg">
                    <option value="" disabled>Select Department</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                  </select>
                </div>
                <div class="d-grid mt-4">
                  <button type="submit" class="btn btn-primary btn-lg">Create Profile</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      </div>
      <div v-if="showAppointmentsModal" class="modal-backdrop fade show"></div>
      <div v-if="showAppointmentsModal" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content border-0 shadow-lg">
            <div class="modal-header bg-info text-white">
              <h5 class="modal-title">All Appointments</h5>
              <button type="button" class="btn-close btn-close-white" @click="showAppointmentsModal = false"></button>
            </div>
            <div class="modal-body p-0">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="bg-light">
                    <tr>
                      <th class="ps-4">Date & Time</th>
                      <th>Doctor</th>
                      <th>Patient</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="appt in appointments" :key="appt.id">
                      <td class="ps-4">
                        <div class="fw-bold">{{ appt.date }}</div>
                        <div class="text-muted small">{{ appt.time }}</div>
                      </td>
                      <td>{{ appt.doctor_name }}</td>
                      <td>{{ appt.patient_name }}</td>
                      <td>
                        <span v-if="appt.status === 'Booked'" class="badge bg-primary-subtle text-primary-emphasis">Booked</span>
                        <span v-else-if="appt.status === 'Completed'" class="badge bg-success-subtle text-success-emphasis">Completed</span>
                        <span v-else class="badge bg-secondary-subtle text-secondary-emphasis">{{ appt.status }}</span>
                      </td>
                    </tr>
                    <tr v-if="appointments.length === 0">
                      <td colspan="4" class="text-center py-4 text-muted">No appointments found.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="selectedPatient" class="modal-backdrop fade show"></div>
      <div v-if="selectedPatient" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content border-0 shadow-lg">
            <div class="modal-header bg-success text-white">
              <h5 class="modal-title">Patient Details</h5>
              <button type="button" class="btn-close btn-close-white" @click="selectedPatient = null"></button>
            </div>
            <div class="modal-body p-4 text-center">
              <div class="avatar-circle bg-success-subtle text-success mx-auto mb-3" style="width: 80px; height: 80px; font-size: 2rem;">
                {{ selectedPatient.username.charAt(0).toUpperCase() }}
              </div>
              <h4 class="fw-bold mb-1">{{ selectedPatient.username }}</h4>
              <p class="text-muted mb-4">{{ selectedPatient.email }}</p>
              <div class="row text-start">
                <div class="col-6 mb-3">
                  <label class="small text-muted text-uppercase fw-bold">Contact</label>
                  <div class="fw-bold">{{ selectedPatient.contact || 'N/A' }}</div>
                </div>
                <div class="col-6 mb-3">
                  <label class="small text-muted text-uppercase fw-bold">Status</label>
                  <div>
                    <span v-if="selectedPatient.is_active" class="badge bg-success-subtle text-success-emphasis">Active</span>
                    <span v-else class="badge bg-danger-subtle text-danger-emphasis">Inactive</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showDepartmentsModal" class="modal-backdrop fade show"></div>
      <div v-if="showDepartmentsModal" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content border-0 shadow-lg">
            <div class="modal-header bg-warning text-white">
              <h5 class="modal-title">Manage Departments</h5>
              <button type="button" class="btn-close btn-close-white" @click="showDepartmentsModal = false"></button>
            </div>
            <div class="modal-body p-4">
              <form @submit.prevent="addDepartment" class="mb-4">
                <div class="input-group">
                  <input v-model="newDepartment" class="form-control" placeholder="New Department Name" required>
                  <button class="btn btn-warning text-white" type="submit">Add</button>
                </div>
              </form>
              <ul class="list-group">
                <li v-for="dept in departments" :key="dept.id" class="list-group-item d-flex justify-content-between align-items-center">
                  {{ dept.name }}
                  <span class="badge bg-secondary rounded-pill">{{ dept.id }}</span>
                </li>
                <li v-if="departments.length === 0" class="list-group-item text-center text-muted">No departments found.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
import { ref, onMounted, computed } from 'vue';
import apiClient from '../services/api';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);
export default {
  components: { Bar },
  setup() {
    const stats = ref({ doctors: 0, patients: 0, appointments: 0 });
    const doctors = ref([]);
    const patients = ref([]);
    const appointments = ref([]);
    const departments = ref([]);
    const showAddModal = ref(false);
    const showAppointmentsModal = ref(false);
    const showDepartmentsModal = ref(false);
    const selectedPatient = ref(null);
    const newDoctor = ref({ username: '', email: '', password: '', department_id: '' });
    const newDepartment = ref('');
    const chartData = computed(() => ({
      labels: ['Doctors', 'Patients', 'Appointments'],
      datasets: [{
        label: 'Hospital Data',
        backgroundColor: ['#00695c', '#ff6f00', '#0288d1'],
        data: [stats.value.doctors, stats.value.patients, stats.value.appointments],
        borderRadius: 8
      }]
    }));
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true, grid: { display: false } },
        x: { grid: { display: false } }
      }
    };
    const fetchData = async () => {
      try {
        const statsRes = await apiClient.get('/api/admin/stats');
        stats.value = statsRes.data;
        const docsRes = await apiClient.get('/api/admin/doctors');
        doctors.value = docsRes.data;
        const patientsRes = await apiClient.get('/api/admin/patients');
        patients.value = patientsRes.data;
        const apptsRes = await apiClient.get('/api/admin/appointments');
        appointments.value = apptsRes.data;
        const deptsRes = await apiClient.get('/api/admin/departments');
        departments.value = deptsRes.data;
      } catch (error) {
        if (error.response && (error.response.status === 401 || error.response.status === 422)) {
           localStorage.removeItem('token');
           window.location.href = '/login';
        }
      }
    };
    const addDoctor = async () => {
      await apiClient.post('/api/admin/doctors', newDoctor.value);
      newDoctor.value = { username: '', email: '', password: '', department_id: '' };
      showAddModal.value = false;
      fetchData();
    };
    const addDepartment = async () => {
      await apiClient.post('/api/admin/departments', { name: newDepartment.value });
      newDepartment.value = '';
      fetchData();
    };
    const deleteDoctor = async (id) => {
      if(confirm('Are you sure you want to deactivate this doctor?')) {
        await apiClient.delete(`/api/admin/doctors/${id}`);
        fetchData();
      }
    };
    const viewPatient = (patient) => {
      selectedPatient.value = patient;
    };
    onMounted(fetchData);
    return { stats, doctors, patients, appointments, departments, newDoctor, newDepartment, showAddModal, showAppointmentsModal, showDepartmentsModal, selectedPatient, addDoctor, addDepartment, deleteDoctor, viewPatient, chartData, chartOptions };
  }
};
</script>
<style scoped>
.bg-gradient-primary { background: linear-gradient(45deg, #00695c, #4db6ac); }
.bg-gradient-success { background: linear-gradient(45deg, #2e7d32, #81c784); }
.bg-gradient-info { background: linear-gradient(45deg, #0277bd, #4fc3f7); }
.shadow-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.15) !important; }
.icon-circle { width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.avatar-circle { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.fade-in { animation: fadeIn 0.5s ease-in; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
