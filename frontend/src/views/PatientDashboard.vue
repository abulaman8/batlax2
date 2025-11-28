<template>
  <div class="fade-in">
    <div class="container">
      <h2 class="mb-4 fw-bold text-primary">Patient Portal</h2>
    
    <div class="row">
      <!-- Booking Section -->
      <div class="col-md-8">
        <div class="card h-100">
          <div class="card-header bg-white py-3">
            <h5 class="mb-0 fw-bold">Find a Specialist</h5>
          </div>
          <div class="card-body">
            <div class="input-group mb-4 shadow-sm">
              <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
              <input v-model="searchSpec" placeholder="Search by Specialization (e.g., Cardiology, Dentist)" class="form-control border-start-0 ps-0" @input="searchDoctors">
            </div>

            <div v-if="doctors.length > 0" class="row g-3">
              <div v-for="doc in doctors" :key="doc.id" class="col-md-6">
                <div class="card h-100 border shadow-sm doctor-card">
                  <div class="card-body">
                    <div class="d-flex align-items-center mb-3">
                      <div class="avatar-circle bg-primary text-white me-3">{{ doc.name.charAt(0) }}</div>
                      <div>
                        <h6 class="mb-0 fw-bold">{{ doc.name }}</h6>
                        <small class="text-muted">{{ doc.specialization }}</small>
                      </div>
                    </div>
                    <form @submit.prevent="bookAppointment(doc.id)">
                      <div class="mb-2">
                        <label class="small text-muted">Date</label>
                        <input type="date" v-model="bookingDate" class="form-control form-control-sm" required>
                      </div>
                      <div class="mb-3">
                        <label class="small text-muted">Time</label>
                        <input type="time" v-model="bookingTime" class="form-control form-control-sm" required>
                      </div>
                      <button class="btn btn-primary btn-sm w-100 rounded-pill">Book Appointment</button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
            <div v-else-if="searchSpec.length > 2" class="text-center py-5 text-muted">
              <p>No doctors found for "{{ searchSpec }}"</p>
            </div>
            <div v-else class="text-center py-5 text-muted">
              <i class="bi bi-search display-4 mb-3 d-block opacity-25"></i>
              <p>Start typing to find a doctor...</p>
            </div>
          </div>
        </div>
      </div>

      <!-- History Section -->
      <div class="col-md-4">
        <div class="card h-100">
          <div class="card-header bg-white py-3">
            <h5 class="mb-0 fw-bold">Medical History</h5>
          </div>
          <div class="card-body p-0">
            <div class="list-group list-group-flush">
              <div v-for="appt in history" :key="appt.id" class="list-group-item p-3 border-bottom">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h6 class="mb-0 fw-bold">Dr. {{ appt.doctor_name }}</h6>
                    <small class="text-muted">{{ appt.date }} at {{ appt.time }}</small>
                  </div>
                  <span :class="statusBadge(appt.status)">{{ appt.status }}</span>
                </div>
                <div v-if="appt.diagnosis" class="mt-2 bg-light p-2 rounded">
                  <small class="d-block text-muted fw-bold text-uppercase" style="font-size: 0.7rem;">Diagnosis</small>
                  <p class="mb-1 small">{{ appt.diagnosis }}</p>
                  <div v-if="appt.treatment && appt.treatment.prescription">
                     <small class="d-block text-muted fw-bold text-uppercase mt-2" style="font-size: 0.7rem;">Prescription</small>
                     <p class="mb-0 small text-primary">{{ appt.treatment.prescription }}</p>
                  </div>
                </div>
                <button v-if="appt.diagnosis" class="btn btn-link btn-sm p-0 mt-2 text-decoration-none" @click="viewDetails(appt)">
                  View Full Details
                </button>
              </div>
              <div v-if="history.length === 0" class="text-center py-4 text-muted">
                No appointment history.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="selectedAppt" class="modal-backdrop fade show"></div>
    <div v-if="selectedAppt" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Appointment Details</h5>
            <button type="button" class="btn-close btn-close-white" @click="selectedAppt = null"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-4">
              <h6 class="text-muted text-uppercase small fw-bold">Doctor</h6>
              <p class="fs-5 mb-0">Dr. {{ selectedAppt.doctor_name }}</p>
              <small class="text-muted">{{ selectedAppt.date }} | {{ selectedAppt.time }}</small>
            </div>
            <div class="mb-4 p-3 bg-light rounded border-start border-4 border-info">
              <h6 class="text-info text-uppercase small fw-bold mb-2">Diagnosis</h6>
              <p class="mb-0">{{ selectedAppt.diagnosis }}</p>
            </div>
            <div class="mb-4 p-3 bg-light rounded border-start border-4 border-success">
              <h6 class="text-success text-uppercase small fw-bold mb-2">Prescription</h6>
              <p class="mb-0" style="white-space: pre-line;">{{ selectedAppt.treatment?.prescription || 'No prescription recorded' }}</p>
            </div>
            <div v-if="selectedAppt.treatment?.notes" class="p-3 bg-light rounded border-start border-4 border-warning">
              <h6 class="text-warning text-uppercase small fw-bold mb-2">Doctor's Notes</h6>
              <p class="mb-0">{{ selectedAppt.treatment.notes }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import apiClient from '../services/api';

export default {
  setup() {
    const doctors = ref([]);
    const history = ref([]);
    const searchSpec = ref('');
    const bookingDate = ref('');
    const bookingTime = ref('');
    const selectedAppt = ref(null);

    const searchDoctors = async () => {
      if (searchSpec.value.length > 2) {
        const res = await apiClient.get(`/api/patient/doctors?specialization=${searchSpec.value}`);
        doctors.value = res.data;
      }
    };

    const fetchHistory = async () => {
      const res = await apiClient.get('/api/patient/appointments');
      history.value = res.data;
    };

    const bookAppointment = async (doctorId) => {
      try {
        await apiClient.post('/api/patient/appointments', {
          doctor_id: doctorId,
          date: bookingDate.value,
          time: bookingTime.value
        });
        alert('Appointment booked successfully!');
        bookingDate.value = '';
        bookingTime.value = '';
        fetchHistory();
      } catch (e) {
        alert('Booking failed: ' + (e.response?.data?.msg || e.message));
      }
    };

    const statusBadge = (status) => {
      if (status === 'Booked') return 'badge bg-primary-subtle text-primary-emphasis';
      if (status === 'Completed') return 'badge bg-success-subtle text-success-emphasis';
      return 'badge bg-secondary-subtle text-secondary-emphasis';
    };

    const viewDetails = async (appt) => {
        // In a real app, we might fetch details here. 
        // For now, we'll assume the list has enough or we mock it for the UI demo if missing.
        // Let's assume the backend sends 'diagnosis' string. 
        // We need to ensure the backend sends the full treatment object.
        // I will update the backend to send full treatment details.
        selectedAppt.value = appt;
    };

    onMounted(fetchHistory);

    return { doctors, history, searchSpec, bookingDate, bookingTime, searchDoctors, bookAppointment, statusBadge, selectedAppt, viewDetails };
  }
};
</script>

<style scoped>
.avatar-circle { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.doctor-card { transition: transform 0.2s; }
.doctor-card:hover { transform: translateY(-3px); border-color: var(--primary-color) !important; }
.fade-in { animation: fadeIn 0.5s ease-in; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
