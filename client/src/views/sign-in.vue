<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center mb-5>
      <v-flex xs12 sm8 md6 lg3>
        <p class="text-xs-center display-1 font-weight-thin">{{ $t('application.name') }}</p>
        <v-form @submit.prevent="login" ref="form" data-ref="form">
          <v-layout align-center justify-space-around wrap fill-height mb-3>
            <v-avatar size="150" >
              <v-img
                :src="`https://cdn3.iconfinder.com/data/icons/cryptocurrency-and-blockchain/64/cryptocurrency_blockchain_mining-2-512.png`"
                aspect-ratio="1"
              />
            </v-avatar>
          </v-layout>
          <p
            data-ref="greeting-label"
            class="text-xs-center title font-weight-light">
            {{ $t('sign-in-view.label') }}
          </p>
          <v-layout align-center mt-3 mb-3 ml-4>
          <ul data-ref="error-list">
            <li class="title font-weight-light red--text" v-for="(error, index) in form_errors" :key="index">
              {{error}}
            </li>
          </ul>
          </v-layout>
          <v-text-field
            prepend-icon="person"
            label="E-mail"
            type="text"
            ref="email"
            data-ref="email"
            autofocus
            required
            v-model="email"
            v-validate="'required|email'"
            data-vv-name="email"
            :error-messages="errors.first('email')">
          </v-text-field>
          <v-text-field
            prepend-icon="lock"
            v-bind:label="$t('globals.password')"
            type="password"
            ref="password"
            data-ref="password"
            required
            v-model="password"
            v-validate="'required'"
            data-vv-name="password"
            :error-messages="errors.first('password')">
          </v-text-field>
          <v-layout row mt-2>
            <v-btn type="submit" round large block color="secondary" data-ref="submit" dark>
              <v-layout row justify-space-between>
                <v-flex xs2></v-flex><v-flex xs2>{{ $t('sign-in-view.login') }}</v-flex>
                <v-flex xs2>
                  <v-icon class="material-icons" right>keyboard_arrow_right</v-icon>
                </v-flex>
              </v-layout>
            </v-btn>
          </v-layout>
        </v-form>
        <v-layout justify-space-between row fill-height mt-3>
          <p class="subheading font-weight-light grey--text" role="button">
            <router-link to="/password-forgot" data-ref="password-forgot">
              <u>{{ $t('sign-in-view.forgot-your-password') }}</u>
            </router-link>
          </p>
          <p class="subheading font-weight-light grey--text" role="button">
            <u>{{ $t('sign-in-view.dont-have-an-account') }}</u>
          </p>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'SigInView',

  data () {
    return {
      email: '',
      password: '',
      form_errors: []
    }
  },

  methods: {
    async login () {
      this.form_errors = []

      if (!await this.$validator.validateAll()) {
        return
      }

      try {
        await this.$store.dispatch('auth/obtainToken', {
          email: this.email,
          password: this.password
        })

        this.$router.push('/home')
      } catch (error) {
        console.log(error)

        if (error.response.data) {
          this.form_errors = error.response.data['non_field_errors'] || []
        }
      }

      this.resetForm()
    },
    resetForm () {
      this.$refs.form.reset()
      this.$refs.email.focus()
    }
  }
}
</script>

<style scoped>
</style>
