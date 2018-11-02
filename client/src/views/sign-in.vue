<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center mb-5>
      <v-flex xs12 sm8 md6 lg3>
        <p class="text-xs-center display-1 font-weight-thin">{{ $t('application.name') }}</p>
        <v-form>
          <v-layout align-center justify-space-around wrap fill-height mb-3>
            <v-avatar size="150" >
              <v-img
                :src="`https://cdn3.iconfinder.com/data/icons/cryptocurrency-and-blockchain/64/cryptocurrency_blockchain_mining-2-512.png`"
                aspect-ratio="1"
              />
            </v-avatar>
          </v-layout>
          <p class="text-xs-center title font-weight-light">{{ $t('sign-in.label') }}</p>
          <v-layout align-center mt-3 mb-3 ml-4>
          <ul>
            <li class="title font-weight-light red--text" v-for="(error, index) in form_errors" :key="index">
              {{error}}
            </li>
          </ul>
          </v-layout>
          <v-text-field
            id="email"
            prepend-icon="person"
            name="login"
            label="E-mail"
            type="text"
            ref="email"
            autofocus
            required
            v-model="email"
            v-validate="'required|email'"
            data-vv-name="email"
            :error-messages="errors.first('email')">
          </v-text-field>
          <v-text-field
            id="password"
            prepend-icon="lock"
            name="password"
            v-bind:label="$t('globals.password')"
            type="password"
            ref="password"
            required
            v-model="password"
            v-validate="'required'"
            data-vv-name="password"
            :error-messages="errors.first('password')">
          </v-text-field>
          <v-layout row mt-2>
            <v-btn id="btn-submit" type="submit" round large block color="secondary" dark @click="login">
              <v-layout row justify-space-between>
                <v-flex xs2></v-flex><v-flex xs2>{{ $t('sign-in.login') }}</v-flex>
                <v-flex xs2>
                  <v-icon class="material-icons" right>keyboard_arrow_right</v-icon>
                </v-flex>
              </v-layout>
            </v-btn>
          </v-layout>
        </v-form>
        <v-layout justify-space-between row fill-height mt-3>
          <p class="subheading font-weight-light grey--text" role="button">
            <u>{{ $t('sign-in.forgot-your-password') }}</u>
          </p>
          <p class="subheading font-weight-light grey--text" role="button">
            <u>{{ $t('sign-in.dont-have-an-account') }}</u>
          </p>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'SigIn',

  data () {
    return {
      email: '',
      password: '',
      form_errors: []
    }
  },

  methods: {
    async login (submitEvent) {
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
    }
  }
}
</script>

<style scoped>
</style>
