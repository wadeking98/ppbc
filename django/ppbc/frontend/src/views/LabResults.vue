<template>
  <div class="container">
    <br>

    <h1><font-awesome-icon icon="flask"></font-awesome-icon> Lab Results</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Test</th>
          <th>Results</th>
          <th>
            Date of Inspection
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="labResult in labResults" :key="labResult.id" class="accordion-toggle">
          <td>{{ labResult.attrs.lab_test }}</td>
          <td>{{ labResult.attrs.lab_result }}</td>
          <td>{{ labResult.attrs.lab_date }}</td>
          <td class="raw_data">
            <b-button class="raw_buttn" @click="raw(labResult)">Raw</b-button>
            <transition name=fade >
              <b-card class="raw_lab" v-if="raw_lab.includes(labResult.attrs.lab_test)">
                {{ JSON.stringify(labResult) }}
              </b-card>
            </transition>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "LabResults",
  data: () => {
    return {
      labResults: [],
      raw_lab:[],
      isDetailsShowing: false
    };
  },
  components: {},
  methods: {
    getAllLabResults() {
      this.$http
        .get("http://localhost:8000/api/credentials/")
        .then(response => {
          console.log(response);
          this.labResults = response.body.results
          .filter(lab => lab.attrs.type == "lab");
        });
    },
    raw(lab){
      if(this.raw_lab.includes(lab.attrs.lab_test)){
        this.raw_lab.pop(lab.attrs.lab_test)
      }else{
        this.raw_lab.push(lab.attrs.lab_test)
      }
    }

  },
  beforeMount() {
    this.getAllLabResults();
  }
};
</script>

<style scoped>
.container {
  text-align: left;
}
.details {
  margin-left: 15px;
}
.check-icon {
  color: green
}
.raw_data{
  width:50vh;
}
.raw_lab{
  margin-top: 2vh;
  width: 50vh;
}.raw_buttn{
  position: relative;
  left:45%;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity:0;
}
</style>