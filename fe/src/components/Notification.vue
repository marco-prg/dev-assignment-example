<template>
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
      {{
        this.$te(`notification.error.${notificationState.error}`)
          ? this.$t(`notification.error.${notificationState.error}`)
          : notificationState.error
      }}
    </small>
    <template v-slot:action="{ attrs }">
      <v-btn color="white" text v-bind="attrs" @click="hideNotification">
        {{ $t("button.close") }}
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Notification",

  methods: {
    ...mapActions(["hideNotification"]),
  },

  computed: {
    ...mapGetters(["notificationState"]),
  },
}
</script>
