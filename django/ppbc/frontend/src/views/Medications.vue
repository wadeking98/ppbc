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
          <!-- <th>
            <button class="btn btn-primary" v-on:click="getAllMedications()">
              <font-awesome-icon icon="sync-alt"/>
            </button>
          </th> -->
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
          <td class="raw_data">
            <b-button class="raw_buttn" @click="raw(medication)">RAW</b-button>
            <transition name=fade >
              <b-card class="raw_med" v-if="raw_med.includes(medication.attrs.med_name)">
                {{ JSON.stringify(medication) }}
              </b-card>
            </transition>
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
      raw_med:[],
      medications: []
    };
  },
  components: {
    "medicaiton-modal": MedicationModal
  },
  methods: {
    raw(med){
      if(this.raw_med.includes(med.attrs.med_name)){
        this.raw_med.pop(med.attrs.med_name)
      }else{
        this.raw_med.push(med.attrs.med_name)
      }
      console.log(this.raw_med)
    },
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
.raw_med{
  margin-top: 2vh;
  width: 50vh;
}.raw_buttn{
  position: relative;
  left:45%;
}
.raw_data{
  width:50vh;
}
.container {
  text-align: left;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity:0;
}
</style>
