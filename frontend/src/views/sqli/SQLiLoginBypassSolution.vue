<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :title="'Solution #1: SQLi login bypass'"
    :nextChallengeLink="'/challenges/sqli2'"
  >
    <template #solution>
      <SQLiGenericDefense />
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { sqliLoginBypassPatchedSnippet } from '@/snippets'
import SQLiGenericDefense from './SQLiGenericDefense.vue'

const patchedSourceCode = {
  fileLink:
    'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/patches/sqli_login_bypass.py',
  snippet: sqliLoginBypassPatchedSnippet,
}
</script>
