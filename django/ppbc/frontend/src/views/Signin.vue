<template>
    <div class = "container">
        <h2>Sign In</h2>
        <b-form v-on:submit.prevent="submit()">
            <b-form-group id="signin" label="">
                <!-- dynamic error message -->
                <p class="loginErr" v-if="logErr">Incorrect Username or Password</p>
                <b-form-input 
                    id="signin-email"
                    v-model="username"
                    placeholder="Email"
                    required
                ></b-form-input>

                <b-form-input 
                    id="signin-password"
                    v-model="password"
                    placeholder="Password"
                    required
                    type="password"
                ></b-form-input>

                

            </b-form-group>

            <b-button v-if="!loading" type="submit" variant="primary">Submit</b-button>
            <b-spinner v-if="loading"></b-spinner>
        </b-form>
        
    </div>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
export default {
    
    data: ()=>{
        return{
            loading: false,
            logErr: false,
            username:'',
            password:'',
            next: '%2Findy%2Fprofile%2F'
        }
    },
    created: function(){
        
    },
    methods: {
        submit(){
            var vm = this;
            vm.loading = true;
            var dataStr = 'username='+vm.username+'&password='+vm.password

            //set the csrf tokens so django doesn't get fussy when we post
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

            axios.post('http://localhost:8000/api/signin/', dataStr)
                .then(function (response) {
                    vm.loading = false;
                    //determine if indy accepts the login request
                    
                    var res = response.data
                    console.log(response.data)

                    
                    if(!res.login){
                        vm.logErr = true;
                    }else{
                        vm.redirect('home');
                    }
                    
                    
                })
                .catch(function (error) {
                    //currentObj.output = error;
                });
        },
        redirect(path) {
            this.$router.push('/' + path);
        }
    }
}
</script>
<style>
.loginErr{
    color: orange;
}
</style>


