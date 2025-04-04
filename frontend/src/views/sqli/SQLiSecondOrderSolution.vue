<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :title="'Solution #2: SQLi second order'"
    :previousChallengeLink="'/challenges/sqli2'"
    :nextChallengeLink="'/challenges/ssrf1'"
  >
    <template #solution>
      <SQLiGenericDefense />
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { sqliSecondOrderPatchedSnippet } from '@/snippets'
import SQLiGenericDefense from './SQLiGenericDefense.vue'

const patchedSourceCode = {
  fileLink:
    'https://github.com/neumaneuma/AppSec-Cheat-Codes/blob/main/backend/patches/sqli_second_order.py',
  snippet: sqliSecondOrderPatchedSnippet,
}
</script>
