<template>
  <div class="fade-in">
    <h2 class="mb-4 fw-bold text-primary">Doctor's Console</h2>
    
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
        <h5 class="mb-0 fw-bold">Today's Appointments</h5>
        <span class="badge bg-primary-subtle text-primary-emphasis">{{ appointments.length }} Scheduled</span>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light">
              <tr>
                <th class="ps-4">Time</th>
                <th>Patient</th>
                <th>Status</th>
                <th class="text-end pe-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appt in appointments" :key="appt.id">
                <td class="ps-4 fw-bold text-muted">{{ appt.time }}</td>
                <td>
                  <div class="d-flex align-items-center">
                    <div class="avatar-circle bg-info-subtle text-info-emphasis me-3">
                      {{ appt.patient_name.charAt(0).toUpperCase() }}
                    </div>
                    <span class="fw-bold">{{ appt.patient_name }}</span>
                  </div>
                </td>
                <td><span :class="statusBadge(appt.status)">{{ appt.status }}</span></td>
                <td class="text-end pe-4">
                  <button v-if="appt.status === 'Booked'" @click="openCompleteModal(appt)" class="btn btn-primary btn-sm rounded-pill px-3">
                    Consult
                  </button>
                  <button v-else class="btn btn-outline-secondary btn-sm rounded-pill px-3" disabled>
                    Viewed
                  </button>
                </td>
              </tr>
              <tr v-if="appointments.length === 0">
                <td colspan="4" class="text-center py-5 text-muted">
                  No appointments scheduled.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Complete Modal -->
    <div v-if="selectedAppt" class="modal-backdrop fade show"></div>
    <div v-if="selectedAppt" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Consultation: {{ selectedAppt.patient_name }}</h5>
            <button type="button" class="btn-close btn-close-white" @click="selectedAppt = null"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-3">
              <label class="form-label fw-bold text-uppercase small text-muted">Diagnosis</label>
              <textarea v-model="diagnosis" class="form-control" rows="3" placeholder="Enter diagnosis details..."></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold text-uppercase small text-muted">Prescription</label>
              <textarea v-model="prescription" class="form-control" rows="4" placeholder="Enter medications and dosage..."></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold text-uppercase small text-muted">Private Notes</label>
              <textarea v-model="notes" class="form-control" rows="2" placeholder="Internal notes..."></textarea>
            </div>
          </div>
          <div class="modal-footer bg-light">
            <button @click="selectedAppt = null" class="btn btn-link text-muted text-decoration-none">Cancel</button>
            <button @click="completeAppointment" class="btn btn-primary px-4">Complete Consultation</button>
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
    const appointments = ref([]);
    const selectedAppt = ref(null);
    const diagnosis = ref('');
    const prescription = ref('');
    const notes = ref('');

    const fetchAppointments = async () => {
      const res = await apiClient.get('/api/doctor/appointments');
      appointments.value = res.data;
    };

    const statusBadge = (status) => {
      if (status === 'Booked') return 'badge bg-primary-subtle text-primary-emphasis';
      if (status === 'Completed') return 'badge bg-success-subtle text-success-emphasis';
      return 'badge bg-secondary-subtle text-secondary-emphasis';
    };

    const openCompleteModal = (appt) => {
      selectedAppt.value = appt;
      diagnosis.value = '';
      prescription.value = '';
      notes.value = '';
    };

    const completeAppointment = async () => {
      await apiClient.post(`/api/doctor/appointments/${selectedAppt.value.id}/complete`, {
        diagnosis: diagnosis.value,
        prescription: prescription.value,
        notes: notes.value
      });
      selectedAppt.value = null;
      fetchAppointments();
    };

    onMounted(fetchAppointments);

    return { appointments, selectedAppt, diagnosis, prescription, notes, statusBadge, openCompleteModal, completeAppointment };
  }
};
</script>

<style scoped>
.avatar-circle { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.8rem; }
.fade-in { animation: fadeIn 0.5s ease-in; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
