<template>
    <div >
        <ul>
            <li v-for="req in requests" :key="req.presentation_exchange_id">
                <b-card class="req" bg-variant="info" text-variant="white">
                    <h5>Name: {{ req.presentation_request.name }}</h5>
                    <h6>Status: {{ req.state }}</h6>
                    <h6>Attributes:</h6>
                    <p v-for="(val,key) in req.presentation_request.requested_attributes"
                    class="attr" 
                    :key="key">{{ alias[val.name] }}</p>
                </b-card>
            </li>
        </ul>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data(){
        return{
            requests:[],
            id:0,
            alias:{
                "imm_id":"ID",
                "imm_name":"Immunization Name",
                "imm_date":"Immunization Date",
                "med_name":"Medication Name",
                "med_dosage":"Dosage",
                "persc_date":"Perscription Date",
                "exp_date":"Expiry Date",
                "num_renewals":"# of Renewals",
                "lab_test":"Lab Name",
                "lab_result":"Lab Result",
                "lab_date":"Lab Date"
            }
        }
    },
    methods:{
        get_req(){
            alert("got here")
            axios.get("http://localhost:8000/api/get_req").then((response)=>{
                this.requests = response.data.results.filter(req=>req.connection_id==this.id)
                console.log(response)
                console.log(vm.requests[0].presentation_exchange_id)
            })
        }
    },
    created(){
        this.id = this.$route.params.conn_id
        axios.get("http://localhost:8000/api/get_req").then((response)=>{
            this.requests = response.data.results
            console.log(this.requests)
        })
    }
    
}
</script>
<style>
.req{
    width:100vh;
    margin-top:3vh;
}
li{
    list-style: none;
}
.attr{
    margin-left:2vh;
}
</style>


