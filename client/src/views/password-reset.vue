<template>
  <cmp-greeting-page
    :label="$t('password-reset-view.label')"
    :helpText="helpText">
    <v-alert
      data-ref="success-info"
      :value="ok"
      color="success"
      icon="check_circle"
      outline>
      {{ $t('password-reset-view.alert-after-send') }}
    </v-alert>
    <v-form @submit.prevent="submit" ref="form" data-ref="form" v-if="!ok">
      <v-text-field
        prepend-icon="email"
        label="E-mail"
        color="grey darken-2"
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
      <v-layout row mt-3>
        <v-btn type="submit"
          outline
          round
          large
          block
          color="secondary"
          data-ref="submit"
          class="text-none">
          {{ $t('password-reset-view.send-password-reset-email') }}
        </v-btn>
      </v-layout>
    </v-form>
    <div data-ref="try-sign-in" v-if="ok">
      <v-layout row mt-3>
        <v-btn
          to="/sign-in"
          outline
          round
          large
          block
          color="secondary"
          class="text-none"
          data-ref="return-to-sign-in">
          {{ $t('password-reset-view.return-to-sign-in') }}
        </v-btn>
      </v-layout>
    </div>
  </cmp-greeting-page>
</template>

<script>
import ApiValidationsHandlerMixin from '@/mixins/api-validations-handler.js'

export default {
  name: 'PasswordResetView',
  mixins: [ApiValidationsHandlerMixin],
  components: {
    'cmp-greeting-page': () => import('@/components/greeting-page.vue')
  },

  data () {
    return {
      ok: false,
      email: ''
    }
  },

  computed: {
    helpText () {
      return this.ok ? null : this.$t('password-reset-view.help-text')
    }
  },

  methods: {
    async submit () {
      if (!await this.$validator.validateAll()) {
        return this.resetForm()
      }

      try {
        const response = await this.$services.user.sendPasswordResetEmail(this.email)
        this.ok = response.status === 204
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
