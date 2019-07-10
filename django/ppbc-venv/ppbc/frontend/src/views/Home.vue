<template>
  <div class="container">
    <br>
    <b-jumbotron text-variant="white" :fluid="true">
      <template slot="header">Health Gateway</template>
      <template slot="lead">
        Safely and securely view your current medications, immunizations and lab results. 
      </template>
    </b-jumbotron>
    <div class="page-body">
      <b-row>
        <b-col>
          <b-card class="clickable-card" bg-variant="info" text-variant="white" @click="redirect('medications')"> 
            <h4 class="card-top">
              <font-awesome-icon icon="prescription-bottle-alt"></font-awesome-icon> Medications
            </h4>
            <p class="card-text">
              View your current medication perscriptions.
            </p>
          </b-card>
        </b-col>
        <b-col>
          <b-card class="clickable-card" bg-variant="primary" text-variant="white" @click="redirect('immunizations')">
            <h4 class="card-top">
              <font-awesome-icon icon="syringe"></font-awesome-icon> Immunizations
            </h4>
            <p class="card-text">
              View all your past Immunizations.
            </p>
          </b-card>
        </b-col>
        <b-col>
          <b-card class="clickable-card" bg-variant="secondary" text-variant="white" @click="redirect('lab-results')">
            <h4 class="card-top">
              <font-awesome-icon icon="flask"></font-awesome-icon> Lab Results
            </h4>
            <p class="card-text">
              View your lab results and observations.
            </p>
          </b-card>
        </b-col>
      </b-row>
    </div>
    <div id = "requests" >
      <b-dropdown class="clickable-card rqs" style="width:100%;" variant="primary" >
        <template slot="button-content">
          Requests ({{rqs.length}})
        </template>
        <b-dropdown-item v-for="rq in rqs" :key="rq.text">
          {{ rq.text }}
        </b-dropdown-item>

      </b-dropdown>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
export default {
  name: "Home",
  components: {},
  data: () => {
    return {
      rqs:[
        {text:"hello"},
        {text:"world"},
        {text:"test"}
      ]
    };
  },
  methods: {
    redirect(path) {
      this.$router.push('/' + path);
    },
    newReq(req){
      this.rqs.push({text:req});
    }
  }
};
</script>
<style scoped>
  #requests{
    display:block;
    margin-top: 2vh;
  }
  .clickable-card:hover {
    cursor: pointer;
  }
  .jumbotron {
    background-image: url("../assets/cover.jpeg");
    background-size: cover;
  }
</style>

