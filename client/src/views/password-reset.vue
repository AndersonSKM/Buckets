<template>
  <cmp-greeting-page :label="$t('password-reset-view.label')" :helpText="helpText">
    <v-form @submit.prevent="submit" ref="form" data-ref="form" v-if="!ok">
      <v-text-field
        prepend-icon="email"
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
      <v-layout row mt-3>
        <v-btn type="submit"
          outline
          round
          large
          block
          color="secondary"
          data-ref="submit"
          class="text-capitalize">
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
          color="success"
          class="text-capitalize"
          data-ref="return-to-sign-in">
          {{ $t('password-reset-view.return-to-sign-in') }}
        </v-btn>
      </v-layout>
    </div>
  </cmp-greeting-page>
</template>

<script>
import CmpGreetingPage from '@/components/greeting-page.vue'
import ApiValidationsHandlerMixin from '@/mixins/api-validations-handler.js'

export default {
  name: 'PasswordResetView',
  mixins: [ApiValidationsHandlerMixin],
  components: {
    'cmp-greeting-page': CmpGreetingPage
  },

  data () {
    return {
      ok: false,
      email: ''
    }
  },

  computed: {
    helpText () {
      const textKind = this.ok ? 'after' : 'before'
      return this.$t(`password-reset-view.help-text-${textKind}-send`)
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
