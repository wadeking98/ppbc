<template>
    <div >
        <ul>
            <li v-for="req in requests" :key="req.presentation_exchange_id">
                <!-- create a card for each presentation request -->
                <b-card class="req" bg-variant="info" text-variant="white">
                    <h5>Name: {{ req.presentation_request.name }}</h5>
                    <h6>Status: {{ req_alias[req.state] }}</h6>
                    <h6 v-if="req.state=='verified'">Verified Attributes:</h6>
                    <h6 v-else-if="req.state=='presentation_sent'">Sent Attributes:</h6>
                    <h6 v-else>Requested Attributes:</h6>
                    <!-- grab all the attributes in the credential that match
                    the presentation request -->
                    <div v-for="(val,key) in req.presentation_request.requested_attributes"
                    :key="key">
                        <p class="attr-val" 
                        v-if="req.state=='verified' || req.state=='presentation_sent'">
                            <!-- get the verified attribute values -->
                            {{ alias[val.name] }}: 
                            {{ req.presentation.requested_proof.revealed_attrs[key]['raw'] }}
                        </p>
                        <p class="attr" v-else>{{ alias[val.name] }}</p> 
                    </div>

                    <!-- load the request credentials on mouse over -->
                    <div v-if="req.state=='request_received'"
                    @mouseover="()=>{
                            id = req.presentation_exchange_id
                            //since all attributes in a card are from the same credential,
                            //we can just grab any attribute name and use it to get request credentials
                            attr = req.presentation_request.requested_attributes
                            refer = Object.keys(attr)[0]
                            get_req_cred(id, refer)
                        }">
                        <b-form v-on:submit.prevent="subm_cred(req)">
                            <b-form-select v-model="req_subm_vals[req.presentation_exchange_id]">
                                <option :value="null">--Please Select a Credential--</option>
                                <!-- create an option for each credential that is the same type as the
                                presentation request -->
                                <option v-for="cred in req_creds" :key="cred['cred_info']['referent']" 
                                :value="cred['cred_info']['referent']">
                                    <!-- load request attributes into option -->
                                    <p v-for="(val,key) in req.presentation_request.requested_attributes"
                                    :key="key">{{ alias[val.name] }} : {{ cred.cred_info.attrs[val.name] }} </p>
                                </option>
                            </b-form-select>
                            <b-button class="req_sub" type="submit">Submit</b-button>
                            
                        </b-form>
                    </div>
                    <b-button class="req_rem" @click="remove_req(req.presentation_exchange_id)">Remove</b-button>
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
            //holds the presentation requests
            requests:[],

            //holds the credentials related to a presentation request
            req_creds:[],

            //holds the request submission values ie.(request id paired with 
            //the id of the credential selected in the request card)
            req_subm_vals:{},

            //this conneciton id
            id:0,

            //mapping for raw names to aliases
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
            },

            req_alias:{
                "request_sent":"Pending",
                "request_received":"Recieved",
                "verified": "Verified",
                "presentation_sent":"Sent"
            }
        }
    },
    methods:{
        get_req_cred(req_id, ref){
            var post_data = {
                "id":req_id,
                "referent":ref
            }
            axios.post("http://localhost:8000/api/get_req_cred/", post_data).then((resp)=>{
                this.req_creds = resp.data
                
            })
        },
        subm_cred(req){
            //get the presentation request id and the cred referent for
            //this proof request
            var req_id = req.presentation_exchange_id
            var attr_keys = Object.keys(req.presentation_request.requested_attributes)

            //build the submission data in the following form 
            //{request id:{request attribute id:credential referent}}
            var subm_data={}
            subm_data[req_id]={}
            attr_keys.forEach((attr_key)=>{
                subm_data[req_id][attr_key] = this.req_subm_vals[req_id]
            })

            axios.post("http://localhost:8000/api/subm_pres/", subm_data).then(this.refresh_req)
            console.log(subm_data)
        },
        refresh_req(){
            axios.get("http://localhost:8000/api/get_req").then((response)=>{
                this.requests = response.data.results
                console.log(this.requests)
                //initialize the request submition value dictionary for each
                //presentation request
                this.requests.forEach(req => {
                    this.req_subm_vals[req.presentation_exchange_id]=""
                });
            })
        },
        remove_req(req_id){
            axios.post("http://localhost:8000/api/remove_req/", {"id":req_id}).then(this.refresh_req)
        }
    },
    created(){
        this.id = this.$route.params.conn_id
        this.refresh_req()
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
.attr-val{
    margin-left: 2vh;
}
.req_rem{
    margin-top: 2vh;
}
.req_sub{
    margin-top: 2vh;
}
</style>


