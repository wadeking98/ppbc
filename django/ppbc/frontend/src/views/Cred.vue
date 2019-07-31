<template>
    <div>
        <b-form class="cred-form" v-on:submit.prevent="send_cred()">
            <b-form-select v-model="type" :options="options" class="cred-select"
            id="type-select"></b-form-select>
            
            <div v-if="type=='imm'" class="cred-imm-form">
                <b-form-input class="cred-imm-id" type="text" v-model="imm_id" placeholder="ID"></b-form-input>
                <b-form-input class="cred-imm-name" type="text" v-model="imm_name" placeholder="Immunization Name"></b-form-input>
                <b-form-input class="cred-imm-date" type="date" v-model="imm_date"></b-form-input>
            </div>

            <div v-else-if="type=='med'" class="cred-med-form">
                <b-form-input class="cred-med-name" type="text" v-model="med_name" placeholder="Medication Name"></b-form-input>
                <b-form-input class="cred-med-dos" type="text" v-model="med_dosage" placeholder="Dosage"></b-form-input>
                <b-form-input class="cred-med-pers" type="date" v-model="persc_date" placeholder="Perscription Date"></b-form-input>
                <b-form-input class="cred-med-exp" type="date" v-model="exp_date" placeholder="Expiry Date"></b-form-input>
                <b-form-input class="cred-med-renw" type="text" v-model="num_renewals" placeholder="# of Renewals"></b-form-input>
            </div>

            <div v-else-if="type=='lab'" class="cred-med-form">
                <b-form-input class="cred-lab-test" type="text" v-model="lab_test" placeholder="Lab Test"></b-form-input>
                <b-form-input class="cred-lab-res" type="text" v-model="lab_result" placeholder="Result"></b-form-input>
                <b-form-input class="cred-lab-date" type="date" v-model="lab_date" placeholder="Inspection Date"></b-form-input>
            </div>

            <b-button v-if="type!=''" variant="primary" type="submit">Submit</b-button>
        </b-form>

    </div>
</template>
<script>
import axios from 'axios';
export default {
    name:'credentials',
    data(){
        return{
            id:0,
            type:"",
            imm_id:"",
            imm_name:"",
            imm_date:"",
            med_name:"",
            med_dosage:"",
            persc_date:"",
            exp_date:"",
            num_renewals:"",
            lab_test:"",
            lab_result:"",
            lab_date:"",
            options:[
                {value: null, text: '--Please Select a Credential Type--', disabled:true},
                {value: "imm", text: "Immunization"},
                {value: "med", text: "Medication"},
                {value: "lab", text: "Lab Results"}
            ]
        }
    },
    created(){
        this.id = this.$route.params.conn_id
        axios.post('http://localhost:8000/api/register_seed/')
    },
    methods:{
        to_query(data){
            var queryString = Object.keys(data).map(function(key) {
                return key + '=' + data[key]
            }).join('&');
            return queryString
        },
        send_cred(){
            var vm = this
            var post_data
            if(vm.type == "med"){
                post_data={
                    "type":vm.type,
                    "med_name":vm.med_name,
                    "med_dosage":vm.med_dosage,
                    "persc_date":vm.persc_date,
                    "exp_date":vm.exp_date,
                    "num_renewals":vm.num_renewals
                }
            }else if(vm.type=="imm"){
                post_data={
                    "type":vm.type,
                    "imm_id":vm.imm_id,
                    "imm_name":vm.imm_name,
                    "imm_date":vm.imm_date
                }
            }
            else if(vm.type=="lab"){
                post_data={
                    "type":vm.type,
                    "lab_test":vm.lab_test,
                    "lab_result":vm.lab_result,
                    "lab_date":vm.lab_date
                }
            }
            console.log(this.to_query(post_data))
            axios.post("http://localhost:8000/api/issue_cred/",this.to_query(post_data))
        }
    }
}
</script>
<style>

.cred-form *{
    display: block;
}
.cred-form *:not(div){
    margin:5vh;
    width:60vh;
}
</style>



