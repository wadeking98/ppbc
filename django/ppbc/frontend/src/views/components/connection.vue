<template>
    <b-card bg-variant="info" text-variant="white">
    <h3>{{ partner }}</h3>
    <h5>Status: {{ status }}</h5>
    <h5>ID: {{ id }}</h5>
    <router-link class="options" :to="{name: 'messages', params:{conn_id:id}}">message</router-link>
    <router-link class="options" :to="{name: 'credentials', params:{conn_id:id}}">credential</router-link>
    <router-link class="options" :to="{name: 'out_requests', params:{conn_id:id}}">send request</router-link>
    <router-link class="options" :to="{name: 'in_requests', params:{conn_id:id}}">request response</router-link>
    <b-link class="options" @click="removeConn()">remove</b-link>
    </b-card>
</template>
<script>
import axios from 'axios'
export default {
    name:'connection',
    props:['wallet', 'partner', 'status', 'id'],
    methods:{
        removeConn(){
            var vm = this
            axios.post('http://localhost:8000/api/del_conn/', 'conn_id='+vm.id).then(function(){
                vm.$emit('refresh')
            })
        }
    },
}
</script>
<style>
.options{
    margin: 1vh;
}
</style>


