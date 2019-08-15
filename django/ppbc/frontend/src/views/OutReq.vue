<template>
    <div>
        <b-form id="request-form" v-on:submit.prevent="send_req()">
            <b-form-group label="Credential Request Title" label-for="cred-req-title">
                <b-form-input type="text" v-model="attributes['title']" id="cred-req-title"></b-form-input>
            </b-form-group>
            <b-form-group label="Credential Request Type" label-for="type-select" class="cred-select">
                <b-form-select v-model="type" :options="options" 
                    id="type-select"></b-form-select>
            </b-form-group>

            <b-form-group label="Request Attributes" v-if="type!=''" label-for="request-attributes">
                <div id="request-attributes">
                    <b-form-group v-for="(val,key) in attributes[type]" :key=key>
                        <b-form-checkbox v-model="attributes[type][key]" 
                        :value="true" :unchecked-value="false"> {{ alias[key] }}
                        </b-form-checkbox>
                    </b-form-group>
                </div>
            </b-form-group>

            <b-button v-if="type!='' && !loading" variant=primary type=submit>Send Request</b-button>
            <b-spinner class="spin" v-else-if="loading"></b-spinner>
        </b-form>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data(){
        return{
            id:0,
            type:"",
            imm_date:"",
            med_name:"",
            loading:false,


            options:[
                {value: null, text: '--Please Select a Credential Type--', disabled:true},
                {value: "imm", text: "Immunization"},
                {value: "med", text: "Medication"},
                {value: "lab", text: "Lab Results"}
            ],
            attributes:{
                "imm":{
                    "imm_id":false, 
                    "imm_name":false, 
                    "imm_date":false
                },
                "med":{
                    "med_name":false,
                    "med_dosage":false,
                    "persc_date":false,
                    "exp_date":false,
                    "num_renewals":false
                },
                "lab":{
                    "lab_test":false,
                    "lab_result":false,
                    "lab_date":false
                },
                "title":""
            },
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
    created(){
        this.id = this.id = this.$route.params.conn_id
        axios.post('http://localhost:8000/api/register_seed/')
    },
    methods:{
        to_query(data){
            var queryString = Object.keys(data).map(function(key) {
                return key + '=' + data[key]
            }).join('&');
            return queryString
        },
        send_req(){
            //shallow copy the attributes object to post data
            var post_data = Object.assign({},this.attributes[this.type])

            post_data["conn_id"]=this.id
            post_data["type"]=this.type
            post_data["title"]=this.attributes["title"]
            console.log(post_data)
            this.loading = true
            axios.post('http://localhost:8000/api/send_cred_req/',post_data).then(()=>{
                this.loading = false
            })
        }
    }
}
</script>

<style>
#request-form{
    display: block;
    margin: 5vh;
    width: 40vh;
}
</style>


