<template>
  <div>
    <ChallengeView
      :title="'Challenge #2: SQLi second order'"
      :introduction="'What is SQL injection?'"
      :shouldShowIntroduction="shouldShowIntroduction"
      :vulnerabilitySourceCode="{
        fileLink:
          'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/vulnerabilities/sqli_second_order.py',
        snippet: sqliSecondOrderVulnerableSnippet,
      }"
      :exploitSourceCode="{
        fileLink:
          'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/exploits/sqli_second_order.py',
        snippet: sqliSecondOrderExploitSnippet,
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
      <!-- Registration Form Section -->
      <section class="challenge-section">
        <h2 class="section-title">Register New Account</h2>
        <p class="challenge-description">
          Create a new account to try to exploit the change password functionality. You are going to
          try to change the password of the user <span class="code-block">batman</span>.
        </p>

        <div class="form-container">
          <AlertMessage v-if="registerState.error" :message="registerState.error" type="error" />
          <AlertMessage
            v-if="registerState.success"
            :message="registerState.success"
            type="success"
          />

          <form @submit.prevent="submitRegister" class="form">
            <div class="form-group">
              <label class="form-label" for="username">Username</label>
              <input
                v-model="registerForm.username"
                :disabled="registerState.isLoading"
                class="form-input"
                :class="{ 'input-error': registerFormErrors.username }"
                name="username"
                id="username"
                type="text"
                placeholder="Username"
                @blur="handleBlur('username', 'register')"
              />
              <p v-if="registerFormErrors.username" class="error-message">
                {{ registerFormErrors.username }}
              </p>
            </div>
            <div class="form-group">
              <label class="form-label" for="password">Password</label>
              <input
                v-model="registerForm.password"
                :disabled="registerState.isLoading"
                class="form-input"
                :class="{ 'input-error': registerFormErrors.password }"
                name="password"
                id="password"
                type="password"
                placeholder="******************"
                @blur="handleBlur('password', 'register')"
              />
              <p v-if="registerFormErrors.password" class="error-message">
                {{ registerFormErrors.password }}
              </p>
            </div>
            <div class="form-actions">
              <button
                :disabled="registerState.isLoading || !isRegisterFormValid"
                class="submit-button"
                type="submit"
              >
                <LoadingSpinner v-if="registerState.isLoading" />
                <span v-else>Register</span>
              </button>
            </div>
          </form>
        </div>
      </section>

      <!-- Change Password Section -->
      <section class="challenge-section">
        <h2 class="section-title">Change Password</h2>
        <p class="challenge-description">
          After registering, try to change the password of the user
          <span class="code-block">batman</span>. Can you find a way to bypass the verification of
          the current password?
        </p>

        <div class="form-container">
          <AlertMessage
            v-if="changePasswordState.error"
            :message="changePasswordState.error"
            type="error"
          />
          <AlertMessage
            v-if="changePasswordState.success"
            :message="changePasswordState.success"
            type="success"
          />

          <form @submit.prevent="submitChangePassword" class="form">
            <div class="form-group">
              <label class="form-label" for="old-password">Old Password</label>
              <input
                v-model="passwordForm.oldPassword"
                :disabled="changePasswordState.isLoading"
                class="form-input"
                :class="{ 'input-error': passwordFormErrors.oldPassword }"
                name="old-password"
                id="old-password"
                type="password"
                placeholder="Old Password"
                @blur="handleBlur('oldPassword', 'password')"
              />
              <p v-if="passwordFormErrors.oldPassword" class="error-message">
                {{ passwordFormErrors.oldPassword }}
              </p>
            </div>
            <div class="form-group">
              <label class="form-label" for="new-password">New Password</label>
              <input
                v-model="passwordForm.newPassword"
                :disabled="changePasswordState.isLoading"
                class="form-input"
                :class="{ 'input-error': passwordFormErrors.newPassword }"
                name="new-password"
                id="new-password"
                type="password"
                placeholder="New Password"
                @blur="handleBlur('newPassword', 'password')"
              />
              <p v-if="passwordFormErrors.newPassword" class="error-message">
                {{ passwordFormErrors.newPassword }}
              </p>
            </div>
            <div class="form-group">
              <label class="form-label" for="verify-password">Verify New Password</label>
              <input
                v-model="passwordForm.verifyPassword"
                :disabled="changePasswordState.isLoading"
                class="form-input"
                :class="{ 'input-error': passwordFormErrors.verifyPassword }"
                name="verify-password"
                id="verify-password"
                type="password"
                placeholder="Verify New Password"
                @blur="handleBlur('verifyPassword', 'password')"
              />
              <p v-if="passwordFormErrors.verifyPassword" class="error-message">
                {{ passwordFormErrors.verifyPassword }}
              </p>
            </div>
            <div class="form-actions">
              <button
                :disabled="changePasswordState.isLoading || !isPasswordFormValid"
                class="submit-button"
                type="submit"
              >
                <LoadingSpinner v-if="changePasswordState.isLoading" />
                <span v-else>Change Password</span>
              </button>
            </div>
          </form>
        </div>
      </section>

      <PassphraseSubmission challenge-id="sqli2" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/AlertMessage.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import SQLiIntroduction from '@/views/sqli/SQLiIntroduction.vue'
import SQLiNews from '@/views/sqli/SQLiNews.vue'
import ChallengeView from '@/views/ChallengeView.vue'
import { store } from '@/store'
import { sqliSecondOrderVulnerableSnippet } from '@/snippets'
import { sqliSecondOrderExploitSnippet } from '@/snippets'
import PassphraseSubmission from '@/components/PassphraseSubmission.vue'
import {
  SQLI_SECOND_ORDER_API_REGISTER_VULNERABLE_URL,
  SQLI_SECOND_ORDER_API_CHANGE_PASSWORD_VULNERABLE_URL,
} from '@/constants'

function determineIfShouldShowIntroduction() {
  const shouldShowIntroduction = !store.sqliIntroductionSeen
  store.sqliIntroductionSeen = true
  return shouldShowIntroduction
}
const shouldShowIntroduction = computed(determineIfShouldShowIntroduction)

// Register form state
const registerForm = ref({
  username: '',
  password: '',
})

const touchedFields = ref({
  register: {
    username: false,
    password: false,
  },
  password: {
    oldPassword: false,
    newPassword: false,
    verifyPassword: false,
  },
})

const registerFormErrors = computed(() => {
  const errors: Record<string, string> = {}
  if (!registerForm.value.username && touchedFields.value.register.username) {
    errors.username = 'Username is required'
  }
  if (!registerForm.value.password && touchedFields.value.register.password) {
    errors.password = 'Password is required'
  }
  return errors
})

const isRegisterFormValid = computed(() => {
  return (
    Object.keys(registerFormErrors.value).length === 0 &&
    registerForm.value.username.length > 0 &&
    registerForm.value.password.length > 0
  )
})

// Password change form state
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  verifyPassword: '',
})

const passwordFormErrors = computed(() => {
  const errors: Record<string, string> = {}
  if (!passwordForm.value.oldPassword && touchedFields.value.password.oldPassword) {
    errors.oldPassword = 'Old password is required'
  }
  if (!passwordForm.value.newPassword && touchedFields.value.password.newPassword) {
    errors.newPassword = 'New password is required'
  }
  if (touchedFields.value.password.verifyPassword) {
    if (!passwordForm.value.verifyPassword) {
      errors.verifyPassword = 'Password verification is required'
    } else if (passwordForm.value.newPassword !== passwordForm.value.verifyPassword) {
      errors.verifyPassword = 'Passwords do not match'
    }
  }
  return errors
})

const isPasswordFormValid = computed(() => {
  return (
    Object.keys(passwordFormErrors.value).length === 0 &&
    passwordForm.value.oldPassword.length > 0 &&
    passwordForm.value.newPassword.length > 0 &&
    passwordForm.value.verifyPassword.length > 0
  )
})

// API states
const { state: registerState, handleApiCall: handleRegister } = useApiState()
const { state: changePasswordState, handleApiCall: handleChangePassword } = useApiState()

const submitRegister = async () => {
  if (!isRegisterFormValid.value) return

  try {
    await handleRegister(async () => {
      const response = await fetch(SQLI_SECOND_ORDER_API_REGISTER_VULNERABLE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: registerForm.value.username,
          password: registerForm.value.password,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Registration failed')
      }

      return response.json()
    }, 'Registration successful!')

    // Clear form after successful registration
    registerForm.value = {
      username: '',
      password: '',
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

const submitChangePassword = async () => {
  if (!isPasswordFormValid.value) return

  try {
    await handleChangePassword(async () => {
      const response = await fetch(SQLI_SECOND_ORDER_API_CHANGE_PASSWORD_VULNERABLE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          old: passwordForm.value.oldPassword,
          new: passwordForm.value.newPassword,
          new_verify: passwordForm.value.verifyPassword,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Password change failed')
      }

      return response.json()
    }, 'Password changed successfully!')

    // Clear form after successful password change
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      verifyPassword: '',
    }
  } catch (error) {
    console.error('Error:', error)
  }
}
const handleBlur = (field: string, form: 'register' | 'password') => {
  if (form === 'register') {
    ;(touchedFields.value[form] as { username: boolean; password: boolean })[
      field as 'username' | 'password'
    ] = true
  } else {
    ;(
      touchedFields.value[form] as {
        oldPassword: boolean
        newPassword: boolean
        verifyPassword: boolean
      }
    )[field as 'oldPassword' | 'newPassword' | 'verifyPassword'] = true
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

.code-block {
  background-color: rgb(229, 231, 235);
  padding: 0.15rem;
  font-family: ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
}

.challenge-description {
  margin-bottom: 1.5rem;
  color: rgb(55, 65, 81);
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

.input-error {
  border-color: rgb(239, 68, 68);
}

.error-message {
  color: rgb(239, 68, 68);
  font-size: 0.75rem;
  margin-top: 0.25rem;
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

@media (min-width: 1024px) {
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
