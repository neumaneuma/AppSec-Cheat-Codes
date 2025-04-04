<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :title="'Solution #3: SSRF bypass webhook'"
    :previousChallengeLink="'/challenges/sqli2'"
    :nextChallengeLink="'/challenges/ssrf2'"
  >
    <template #solution>
      <SSRFGenericDefense />
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { ssrfWebhookPatchedSnippet } from '@/snippets'
import SSRFGenericDefense from './SSRFGenericDefense.vue'

const patchedSourceCode = {
  fileLink:
    'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/patches/ssrf_webhook.py',
  snippet: ssrfWebhookPatchedSnippet,
}
</script>
