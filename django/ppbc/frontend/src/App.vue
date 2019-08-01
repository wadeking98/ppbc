<template>
  <div id="app">
    <fancy-line x='0' y='0' theta='30' r='70' dir=0.1 lim1=20 lim2=45></fancy-line>
    <fancy-line x='40' y='0' theta='120' r='55' dir=-0.15 lim1=80 lim2=150></fancy-line>
    <fancy-line x='60' y='55' theta='230' r='65' dir=-0.15 lim1=200 lim2=260></fancy-line>
    <fancy-line x='30' y='55' theta='300' r='30' dir=0.1 lim1=270 lim2=330></fancy-line>
    <fancy-line x='75' y='0' theta='120' r='50' dir=-0.1 lim1=110 lim2=160></fancy-line>
    <fancy-line x=90 y=55 theta=245 r=40 dir=-0.1 lim1=220 lim2=280></fancy-line>
    <fancy-line x='100' y='0' theta='30' r='30' dir=-0.1 lim1=20 lim2=45></fancy-line>
    <fancy-line x='140' y='0' theta='120' r='55' dir=0.15 lim1=80 lim2=150></fancy-line>
    <fancy-line x='160' y='55' theta='230' r='45' dir=0.15 lim1=200 lim2=260></fancy-line>
    <fancy-line x='130' y='55' theta='300' r='15' dir=-0.1 lim1=270 lim2=330></fancy-line>
    <fancy-line x='175' y='0' theta='120' r='50' dir=0.1 lim1=110 lim2=160></fancy-line>
    <fancy-line x=190 y=55 theta=245 r=45 dir=0.1 lim1=220 lim2=280></fancy-line>
 
   
    
    <div id="nav">
      <b-navbar toggleable="md" type="dark" variant="dark" v-if="(this.$router.currentRoute.name != 'login')
      &&(this.$router.currentRoute.name != 'signin')">
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand>
          <router-link to="/home">Health Gateway</router-link>
        </b-navbar-brand>
        <b-collapse is-nav id="nav_collapse">
          <b-navbar-nav class="ml-auto">
            <b-nav-item>
              <router-link to="/medications">Medications</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/immunizations">Immunizations</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/lab-results">Lab Results</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/profile">Profile</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/connections">Connections</router-link>
            </b-nav-item>
            <b-nav-item>
              <div v-on:click="logout()" >Logout</div>
            </b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
      <b-navbar v-else toggleable="md" type="dark" variant="dark">
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand>
          <router-link to="/home">Health Gateway</router-link>
        </b-navbar-brand>
      </b-navbar>
    </div>

    <router-view/>
  </div>
</template>
<script>
import fancyLine from './views/components/fancy-line'
import axios from 'axios'
export default {
  components:{
    fancyLine
  },
  data() {
    return {
      x:0,
      y:0,
      deg:45,
      r:200,
    }
  },
  methods:{
    redirect(path) {
        this.$router.push('/' + path);
    },
    logout(){
      var vm = this;
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      axios.get('http://localhost:8000/api/logout/')
        .then(function(){
          vm.redirect('');
      })
        .catch(function(){

        });
    },
  },
  mounted() {
    
  },
}

</script>


<style>
/* Global styles go here */
#app {
  font-family: "Arial";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}

#nav a {
  color: #ffffff;
}

#nav a.router-link-exact-active {
  color: #ffffff;
}
</style>
