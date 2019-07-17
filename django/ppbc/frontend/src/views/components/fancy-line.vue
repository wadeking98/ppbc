<template>
    <svg :height="(Number(r))*2" :width="(Number(r))*2" style="position:absolute;z-index:10;" 
    v-bind:style="{left:Number(x)-Number(r), top:Number(y)-Number(r)}">
        <line :x1="Number(r)" :y1="Number(r)" 
        :x2="(r*Math.cos(deg*Math.PI/180))+Number(r)" :y2="(r*Math.sin(deg*Math.PI/180))+Number(r)"
        style="stroke:rgb(255,255,255);stroke-width:2;position:absolute;" v-bind:style="{opacity: Math.min(lim2-deg, deg-lim1)/(lim2-lim1)}" />
    </svg>
</template>

<script>
export default {
    name: 'fancy-line',
    props: ['x', 'y', 'theta', 'r', 'dir', 'lim1', 'lim2'],
    data: function(){
        return{
        deg: this.theta,
        velocity: this.dir
        }
    },
    mounted() {
        var vm = this;
        setInterval(function(){
        if(vm.deg <= vm.lim1 || vm.deg >= vm.lim2){
            vm.velocity = -Number(vm.velocity)
        }
        vm.deg=(Number(vm.deg)+Number(vm.velocity))%360;
        }, 20);
    }
}
</script>

<style>
svg{
    pointer-events: none;
}
</style>
