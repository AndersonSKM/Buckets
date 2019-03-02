<template>
  <cmp-greeting-page :label="label">
    <v-form @submit.prevent="login" ref="form" data-ref="form">
      <cmp-form-error-list/>
      <v-text-field
        data-ref="email"
        prepend-icon="email"
        color="grey darken-2"
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
        color="grey darken-2"
        :label="$t('globals.password')"
        type="password"
        ref="password"
        required
        v-model="password"
        v-validate="'required'"
        data-vv-name="password"
        :error-messages="errors.first('password')">
      </v-text-field>
      <v-layout row mt-2>
        <v-btn
          type="submit"
          round
          large
          block
          outline
          color="secondary"
          class="text-capitalize"
          data-ref="submit"
          dark>
          {{ $t('sign-in-view.login') }}
        </v-btn>
      </v-layout>
    </v-form>
    <v-layout justify-space-between row fill-height mt-3>
      <p class="subheading font-weight-light" role="button">
        <router-link to="/password-reset" data-ref="password-forgot">
          <u class="grey--text text--darken-4">{{ $t('sign-in-view.forgot-your-password') }}</u>
        </router-link>
      </p>
      <p class="subheading font-weight-light" role="button">
        <router-link to="/sign-up" data-ref="sign-up">
          <u class="grey--text text--darken-4">{{ $t('sign-in-view.dont-have-an-account') }}</u>
        </router-link>
      </p>
    </v-layout>
  </cmp-greeting-page>
</template>

<script>
import ApiValidationsHandlerMixin from '@/mixins/api-validations-handler.js'

export default {
  name: 'SigInView',
  mixins: [ApiValidationsHandlerMixin],
  components: {
    'cmp-greeting-page': () => import('@/components/greeting-page.vue'),
    'cmp-form-error-list': () => import('@/components/form-error-list.vue')
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
