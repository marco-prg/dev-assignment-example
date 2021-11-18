<template>
  <v-card>
    <v-sheet class="stackSheet" color="white">
      <div id="chart">
        <apexchart
          class="pa-4"
          type="area"
          height="350"
          :options="chartOptions"
          :series="series"
        ></apexchart>
      </div>
    </v-sheet>

    <v-container fluid class="d-flex flex-row pa-4">
      <v-radio-group v-model="monthGroup">
        <h4 class="ml-2 mb-2">Time interval:</h4>
        <v-radio
          v-for="m in month"
          :key="m"
          :label="`${m} ${m > 1 ? 'months' : 'month'}`"
          :value="m"
        ></v-radio>
      </v-radio-group>
      <v-radio-group v-model="typeGroup" class="ml-12">
        <h4 class="ml-2 mb-2">Stock price type:</h4>
        <v-radio v-for="t in type" :key="t" :label="t" :value="t"></v-radio>
      </v-radio-group>
      <v-data-table
        class="elevation-1 forecastTable"
        :headers="headers"
        :items="forecastItems"
        :hide-default-footer="true"
        :disable-pagination="true"
      ></v-data-table>
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
    // Data table
    headers: [
      {
        align: "start",
        text: "Product",
        value: "product",
        width: "200px",
      },
      {
        align: "start",
        text: "Price forecast (tomorrow)",
        value: "forecast",
        width: "200px",
      },
    ],
    forecastItems: [],

    // ApexChart
    series: [],
    chartOptions: {
      chart: {
        type: "area",
        stacked: false,
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
        text: "Stock price movement",
        align: "left",
        style: {
          fontSize: "16px",
          fontWeight: "bold",
          fontFamily: "Roboto, sans-serif",
          color: "black",
        },
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
        type: "datetime",
        labels: {
          show: true,
          rotate: -45,
          rotateAlways: false,
          hideOverlappingLabels: true,
          showDuplicates: false,
          trim: false,
          maxHeight: 60,
          style: {
            colors: [],
            fontSize: "12px",
            fontFamily: "Roboto, sans-serif",
            fontWeight: 400,
            cssClass: "apexcharts-xaxis-label",
          },
          offsetX: 0,
          offsetY: 0,
          //format: undefined,
          //formatter: undefined,
          datetimeUTC: true,
          datetimeFormatter: {
            year: "yyyy",
            month: "MMM 'yy",
            day: "dd MMM",
            hour: "HH:mm",
          },
        },
      },
      legend: {
        position: "top",
      },
      tooltip: {
        shared: true,
        x: {
          format: "dd MMM yyyy",
        },
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
    ...mapActions(["showLoadingScreen", "showNotification"]),

    async getDataFromApi() {
      this.showLoadingScreen(true);
      axios
        .get(`getdata?months=${this.monthGroup}&type=${this.typeGroup}`)
        .then((response) => {
          let responseData = response.data;

          let history = JSON.parse(responseData.history);

          this.series = [];
          for (const [index, product] of history.columns.entries()) {
            this.series.push({
              name: product,
              data: history.data.map((e, i) => [history.index[i], e[index]]),
            });
          }

          let forecast = JSON.parse(responseData.forecast);
          
          this.forecastItems = [];
          for (const [index, product] of forecast.columns.entries()) {
            this.forecastItems.push({
              product: product,
              forecast: forecast.data.map(e => e[index].toFixed(2)),
            });
          }

        })
        .catch((e) => {
          console.error(e);
          this.showNotification({
            text: this.$t("notification.apiError"),
            error: e,
          });
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
.forecastTable {
  position: absolute;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 400px;
}
</style>
