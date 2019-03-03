<template>
  <cmp-greeting-page :label="$t('sign-up-view.label')">
    <v-alert
      data-ref="success-info"
      :value="ok"
      color="success"
      icon="check_circle"
      outline>
      {{ $t('sign-up-view.alert-after-create') }}
    </v-alert>
    <v-form @submit.prevent="submit" ref="form" data-ref="form" v-if="!ok">
      <cmp-form-error-list/>
      <v-text-field
        data-ref="name"
        prepend-icon="person"
        color="grey darken-2"
        :label="$t('sign-up-view.name')"
        type="text"
        ref="name"
        autofocus
        required
        v-model="name"
        v-validate="'required'"
        data-vv-name="name"
        :error-messages="errors.first('name')">
      </v-text-field>
      <v-text-field
        data-ref="email"
        prepend-icon="email"
        color="grey darken-2"
        label="E-mail"
        type="text"
        ref="email"
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
        :label="$t('sign-up-view.password')"
        type="password"
        ref="password"
        required
        v-model="password"
        v-validate="'required'"
        data-vv-name="password"
        :error-messages="errors.first('password')">
      </v-text-field>
      <v-layout row mt-1>
        <v-btn
          type="submit"
          round
          large
          block
          outline
          color="secondary"
          data-ref="submit"
          class="text-none"
          dark>
          {{ $t('sign-up-view.continue') }}
        </v-btn>
      </v-layout>
      <cmp-sign-in-reference :label="$t('sign-up-view.already-have-account')"/>
    </v-form>
    <div data-ref="try-sign-in" v-if="ok">
      <v-layout row mt-2>
        <v-btn
          to="/sign-in"
          outline
          round
          large
          block
          color="secondary"
          class="text-none"
          data-ref="return-to-sign-in">
          {{ $t('sign-up-view.sign-in-now') }}
        </v-btn>
      </v-layout>
    </div>
  </cmp-greeting-page>
</template>

<script>
import ApiValidationsHandlerMixin from '@/mixins/api-validations-handler.js'

export default {
  name: 'SignUpView',
  mixins: [ApiValidationsHandlerMixin],
  components: {
    'cmp-greeting-page': () => import('@/components/greeting-page.vue'),
    'cmp-form-error-list': () => import('@/components/form-error-list.vue'),
    'cmp-sign-in-reference': () => import('@/components/sign-in-reference.vue')
  },

  data () {
    return {
      ok: false,
      name: '',
      email: '',
      password: ''
    }
  },

  methods: {
    async submit () {
      if (!await this.$validator.validateAll()) {
        return
      }

      try {
        const response = await this.$services.user.create({
          name: this.name,
          email: this.email,
          password: this.password
        })

        this.ok = response.status === 201
      } catch (error) {
        this.handleApiValidations(error, this.$validator)
        this.password = ''
      }
    }
  }
}
</script>

<style scoped>

</style>
