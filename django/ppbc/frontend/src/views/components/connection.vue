<template>
    <b-card bg-variant="info" text-variant="white">
    <h3>{{ partner }}</h3>
    <h5>Status: {{ status }}</h5>
    <h5>ID: {{ id }}</h5>
    <router-link :to="{name: 'messages', params:{conn_id:id}}">message</router-link>
    <b-link @click="removeConn()">remove</b-link>
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
</style>


