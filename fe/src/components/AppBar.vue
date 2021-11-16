<template>
  <v-app-bar app>
    <v-tabs 
      align-with-title
      :value="getActiveTab"
      class="section-tabs ml-4"
    >
      <v-tab
        v-for="item in mainRoutes"              
        :key="item.path"
        class="d-flex pa-0 ml-0"
      >
        <router-link 
          :to="item.path"
          class="section-link px-2 pt-6"
        >
          {{ $t(`appbar.${item.name}`) }}
        </router-link>
      </v-tab>
    </v-tabs>
  </v-app-bar>
</template>

<script>
import { routes } from "../router";

export default {
  name: "AppBar",

  data: () => ({
  }),

  computed: {    
    mainRoutes: function() {
      return routes
        .filter((r) => r.mainMenu);
    },

    getActiveTab: function() {
      return this.$route.meta.number;
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.section-tabs {
  max-width: 900px;
}

.section-link {
  text-decoration: none;
  width: 100%; 
  height: 100%;
}
</style>
