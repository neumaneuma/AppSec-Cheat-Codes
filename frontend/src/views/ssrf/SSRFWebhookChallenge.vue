<template>
  <div>
    <ChallengeView
      :title="'Challenge #3: SSRF bypass webhook'"
      :introduction="'What is SSRF?'"
      :shouldShowIntroduction="shouldShowIntroduction"
      :vulnerabilitySourceCode="{
        fileLink:
          'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/vulnerabilities/ssrf_webhook.py',
        snippet: ssrfWebhookVulnerableSnippet,
      }"
      :exploitSourceCode="{
        fileLink:
          'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/exploits/ssrf_webhook.py',
        snippet: ssrfWebhookExploitSnippet,
      }"
    >
      <template #introduction>
        <SSRFIntroduction />
      </template>
      <template #news>
        <SSRFNews />
      </template>
    </ChallengeView>

    <div class="challenge-sections">
      <!-- Webhook Form Section -->
      <section class="challenge-section">
        <h2 class="section-title">Webhook Challenge</h2>
        <p class="challenge-description">
          This web server has a functionality built for webhooks. However, you can abuse this
          functionality to access an internal admin API. The only thing you know is that the
          internal API can be accessed through
          <span class="code-block">http://internal_api</span>
        </p>

        <div class="form-container">
          <AlertMessage v-if="apiState.error" :message="apiState.error" type="error" />
          <AlertMessage v-if="apiState.success" :message="apiState.success" type="success" />

          <form @submit.prevent="submitWebhook" class="form">
            <div class="form-group">
              <label class="form-label" for="custom_url">
                Enter the URL to use for the webhook:
              </label>
              <input
                v-model="customUrl"
                :disabled="apiState.isLoading"
                class="form-input"
                name="custom_url"
                id="custom_url"
                type="text"
                placeholder="http://example.com/webhook"
              />
            </div>
            <div class="form-actions">
              <button :disabled="apiState.isLoading" class="submit-button" type="submit">
                <LoadingSpinner v-if="apiState.isLoading" />
                <span v-else>Submit</span>
              </button>
            </div>
          </form>

          <!-- Response Display -->
          <div v-if="webhookResponse" class="response-container">
            <h3 class="response-title">Response:</h3>
            <pre class="response-content">{{ webhookResponse }}</pre>
          </div>
        </div>
      </section>

      <PassphraseSubmission challenge-id="ssrf1" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/AlertMessage.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import SSRFIntroduction from '@/views/ssrf/SSRFIntroduction.vue'
import SSRFNews from '@/views/ssrf/SSRFNews.vue'
import ChallengeView from '@/views/ChallengeView.vue'
import { store } from '@/store'
import { ssrfWebhookVulnerableSnippet } from '@/snippets'
import { ssrfWebhookExploitSnippet } from '@/snippets'
import PassphraseSubmission from '@/components/PassphraseSubmission.vue'
import { SSRF_WEBHOOK_API_VULNERABLE_URL } from '@/constants'

const customUrl = ref('')
const webhookResponse = ref('')
const { state: apiState, handleApiCall } = useApiState()

function determineIfShouldShowIntroduction() {
  const shouldShowIntroduction = !store.ssrfIntroductionSeen
  store.ssrfIntroductionSeen = true
  return shouldShowIntroduction
}
const shouldShowIntroduction = computed(determineIfShouldShowIntroduction)

const submitWebhook = async () => {
  try {
    const result = await handleApiCall(async () => {
      const response = await fetch(SSRF_WEBHOOK_API_VULNERABLE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: customUrl.value }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Webhook submission failed')
      }

      return response.text()
    }, 'Webhook submitted successfully!')

    webhookResponse.value = result
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>

<style scoped>
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

.challenge-description {
  margin-bottom: 1.5rem;
  color: rgb(55, 65, 81);
}

.code-block {
  background-color: rgb(229, 231, 235);
  padding: 0.15rem;
  font-family: ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
}

.form-container {
  width: 100%;
  margin-top: 1.5rem;
}

.form {
  background-color: rgb(249, 250, 251);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid rgb(229, 231, 235);
  width: 100%;
  box-sizing: border-box;
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

.response-container {
  margin-top: 1rem;
  padding: 1rem;
  background-color: rgb(243, 244, 246);
  border-radius: 0.375rem;
}

.response-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.response-content {
  white-space: pre-wrap;
  font-size: 0.875rem;
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
