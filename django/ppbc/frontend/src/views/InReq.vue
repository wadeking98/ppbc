<template>
    <div >
        <ul>
            <li v-for="req in requests" :key="req.presentation_exchange_id">
                <!-- create a card for each presentation request -->
                <b-card class="req" bg-variant="info" text-variant="white">
                    <h5>Name: {{ req.presentation_request.name }}</h5>
                    <h6>Status: {{ req.state }}</h6>
                    <h6>Attributes:</h6>
                    <!-- grab all the attributes in the credential that match
                    the presentation request -->
                    <div v-for="(val,key) in req.presentation_request.requested_attributes"
                    :key="key">
                        <p class="attr" >{{ alias[val.name] }}</p>
                    </div>

                    <!-- load the request credentials on mouse down -->
                    <div v-if="req.state=='request_received'"
                    @mousedown="()=>{
                            id = req.presentation_exchange_id
                            attr = req.presentation_request.requested_attributes
                            refer = Object.keys(attr)[0]
                            get_req_cred(id, refer)
                        }">
                        <b-form v-on:submit.prevent="subm_cred(req.presentation_exchange_id)">
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
                            <b-button type="submit">Submit</b-button>
                        </b-form>
                    </div>
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
        subm_cred(req_id){
            //get the presentation request id and the cred referent for
            //this proof request
            console.log({"id":req_id,"ref":this.req_subm_vals[req_id]})
        }
    },
    created(){
        this.id = this.$route.params.conn_id
        axios.get("http://localhost:8000/api/get_req").then((response)=>{
            this.requests = response.data.results
            console.log(this.requests)
            //initialize the request submition value dictionary for each
            //presentation request
            this.requests.forEach(req => {
                this.req_subm_vals[req.presentation_exchange_id]=""
            });
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


