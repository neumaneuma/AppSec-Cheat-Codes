<template>
  <div>
    <ChallengeView
      :title="'Challenge #1: SQLi login bypass'"
      :introduction="'What is SQL injection?'"
      :shouldShowIntroduction="shouldShowIntroduction"
      :vulnerabilitySourceCode="{
        fileLink:
          'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/vulnerabilities/sqli_login_bypass.py',
        snippet: sqliLoginBypassVulnerableSnippet,
      }"
      :exploitSourceCode="{
        fileLink:
          'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/exploits/sqli_login_bypass.py',
        snippet: sqliLoginBypassExploitSnippet,
      }"
    >
      <template #introduction>
        <SQLiIntroduction />
      </template>
      <template #news>
        <SQLiNews />
      </template>
    </ChallengeView>

    <div class="challenge-sections">
      <!-- Login Form Section -->
      <section class="challenge-section">
        <h2 class="section-title">Login Challenge</h2>
        <p class="challenge-description">
          You know there is a user with the username
          <span class="code-block">administrator</span>. Try to figure out how to login as
          <span class="code-block">administrator</span> without knowing what their password is!
        </p>

        <div class="form-container">
          <AlertMessage v-if="loginApiState.error" :message="loginApiState.error" type="error" />
          <AlertMessage
            v-if="loginApiState.success"
            :message="loginApiState.success"
            type="success"
          />

          <form @submit.prevent="submitLogin" class="form">
            <div class="form-group">
              <label class="form-label" for="username">Username</label>
              <input
                v-model="username"
                :disabled="loginApiState.isLoading"
                class="form-input"
                name="username"
                id="username"
                type="text"
                placeholder="Username"
              />
            </div>
            <div class="form-group">
              <label class="form-label" for="password">Password</label>
              <input
                v-model="password"
                :disabled="loginApiState.isLoading"
                class="form-input"
                name="password"
                id="password"
                type="password"
                placeholder="******************"
              />
            </div>
            <div class="form-actions">
              <button :disabled="loginApiState.isLoading" class="submit-button" type="submit">
                <LoadingSpinner v-if="loginApiState.isLoading" />
                <span v-else>Login</span>
              </button>
            </div>
          </form>
        </div>
      </section>

      <PassphraseSubmission challenge-id="sqli1" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/AlertMessage.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { SQLI_LOGIN_BYPASS_API_VULNERABLE_URL } from '@/constants'
import SQLiIntroduction from '@/views/sqli/SQLiIntroduction.vue'
import SQLiNews from '@/views/sqli/SQLiNews.vue'
import ChallengeView from '@/views/ChallengeView.vue'
import { store } from '@/store'
import { sqliLoginBypassVulnerableSnippet } from '@/snippets'
import { sqliLoginBypassExploitSnippet } from '@/snippets'
import PassphraseSubmission from '@/components/PassphraseSubmission.vue'

const username = ref('')
const password = ref('')
const { state: loginApiState, handleApiCall: handleLoginApiCall } = useApiState()

function determineIfShouldShowIntroduction() {
  const shouldShowIntroduction = !store.sqliIntroductionSeen
  store.sqliIntroductionSeen = true
  return shouldShowIntroduction
}
const shouldShowIntroduction = computed(determineIfShouldShowIntroduction)

const submitLogin = async () => {
  await handleLoginApiCall(async () => {
    const response = await fetch(SQLI_LOGIN_BYPASS_API_VULNERABLE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }

    return response.json()
  }, 'Login successful!')
}
</script>

<style scoped>
.challenge-title {
  margin-top: 1.5rem;
  font-size: 2.25rem;
  line-height: 2.5rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.challenge-description {
  margin: 2rem 0;
}

.code-block {
  background-color: rgb(229, 231, 235);
  padding: 0.15rem;
  font-family: ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
}

.challenge-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin: 2rem auto;
  max-width: 64rem;
  padding: 0 2rem;
}

.challenge-section {
  background-color: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: rgb(17, 24, 39);
  margin-bottom: 1rem;
}

.form {
  background-color: rgb(249, 250, 251);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid rgb(229, 231, 235);
  width: 100%;
  box-sizing: border-box;
}

.form-container {
  width: 100%;
  max-width: 100%;
  margin: 1.5rem auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  color: rgb(55, 65, 81);
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  letter-spacing: 0.025em;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid rgb(209, 213, 219);
  border-radius: 0.5rem;
  color: rgb(55, 65, 81);
  line-height: 1.25;
  transition: all 0.15s ease-in-out;
  background-color: rgb(249, 250, 251);
  box-sizing: border-box;
}

.form-input:hover {
  border-color: rgb(156, 163, 175);
}

.form-input:focus {
  outline: none;
  border-color: rgb(59, 130, 246);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  background-color: white;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.submit-button {
  background-color: rgb(59, 130, 246);
  color: white;
  font-weight: 600;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  transition: all 0.15s ease-in-out;
  border: none;
  cursor: pointer;
  min-width: 8rem;
}

.submit-button:hover:not(:disabled) {
  background-color: rgb(37, 99, 235);
  transform: translateY(-1px);
}

.submit-button:active:not(:disabled) {
  transform: translateY(1px);
}

.submit-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background-color: rgb(156, 163, 175);
}

@media (min-width: 768px) {
  .challenge-sections {
    flex-direction: row;
    align-items: flex-start;
    gap: 2rem;
  }

  .challenge-section {
    flex: 1;
    min-width: 0;
  }
}
</style>
