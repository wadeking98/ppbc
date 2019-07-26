<template>
    <div>
        <b-form class="cred-form">
            <b-form-select v-model="type" :options="options" class="cred-select"
            id="type-select"></b-form-select>
            
            <div v-if="type=='imm'" class="cred-imm-form">
                <b-form-input class="cred-imm-id" type="text" v-model="imm_id" placeholder="ID"></b-form-input>
                <b-form-input class="cred-imm-name" type="text" v-model="imm_name" placeholder="Immunization Name"></b-form-input>
                <b-form-input class="cred-imm-date" type="date" v-model="imm_date"></b-form-input>
            </div>
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
    }
}
</script>
<style>
.cred-select{
    width: 40vh;
}
.cred-imm-id{
    width:30vh;
}
.cred-imm-name{
    width:40vh;
}
.cred-imm-date{
    width:35vh;
}
.cred-form *{
    display: inline-block;
}
.cred-form *:not(div){
    margin:5vh;
}
</style>



