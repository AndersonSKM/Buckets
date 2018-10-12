<template>
  <div>
    <p>Home</p>
    <v-btn @click="teste">Teste</v-btn>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    teste () {
      console.log('teste')
      this.$router.push('/home')
    }
  }
}
</script>

<style scoped>
</style>
