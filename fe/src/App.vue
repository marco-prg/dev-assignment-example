<template>
  <v-app>
    <app-bar />
    <v-main>
      <v-overlay :value="isLoading">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
    <notification />
  </v-app>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "App",

  computed: {
    ...mapGetters(["isLoading"]),
  },
};
</script>

<style scoped>
.container {
  height: 100%;
}
</style>
