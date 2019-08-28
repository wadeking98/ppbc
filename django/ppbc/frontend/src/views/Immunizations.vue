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
          <td class="raw_data">
            <b-button class="raw_buttn" @click="raw(immunization)" >Raw</b-button>
            <transition name=fade >
              <b-card class="raw_imm" v-if="raw_imm.includes(immunization.attrs.imm_id)">
                {{ JSON.stringify(immunization) }}
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
  name: "Immunizations",
  data: () => {
    return {
      immunizations: [],
      raw_imm: [],
      sort: "new-to-old",
    };
  },
  methods: {
    test(){
      alert('test')
    },
    getAllImmunizations() {
      this.$http
        .get("http://localhost:8000/api/credentials/")
        .then(
          response => {
            console.log("RESPONSE:", response.body.results)
            
            this.immunizations = response.body.results
            .filter(cred => cred.attrs.type == 'imm');

            this.sortImmunizations();
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
      if(this.raw_imm.includes(imm.attrs.imm_id)){
        this.raw_imm.pop(imm.attrs.imm_id)
      }else{
        this.raw_imm.push(imm.attrs.imm_id)
      }
      console.log(this.raw_imm)
    },
    
    
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
.raw_data{
  width:50vh;
}
.raw_imm{
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