<template>
  <v-sheet class="stackSheet" color="white">
    <v-sparkline
      :value="value1"
      color="blue"
      line-width="3"
      padding="10"
    ></v-sparkline>
    <v-sparkline
      class="stackSpark"
      :value="value2"
      color="red"
      line-width="3"
      padding="10"
    ></v-sparkline>
  </v-sheet>
</template>

<script>
export default {
  name: 'Home',
  data: () => ({
    value1: [0, 2, 5, 9, 5, 10, 3, 5, 0, 0, 1, 8, 2, 9, 0],
    value2: [7, 4, 7, 2, 9, 0, 1, 2, 4, 7, 7, 10, 1, 3, 5],
  }),
};
</script>
<style scoped>
.stackSheet {
  position: relative;
}
.stackSpark {
  position: absolute;
  top: 0;
  left: 0;
}
</style>
