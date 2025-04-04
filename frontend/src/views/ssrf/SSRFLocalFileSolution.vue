<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :title="'Solution #4: SSRF local file inclusion'"
    :previousChallengeLink="'/challenges/ssrf1'"
  >
    <template #solution>
      <SSRFGenericDefense />
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { ssrfLocalFileInclusionPatchedSnippet } from '@/snippets'
import SSRFGenericDefense from './SSRFGenericDefense.vue'

const patchedSourceCode = {
  fileLink:
    'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/patches/ssrf_local_file_inclusion.py',
  snippet: ssrfLocalFileInclusionPatchedSnippet,
}
</script>
