<template>
    <div class = "container">
        <h2>Sign Up</h2>
        <b-button v-on:click="User_variant='primary'; Org_variant='secondary'" v-bind:variant="User_variant">User</b-button>
        <b-button v-on:click="User_variant='secondary'; Org_variant='primary'" v-bind:variant="Org_variant">Organization</b-button>

        <b-form v-on:submit.prevent="submit()">
            <b-form-group id="signup-optional" label="">
                <b-form-input 
                    id="signup-fname"
                    v-model="first_name"
                    placeholder="First Name"
                ></b-form-input> 

                <b-form-input 
                    id="signup-lname"
                    v-model="last_name"
                    placeholder="Last Name"
                ></b-form-input>
            </b-form-group>

            <b-form-group id="signup-required">
                <b-form-input 
                    id="signup-email"
                    v-model="email"
                    placeholder="Email*"
                    required
                ></b-form-input>
                <!-- error message -->
                <p class="error" v-if="!loading && !emailIsValid(email) && error">Invalid Email!</p>

                <b-form-input 
                    id="signup-password1"
                    v-model="password1"
                    placeholder="Password*"
                    required
                    type="password"
                ></b-form-input>
                <!-- error message -->

                <b-form-input 
                    id="signup-password2"
                    v-model="password2"
                    placeholder="Confirm Password*"
                    required
                    type="password"
                ></b-form-input>

                <p class="error" v-if="!loading && ((password1 !== password2)) && error">Passwords Do Not Match!</p>
                <p class="error" v-else-if="(password1.length == 0) && error">Password Field Required!</p>
            </b-form-group>

            <b-form-group v-if="Org_variant==='primary'" id='org-section'>
                <b-form-input 
                    id="signup-org-name"
                    v-model="org_name"
                    placeholder="Organization Name"
                    required
                ></b-form-input>

                <b-form-input 
                    id="signup-org-role"
                    v-model="org_role_name"
                    placeholder="Organization Role"
                    required
                ></b-form-input>
            </b-form-group>

            <p class="error" v-if="((this.org_name.length==0)||(this.org_role_name.length==0))&&error&&Org_variant=='primary'">Organization Information Required</p>

            <b-form-group id='submision'>
                <!-- submit button and loading icon -->
                <b-button v-if="!loading && !formReady()" v-on:click="earlySubmit()" variant="secondary">Submit</b-button>
                <b-button v-else-if="!loading" type="submit" variant="primary">Submit</b-button>
                <b-spinner v-if="loading"></b-spinner>

            </b-form-group>
        </b-form>        
    </div>
</template>

<script>
import axios from 'axios'
import Vue from 'vue'
import { setTimeout } from 'timers';
export default {
    
    data: ()=>{
        return{
            Org_variant: 'secondary',
            User_variant: 'primary',
            error: false,
            //laoding status
            loading: false,
            //form data
            first_name:'',
            last_name:'',
            email:'',
            password1:'',
            password2:'',
            org_name:'',
            org_role_name:'',
            ico_url:'',
        }
    },
    
    methods: {
        redirect(path) {
            this.$router.push('/' + path);
        },
        submit(){
            var vm = this;
            //start the loading icon after submit is clicked
            vm.loading = true;
            var userDataStr = 'first_name='+vm.first_name+'&last_name='+vm.last_name+'&email='+vm.email+'&password1='+vm.password1+'&password2='+vm.password2;
            var orgDataStr = userDataStr+'&org_name='+vm.org_name+'&org_role_name='+vm.org_role_name+'&ico_url='+vm.ico_url;

            var userUrl = 'http://localhost:8000/api/signup/';
            var orgUrl = 'http://localhost:8000/api/org_signup/'

            //ternerary operators to assign the right type of url and data string
            var url = vm.Org_variant === 'primary' ? orgUrl : userUrl;
            var data = vm.Org_variant === 'primary' ? orgDataStr : userDataStr;
            
            //set the csrf tokens so django doesn't get fussy
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            
            axios.post(url, data)
                .then(function (response) {
                    //stop loading icon and redirect to home
                    vm.loading = false;
                    vm.redirect('signin');
                })
                .catch(function (error) {
                    //currentObj.output = error;
                });
            
        },
        formReady(){
            if(this.Org_variant==='primary'){
                 return (this.password1 === this.password2) && (this.password1.length > 0) && this.emailIsValid(this.email) && (this.org_name.length>0)&&(this.org_role_name.length>0)
            }
            return (this.password1 === this.password2) && (this.password1.length > 0) && this.emailIsValid(this.email)
        },
        earlySubmit(){
            this.error = true;
            console.log(!this.loading && ((this.password1 !== this.password2) || (this.password1.length == 0)) && this.emailIsValid(this.email));
        },
        emailIsValid(email){
            var emailRx = /.+@.+\..+/g;
            
            return email.match(emailRx) != null;
        },
    }
}


</script>

<style>
.error{
    color: orange;
}

</style>
