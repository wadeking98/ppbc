<template>
    <div class ="container">
        <h2>Select a Connection Partner</h2>
        <b-form id="connection" v-on:submit.prevent="sendConn()">
            <!-- <b-form-input 
                id="connection_request"
                v-model="partner"
                placeholder="Partner Email or Organization Name"
            ></b-form-input> -->
            <b-form-select v-model="partner">
                <option :value="null" disabled selected="selected">--Please Select a Partner--</option>
                
                <optgroup label="Organizations">
                    <option :value="org" v-for="org in orgs" v-bind:key="org">{{ org }}</option>
                </optgroup>
                <optgroup label="Users">
                    <option :value="usr" v-for="usr in users" v-bind:key="usr">{{ usr }}</option>
                </optgroup>

            </b-form-select>
            <b-button v-if="!loading" type="submit" variant="primary">Submit</b-button>
            <b-spinner v-else></b-spinner>
            <b-button variant="primary" @click="loadConn()">Refresh</b-button>
        </b-form>

        <connection 
        v-for="conn in conenctions" 
        v-bind:wallet="conn.wallet" 
        v-bind:partner="conn.partner_name"
        v-bind:status="conn.status" 
        v-bind:type="conn.type"
        v-bind:key="conn.wallet"
        ></connection>
      
        
    </div>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
import connection from './components/connection'
export default {
    components:{
        connection
    },
    data() {
        return {
            loading: false,
            partner: '',
            conenctions: [],
            users: [],
            orgs: []
        }
    },
    methods:{
        
        loadConn(){
            var vm = this;
            axios.get('http://localhost:8000/api/list_conn/')
            .then(function(response){
                vm.conenctions = response.data.results;
                console.log(vm.conenctions);
            })
        },

        loadOrgs(){
            var vm = this;
            axios.get('http://localhost:8000/api/list_org/')
            .then(function(response){
                vm.orgs = response.data;
            })
        },

        loadUsrs(){
            var vm = this;
            axios.get('http://localhost:8000/api/list_usr/')
            .then(function(response){
                vm.users = response.data;
            })
        },
        
        sendConn(){
            var vm = this;
            vm.loading = true;

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.get('http://localhost:8000/api/wallet')
            .then(function(res){
                var testStr = 'wallet_name='+res.data.wallet+'&partner_name='+vm.partner
                axios.post('http://localhost:8000/api/conn/', testStr)
                .then(function(res){
                    console.log(res.data);
                    vm.loading = false;
                    vm.loadConn()
                })
                .catch(function(err){

                });
            })
            
        },

        
    },
    created() {
        this.loadConn();
        this.loadOrgs();
        this.loadUsrs();
    },
    
}
</script>

<style>
.pfReq{
    text-decoration: none;
    color: white;
    display: inline-block;
    margin-right: 2vh;
}
.pfReq:hover{
    color:lightgray;
}
#req{
    display: inline-block;
}
</style>

