<template>
  <v-card>
    <v-sheet class="stackSheet" color="white">
      <v-sparkline
        v-for="s in products.length"
        style="height: 300px"
        :key="s"
        :class="s == 1 ? 'stackSpark' : null"
        :value="getDataValues(s)"
        color="blue"
        line-width="1"
        padding="10"
        :labels="s == 1 ? labels : ''"
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
        <v-radio v-for="t in type" :key="t" :label="t" :value="t"></v-radio>
      </v-radio-group>
    </v-container>
  </v-card>
</template>

<script>
import { mapActions } from "vuex";
import axios from "axios";

export default {
  name: "Home",
  data: () => ({
    // data from API
    products: [],
    data: [],
    labels: [],
    // Configurable options
    month: [1, 3, 6, 12],
    monthGroup: 1,
    type: ["Open", "High", "Low", "Close"],
    typeGroup: "Close",
  }),

  async created() {
    await this.getDataFromApi();
  },

  methods: {
    ...mapActions(["showLoadingScreen"]),

    getDataValues(index) {
      return this.data.map((e) => e[index - 1]);
    },

    async getDataFromApi() {
      this.showLoadingScreen(true);
      axios
        .get(`getdata?months=${this.monthGroup}&type=${this.typeGroup}`)
        .then((response) => {
          // JSON responses are automatically parsed.
          console.log(response.data);
          let jsonResponse = response.data;

          this.products = jsonResponse.columns;
          this.data = jsonResponse.data;
          this.labels = jsonResponse.index;
        })
        .catch((e) => {
          console.error(e);
        })
        .finally(() => this.showLoadingScreen(false));
    },
  },

  watch: {
    monthGroup: async function () {
      await this.getDataFromApi();
    },

    typeGroup: async function () {
      await this.getDataFromApi();
    },
  },
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
