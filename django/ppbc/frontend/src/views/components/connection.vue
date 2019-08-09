<template>
    <b-card bg-variant="info" text-variant="white">
    <h3>{{ partner }}</h3>
    <h5>Status: {{ status }}</h5>

    <router-link class="options" :to="{name: 'messages', params:{conn_id:id}}">
        <b-button>message</b-button>
    </router-link>

    <router-link class="options" :to="{name: 'credentials', params:{conn_id:id}}">
        <b-button>credential</b-button>
    </router-link>

    <router-link class="options" :to="{name: 'out_requests', params:{conn_id:id}}">
        <b-button>send request</b-button>
    </router-link>

    <router-link class="options" :to="{name: 'in_requests', params:{conn_id:id}}">
        <b-button>request response</b-button>
    </router-link>

    <b-link class="options" @click="removeConn()">
        <b-button>remove</b-button>
    </b-link>
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


