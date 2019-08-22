<template>
  <div class="container">
    <br>
    <h1><font-awesome-icon icon="syringe"></font-awesome-icon> Immunizations</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Immunization ID</th>
          <th>Immunization Name</th>
          <th>
            <button class="btn btn-light" @click="sortImmunizations()">
              <font-awesome-icon icon="arrows-alt-v"/>
            </button>
            Most Recent Administration (YYYY-MM-DD)
          </th>
          
        </tr>
      </thead>
      <tbody>
        <tr v-for="immunization in immunizations" :key="immunization.attrs.imm_id">
          <td>{{ immunization.attrs.imm_id }}</td>
          <td>{{ immunization.attrs.imm_name }}</td>
          <td>{{ immunization.attrs.imm_date }}</td>
          <td>
            <b-button :pressed="false" @click="raw(immunization)" >Raw</b-button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
// @ is an alias to /src
export default {
  name: "Immunizations",
  data: () => {
    return {
      immunizations: [],
      sort: "new-to-old",
    };
  },
  methods: {
    getAllImmunizations() {
      this.$http
        .get("http://localhost:8000/api/credentials/")
        .then(
          response => {
            console.log("RESPONSE:", response.body.results)
            
            this.immunizations = response.body.results
            .filter(cred => cred.attrs.type == 'imm');

            this.sortImmunizations();
          },
          response => {
            console.error(response);
          }
        );
    },
    sortImmunizations() {
      let val1, val2;
      if (this.sort === "new-to-old") {
        val1 = 1;
        val2 = -1;
        this.sort = "old-to-new";
      } else {
        val1 = -1;
        val2 = 1;
        this.sort = "new-to-old";
      }
      this.immunizations = this.immunizations.sort((a, b) => {
        return val1 ? a.imm_date < b.imm_date : val2
      });
    },

    raw(imm){
      alert(JSON.stringify(imm))
    }
    
  },
  beforeMount() {
    this.getAllImmunizations();
  }
};
</script>

<style scoped>
.container {
  text-align: left;
}
</style>