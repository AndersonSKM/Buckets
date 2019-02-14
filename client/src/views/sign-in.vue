<template>
  <cmp-greeting-page :label="label">
    <v-form @submit.prevent="login" ref="form" data-ref="form">
      <v-layout align-center mt-3 mb-3 ml-4>
        <ul data-ref="error-list">
          <li
            class="title font-weight-light red--text"
            v-for="(error, index) in errors.collect('non_field_errors')"
            :key="index">
            {{error}}
          </li>
        </ul>
      </v-layout>
      <v-text-field
        data-ref="email"
        prepend-icon="person"
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
        data-ref="password"
        prepend-icon="lock"
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
        <router-link to="/password-reset" data-ref="password-forgot">
          <u>{{ $t('sign-in-view.forgot-your-password') }}</u>
        </router-link>
      </p>
      <p class="subheading font-weight-light grey--text" role="button">
        <u>{{ $t('sign-in-view.dont-have-an-account') }}</u>
      </p>
    </v-layout>
  </cmp-greeting-page>
</template>

<script>
import CmpGreetingPage from '@/components/greeting-page.vue'
import ApiValidationsHandlerMixin from '@/mixins/api-validations-handler.js'

export default {
  name: 'SigInView',
  mixins: [ApiValidationsHandlerMixin],
  components: {
    'cmp-greeting-page': CmpGreetingPage
  },

  data () {
    return {
      email: '',
      password: ''
    }
  },

  computed: {
    label () {
      return this.$t('sign-in-view.label')
    }
  },

  methods: {
    async login () {
      if (!await this.$validator.validateAll()) {
        return
      }

      try {
        const response = await this.$store.dispatch('auth/obtainToken', {
          email: this.email,
          password: this.password
        })

        if (response.status === 200) {
          this.$router.push('/')
        }
      } catch (error) {
        this.handleApiValidations(error, this.$validator)
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
