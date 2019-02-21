<template>
  <v-layout align-center mt-3 mb-3 ml-4>
    <ul data-ref="error-list">
      <li
        class="title font-weight-light red--text"
        v-for="(error, index) in nonFieldErrors"
        :key="index"
      >
        {{ error }}
      </li>
    </ul>
  </v-layout>
</template>

<script>
export default {
  name: 'FormErrorList',
  computed: {
    nonFieldErrors () {
      return this.errors.items
        .filter(error => error.field === 'non_field_errors')
        .map(error => error.msg)
    }
  }
}
</script>
