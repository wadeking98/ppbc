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
          <th>
            <button class="btn btn-primary" @click="getAllLabResults()">
              <font-awesome-icon icon="sync-alt"/>
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="labResult in labResults" :key="labResult.id" class="accordion-toggle">
          <td>{{ labResult.attrs.lab_test }}</td>
          <td>{{ labResult.attrs.lab_result }}</td>
          <td>{{ labResult.attrs.lab_date }}</td>
          <td>
            <button
              class="btn btn-light btn-sm"
              @click="toggleDetails()"
            >DETAILS</button>
          </td>
        </tr>
        <!-- <tr class="details" v-if="this.isDetailsShowing == true">
          <td>
            <p>Observation: {{labResults[0].resource.component[0].code.text}}</p>
            <p>Observation: {{labResults[0].resource.component[1].code.text}}</p>
            <p>Observation: {{labResults[0].resource.component[2].code.text}}</p>
            <p>Observation: {{labResults[0].resource.component[3].code.text}}</p>
            <p>Observation: {{labResults[0].resource.component[4].code.text}}</p>
            <p>Observation: {{labResults[0].resource.component[5].code.text}}</p>
            <p>Observation: {{labResults[0].resource.component[6].code.text}}</p>
          </td>
          <td>
            <p>Result: {{labResults[0].resource.component[0].valueQuantity.value}} {{labResults[0].resource.component[0].valueQuantity.unit}}</p>
            <p>Result: {{labResults[0].resource.component[1].valueQuantity.value}} {{labResults[0].resource.component[1].valueQuantity.unit}}</p>
            <p>Result: {{labResults[0].resource.component[2].valueQuantity.value}} {{labResults[0].resource.component[2].valueQuantity.unit}}</p>
            <p>Result: {{labResults[0].resource.component[3].valueQuantity.value}} {{labResults[0].resource.component[3].valueQuantity.unit}}</p>
            <p>Result: {{labResults[0].resource.component[4].valueQuantity.value}} {{labResults[0].resource.component[4].valueQuantity.unit}}</p>
            <p>Result: {{labResults[0].resource.component[5].valueQuantity.value}} {{labResults[0].resource.component[5].valueQuantity.unit}}</p>
            <p>Result: {{labResults[0].resource.component[6].valueQuantity.value}} {{labResults[0].resource.component[6].valueQuantity.unit}}</p>
          </td>
          <td>
            <p>Pass/Fail: <font-awesome-icon class="check-icon" icon="check"></font-awesome-icon></p>
            <p>Pass/Fail: <font-awesome-icon class="check-icon" icon="check"></font-awesome-icon></p>
            <p>Pass/Fail: <font-awesome-icon class="check-icon" icon="check"></font-awesome-icon></p>
            <p>Pass/Fail: <font-awesome-icon class="check-icon" icon="check"></font-awesome-icon></p>
            <p>Pass/Fail: <font-awesome-icon class="check-icon" icon="check"></font-awesome-icon></p>
            <p>Pass/Fail: <font-awesome-icon class="check-icon" icon="check"></font-awesome-icon></p>
            <p>Pass/Fail: <font-awesome-icon class="check-icon" icon="check"></font-awesome-icon></p>
          </td>
          <td></td>
        </tr> -->
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
    toggleDetails() {
      if (!this.isDetailsShowing) {
        this.isDetailsShowing = true;
      } else {
        this.isDetailsShowing = false;
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
</style>