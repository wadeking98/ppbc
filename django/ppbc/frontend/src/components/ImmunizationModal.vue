<template>
  <div>
    <!-- <b-btn v-b-modal.modal1>Launch demo modal</b-btn> -->
    <!-- Modal Component -->
    <b-modal id="modal1" title="Immunization Modal">
      <p class="my-4">Hello from modal!</p>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "ImmunizationModal",
  data: () => {
    return {};
  },
  props: {},
  methods: {}
};
</script>

<style scoped>
</style>
