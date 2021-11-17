<template>
  <v-card>
    <v-sheet class="stackSheet" color="white">
      <v-sparkline
        :value="value1"
        color="blue"
        line-width="1"
        padding="10"
        show-labels="true"
      ></v-sparkline>
      <v-sparkline
        class="stackSpark"
        :value="value2"
        color="red"
        line-width="1"
        padding="10"
      ></v-sparkline>
      <v-sparkline
        class="stackSpark"
        :value="value3"
        color="green"
        line-width="1"
        padding="10"
      ></v-sparkline>
    </v-sheet>

    <v-container fluid class="d-flex flex-row">
      <v-radio-group v-model="monthGroup">
        <v-radio
          v-for="m in month"
          :key="m"
          :label="`${m} ${m > 1 ? 'months' : 'month'}`"
          :value="m"
        ></v-radio>
      </v-radio-group>

      <v-radio-group v-model="typeGroup" class="pl-12">
        <v-radio
          v-for="t in type"
          :key="t"
          :label="t"
          :value="t"
        ></v-radio>
      </v-radio-group>
    </v-container>
  </v-card>
</template>

<script>
import { get } from "../store/helpers.js";

export default {
  name: "Home",
  data: () => ({
    value1: [0, 2, 5, 9, 5, 10, 3, 5, 0, 0, 1, 8, 2, 9, 0],
    value2: [7, 4, 7, 2, 9, 0, 1, 2, 4, 7, 7, 10, 1, 3, 5],
    value3: [17, 4, 7, 2, 5, 4, 3, 2, 5, 2, 1, 10, 1, 3, 5],
    month: [1, 3, 6, 12],
    monthGroup: 1,
    type: ["Open", "High", "Low", "Close"],
    typeGroup: "Close"
  }),

  methods: {
    async getDataFromApi() {
      this.loading = true;

      let query = "getdata";

      const res = await get(query);
      const json = await res.json();

      this.items = json.result;

      this.loading = false;
    },
  }
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
