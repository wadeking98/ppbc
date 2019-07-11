<template>
  <div class="container">
    <br>
    <h1>Profile</h1>
    <br>
    <b-row>
      <b-col>
        <img src="./../assets/woman.png" width="200" height="200" border="1"/>
      </b-col>
      <b-col cols="9">
        <h2>Alice Jacobs</h2>
        <h4>1234 Vancouver Street</h4>
        <h4>PHN: 9*****6204</h4> 
        <h4>DOB: 1981 FEB 19</h4>
      </b-col>
    </b-row>
    <p>If this profile information is incorrect, go <a href="#">here</a></p>
    <h1>Connections</h1>
    <p>Enjoy all the benefits and value that third-party health apps provide by
      connecting them to your health data</p>
    <h4>You have 3 connected apps</h4>
    <b-row>
      <b-col cols="5">
        <p>&nbsp;</p>
        <img src="https://images.ctfassets.net/1izjqx4qtt8c/1NogrRoCWomi6Ksecqm6KS/0a863bb2d152c76713626ec4fc1ee9d9/THB_logo_hor_pur_RGB.png" height="30"/>
       <h6>Connected with Babylon to share all your health data</h6>
       <b><a href="#">[Disconnect Babylon]</a></b>
       </b-col>
    </b-row>
    <b-row>
      <b-col cols="5">
        <p>&nbsp;</p>
        <img src="https://support.apple.com/library/content/dam/edam/applecare/images/en_US/ios/built_in/ios9-health-app-icon.png" height="40"/>
       <h6>Connected with Apple Health to share all your health data to view progress</h6>
       <b><a href="#">[Disconnect Apple Health]</a></b>
       </b-col>
    </b-row>
    <b-row>
      <b-col cols="5">
        <p>&nbsp;</p>
        <img src="https://careteam.tech/wp-content/uploads/2018/04/ctm_logo.png" height="30"/>
       <h6>Connected with Care Team to share all your health data to provide complex care insights</h6>
       <b><a href="#">[Disconnect Care Team]</a></b>
       </b-col>
    </b-row>
    <p>&nbsp;</p>
    <h1>Delegation</h1>
    <p>Allow others to view your health data by granting.</p>
    <b>You have not delegated access to anyone</b>
  </div>
</template>
<script>
// @ is an alias to /src

export default {
  name: "Profile",
  data: () => {
    return {
      currentPatient: {},
      images: {
        profile: require('./../assets/profile.jpg')
      }
    };
  },
  methods: {
    getCurrentUserInfo() {
      this.$http
        .get("http://hapi.fhir.org/baseDstu3/Patient/422566?_format=json")
        .then(response => {
          this.currentPatient = response.body;
        });
    }
  },
  beforeMount() {
    this.getCurrentUserInfo();
  }
};
</script>
<style scoped>
.container {
  text-align: left;
}
</style>
