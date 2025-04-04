<template>
  <div>
    <ChallengeView
      :title="'Challenge #4: SSRF local file inclusion'"
      :introduction="'What is SSRF?'"
      :shouldShowIntroduction="shouldShowIntroduction"
      :vulnerabilitySourceCode="{
        fileLink:
          'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/vulnerabilities/ssrf_lfi.py',
        snippet: ssrfLocalFileInclusionVulnerableSnippet,
      }"
      :exploitSourceCode="{
        fileLink: 'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/exploits/ssrf_lfi.py',
        snippet: ssrfLocalFileInclusionExploitSnippet,
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
      <!-- API Selection Section -->
      <section class="challenge-section">
        <h2 class="section-title">API Selection Challenge</h2>
        <p class="challenge-description">
          Catcoin is the hot new crypto currency that everyone is talking about. The following form
          is for a financial web app that will allow you to pick the API that is used to query the
          current price of catcoin.
        </p>

        <p class="instruction-text">
          Solve this challenge by stealing the
          <code class="code-block">file:///etc/shadow</code> or
          <code class="code-block">file:///etc/passwd</code> files.
        </p>

        <div class="form-container">
          <AlertMessage v-if="apiState.error" :message="apiState.error" type="error" />
          <AlertMessage v-if="apiState.success" :message="apiState.success" type="success" />

          <form @submit.prevent="submitUrl" class="form">
            <div class="form-group">
              <label class="form-label" for="api_url">API Selection</label>
              <div class="radio-group">
                <div v-for="(url, index) in predefinedUrls" :key="index" class="radio-option">
                  <input
                    type="radio"
                    :id="'url-' + index"
                    v-model="selectedUrl"
                    :value="url"
                    class="radio-input"
                    :disabled="apiState.isLoading"
                  />
                  <label :for="'url-' + index" class="code-block radio-label">{{ url }}</label>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button
                :disabled="apiState.isLoading || !isValidUrl"
                class="submit-button"
                type="submit"
              >
                <LoadingSpinner v-if="apiState.isLoading" />
                <span v-else>Get Price</span>
              </button>
            </div>
          </form>

          <!-- Response Display -->
          <div v-if="apiResponse" class="response-container">
            <h3 class="response-title">Response:</h3>
            <pre class="response-content">{{ apiResponse }}</pre>
          </div>
        </div>
      </section>

      <PassphraseSubmission challenge-id="ssrf2" />
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
import PassphraseSubmission from '@/components/PassphraseSubmission.vue'
import { store } from '@/store'
import { ssrfLocalFileInclusionVulnerableSnippet } from '@/snippets'
import { ssrfLocalFileInclusionExploitSnippet } from '@/snippets'
import { SSRF_LOCAL_FILE_API_VULNERABLE_URL } from '@/constants'

const predefinedUrls = [
  'http://internal_api:12302/get_cat_coin_price_v1/',
  'http://internal_api:12302/get_cat_coin_price_v2/',
]

const selectedUrl = ref(predefinedUrls[0])
const customUrl = ref('')
const apiResponse = ref('')
const { state: apiState, handleApiCall } = useApiState()

function determineIfShouldShowIntroduction() {
  const shouldShowIntroduction = !store.ssrfIntroductionSeen
  store.ssrfIntroductionSeen = true
  return shouldShowIntroduction
}
const shouldShowIntroduction = computed(determineIfShouldShowIntroduction)

const isValidUrl = computed(() => {
  if (selectedUrl.value === 'custom') {
    return customUrl.value.trim().length > 0
  }
  return true
})

const getEffectiveUrl = () => {
  return selectedUrl.value === 'custom' ? customUrl.value : selectedUrl.value
}

const submitUrl = async () => {
  try {
    const result = await handleApiCall(async () => {
      const response = await fetch(SSRF_LOCAL_FILE_API_VULNERABLE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: getEffectiveUrl() }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'URL submission failed')
      }

      return response.text()
    }, 'Request successful!')

    apiResponse.value = result
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

.api-urls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1rem 0;
}

.code-block {
  background-color: rgb(229, 231, 235);
  padding: 0.15rem;
  font-family: ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
}

.instruction-text {
  margin: 1rem 0;
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

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.radio-input {
  margin: 0;
}

.radio-label {
  font-size: 12px;
  font-weight: 800;
  word-break: break-all;
  white-space: normal;
  max-width: 100%;
}

.form-label {
  display: block;
  color: rgb(55, 65, 81);
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
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

@media (max-width: 480px) {
  .radio-option {
    flex-wrap: wrap;
    gap: 0.25rem;
  }

  .radio-label {
    font-size: 11px;
  }
}
</style>
