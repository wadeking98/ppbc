<template>
    <div class="hello">
        <h1>{{ conn_obj.their_label }}</h1>
        <div v-for="act in activity" v-bind:key="act.id">

            <p v-if="act.direction=='received'">{{ conn_obj.their_label }} :
                 {{ act.meta.content }}</p>

            <p v-else>me : {{ act.meta.content }}</p>
        </div>
        
        <b-form v-on:submit.prevent="send_msg()">
            <b-form-input 
                id="mess_box"
                v-model="msg"
                placeholder="Message"
            ></b-form-input>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button @click="refresh_msg()" variant="primary">Refresh</b-button>
        </b-form>
    </div>
</template>

<script>
    import router from '../router';
    import axios from 'axios';

    export default {
        name: 'Page2',
        data () {
            return {
                id: 0,
                activity: '',
                conn_obj: '',
                msg: ''
            }
        },
        created() {
            var vm = this
            this.id = this.$route.params.conn_id;
            axios.get('http://localhost:8000/api/list_conn/').then(function(response){
                vm.conn_obj = response.data
                .results.filter(conn => conn.connection_id == vm.id)[0];
                

                vm.activity = vm.conn_obj
                .activity.filter(act => act.type == "message").slice() .reverse();
            })

        },
        methods: {
            refresh_msg(){
                var vm = this
                axios.get('http://localhost:8000/api/list_conn/').then(function(response){
                    vm.conn_obj = response.data
                    .results.filter(conn => conn.connection_id == vm.id)[0];
                    

                    vm.activity = vm.conn_obj
                    .activity.filter(act => act.type == "message").slice().reverse();
                })
            },
            send_msg(){
                var vm = this
                axios.post('http://localhost:8000/api/send_msg/', "conn_id="+vm.id+"&msg="+vm.msg).then(function(){
                    vm.refresh_msg();
                });
            }
        }
    }
</script>

<style scoped>
    h1, h2 {
        font-weight: normal;
    }

</style>