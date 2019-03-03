<template>
  <v-layout row align-center justify-space-around wrap fill-height mt-3>
    <p
      class="subheading font-weight-light"
      data-ref="sign-in-reference-label" mt-3>
      {{ label }}
      <router-link to="/sign-in" data-ref="sign-in-reference-link">
        <u class="grey--text text--darken-4">{{ $t('sign-in-view.label') }}</u>
      </router-link>
    </p>
  </v-layout>
</template>

<script>
export default {
  name: 'SignInReference',
  props: {
    label: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
