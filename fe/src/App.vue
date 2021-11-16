<template>
  <v-app>
    <AppBar />
    <v-main>
      <v-overlay :value="isLoading">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
    <v-snackbar
      :value="notificationState.text"
      :multi-line="true"
      :timeout="-1"
      :top="true"
      :right="true"
      :color="notificationState.error ? 'red' : 'blue'"
    >
      {{ notificationState.text }}
      <small v-if="notificationState.error">
        <br />
        {{ this.$te(`notification.error.${notificationState.error}`) ? this.$t(`notification.error.${notificationState.error}`) : notificationState.error }}
      </small>
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="hideNotification">
          {{ $t("button.close") }}
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import AppBar from './components/AppBar.vue'
import { mapGetters, mapActions } from "vuex";
import { setUrl } from './store/helpers';

export default {
  components: {
    AppBar,
  },

  methods: {
    ...mapActions([
      "showLoadingScreen",
      "hideNotification"
    ]),
  },

  async created() {
    var configHeaders = new Headers();
    configHeaders.append('pragma', 'no-cache');
    configHeaders.append('cache-control', 'no-cache');

    var configInit = {
      method: 'GET',
      headers: configHeaders,
    };

    var configRequest = new Request('config.json');

    const configRes = await fetch(configRequest, configInit).catch(e => console.error('error', e));
    const configJson = await configRes.json();
    setUrl(configJson.api_url.value);
    this.showLoadingScreen(false);
  },

  computed: {
    ...mapGetters(["isLoading", "notificationState"]),
  },
  
}
</script>

<style scoped>
.container {
  height: 100%;
}
</style>
