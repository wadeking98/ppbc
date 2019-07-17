<template>
    <b-card bg-variant="info" text-variant="white">
    <h3>{{ partner }}</h3>
    <h5>Status: {{ status }}    Type: {{ type }}</h5>
    <div id="req">
    <a class = pfReq href="#" v-if='status === "Active"'><h5>Send proof request</h5></a>
    <a class = pfReq href="#" v-if='type === "Outbound" && status === "Active"'><h5>Send Credential</h5></a>
    </div>
    </b-card>
</template>
<script>
export default {
    name:'connection',
    props:['wallet', 'partner', 'status', 'type'],
}
</script>
<style>
</style>


