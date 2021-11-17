<template>
  <v-card>
    <v-sheet class="stackSheet" color="white">
      <div id="chart">
        <apexchart
          type="area"
          height="350"
          :options="chartOptions"
          :series="series"
        ></apexchart>
      </div>
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
    // Configurable options
    month: [1, 3, 6, 12],
    monthGroup: 1,
    type: ["Open", "High", "Low", "Close"],
    typeGroup: "Close",

    // ApexChart
    series: [],
    chartOptions: {
      chart: {
        type: "area",
        stacked: true,
        height: 350,
        zoom: {
          type: "x",
          enabled: true,
          autoScaleYaxis: true,
        },
        toolbar: {
          autoSelected: "zoom",
        },
      },
      dataLabels: {
        enabled: false,
      },
      markers: {
        size: 0,
      },
      title: {
        text: "Stock Price Movement",
        align: "left",
      },
      fill: {
        type: "gradient",
        gradient: {
          shadeIntensity: 1,
          inverseColors: false,
          opacityFrom: 0.5,
          opacityTo: 0,
          stops: [0, 90, 100],
        },
      },
      yaxis: {
        labels: {
          formatter: function (val) {
            return val.toFixed(2);
          },
        },
        title: {
          text: "Price",
        },
      },
      xaxis: {
        //type: "datetime",
      },
      tooltip: {
        shared: true,
        y: {
          formatter: function (val) {
            return val.toFixed(2);
          },
        },
      },
    },
  }),

  async created() {
    await this.getDataFromApi();
  },

  methods: {
    ...mapActions(["showLoadingScreen"]),

    async getDataFromApi() {
      this.showLoadingScreen(true);
      axios
        .get(`getdata?months=${this.monthGroup}&type=${this.typeGroup}`)
        .then((response) => {
          // JSON responses are automatically parsed.
          let jsonResponse = response.data;

          let products = jsonResponse.columns;
          let data = jsonResponse.data;
          //let labels = jsonResponse.index;

          this.series = [];
          for (const [index, product] of products.entries()) {
            this.series.push({
              name: product,
              data: data.map(e => e[index])
            })
          }
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
