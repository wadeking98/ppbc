<template>
  <div class="container">
    <br>
    <h1><font-awesome-icon icon="prescription-bottle-alt"></font-awesome-icon> Medications</h1>
    <table class="table" v-if="hasMedications">
      <thead>
        <tr>
          <!-- <th>Medication ID</th> -->
          <th>Medication Name</th>
          <th>Dosage</th>
          <th>Perscription Date</th>
          <th>Expiry Date</th>
          <th># of Renewals Left</th>
          <th>
            <button class="btn btn-primary" v-on:click="getAllMedications()">
              <font-awesome-icon icon="sync-alt"/>
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="medication in medications" :key="medication.med_name">
          <!-- <td>{{ medication.resource.id }}</td> -->
          <td>{{ medication.attrs.med_name }}</td>
          <td>{{ medication.attrs.med_dosage }}</td>
          <td>{{ medication.attrs.persc_date }}</td>
          <td>{{ medication.attrs.exp_date }}</td>
          <td>{{ medication.attrs.num_renewals }}</td>
          <td>
            <b-btn @click="openModal(medication)" class="btn btn-light btn-sm">DETAILS</b-btn>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <h1>Looks like you don't have any medications perscribed. Would you like to request one?</h1>
    </div>
    <div>
      <medicaiton-modal></medicaiton-modal>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import MedicationModal from "./components/MedicationModal.vue";
export default {
  name: "Medications",
  data: () => {
    return {
      hasMedications: true,
      medications: []
    };
  },
  components: {
    "medicaiton-modal": MedicationModal
  },
  methods: {
    getAllMedications() {
      this.$http
        .get(
          "http://localhost:8000/api/credentials/"
        )
        .then(
          response => {
            console.log(response.body.results)
            this.medications = response.body.results
            .filter(med => med.attrs.type == "med");
            if (this.medications.length > 0) {
              this.hasMedications = true;
            }
          }
        );
    },
    // eslint-disable-next-line
    openModal(medicationRow) {
      //console.log(medicationRow)
    }
  },

  beforeMount() {
    this.getAllMedications();
  }
};
</script>

<style scoped>
.container {
  text-align: left;
}
</style>
