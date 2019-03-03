<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md6 lg3>
        <v-layout align-center justify-space-around wrap fill-height mt-1>
          <p
            data-ref="app-name"
            class="text-lg-center display-1 font-weight-thin">
            {{ $t('globals.app-name') }}
          </p>
        </v-layout>
        <v-layout row align-center justify-space-around wrap fill-height mt-1>
          <v-avatar size="150" >
            <v-img
              :src="`https://cdn3.iconfinder.com/data/icons/cryptocurrency-and-blockchain/64/cryptocurrency_blockchain_mining-2-512.png`"
              aspect-ratio="1"
            />
          </v-avatar>
        </v-layout>
        <v-layout row align-center justify-space-around wrap fill-height mt-1>
          <p
            class="text-sm-center title font-weight-light"
            data-ref="greeting-label" mt-3>
            {{ label }}
          </p>
        </v-layout>
        <v-layout row align-center justify-space-around wrap fill-height mt-1 mb-1 v-if="helpText">
          <p
            class="text-xs-center title font-weight-light"
            data-ref="help-text" mt-3>
            {{ helpText }}
          </p>
        </v-layout>
        <slot></slot>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'GreetingPage',

  props: {
    label: {
      type: String,
      required: true
    },
    helpText: {
      type: String,
      required: false
    }
  }
}
</script>

<style scoped>
</style>
