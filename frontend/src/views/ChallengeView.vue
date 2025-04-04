<template>
  <div class="challenge-container">
    <div class="challenge-header">
      <h2 class="page-title">{{ title }}</h2>

      <!-- First Hint -->
      <div class="hint-container meta-hint">
        <div class="hint-header collapsible" @click="toggleFirstHint">
          <div class="hint-title">
            <h3 class="hint-text">How should I approach this?</h3>
          </div>
          <div class="hint-icons">
            <span class="plus" :class="{ hidden: isFirstHintOpen }">+</span>
            <span class="minus" :class="{ hidden: !isFirstHintOpen }">-</span>
          </div>
        </div>
        <div class="collapsible-content" ref="firstHintContent">
          <div class="content-wrapper">
            <p>
              This is a
              <a
                href="https://dev.to/atan/what-is-ctf-and-how-to-get-started-3f04"
                target="_blank"
                rel="noopener"
                class="link"
                >capture the flag (CTF)</a
              >
              webapp designed to teach software developers the fundamentals of
              <a
                href="https://en.wikipedia.org/wiki/Application_security"
                target="_blank"
                rel="noopener"
                class="link"
                >application security (AppSec)</a
              >. Software developers learn best when reading and writing code. Most CTFs are
              primarily focused on learning how to exploit the vulnerabilities, as opposed to
              learning how to write secure code that is free of vulnerabilities. Think of this site
              as a code-first CTF. It attempts to reframe the concept of AppSec in terms of code.
            </p>

            <p>
              There are 3 hints for every challenge. One hint will show you
              <span class="emphasis"
                >the exact code of the server-side vulnerability that you are trying to
                exploit</span
              >. Being able to read the code (and even modify it if you are running the webapp
              locally) is how we can translate the abstract concept of a vulnerability into
              something tangible. Another hint will show you
              <span class="emphasis">the exact code of the exploit and how to run it</span>.
              Technically this is less of a hint and more just the answer to how to solve the
              challenge, but let's not get too hung up on semantics.
            </p>

            <p>
              The next logical step is to provide the diff between what the vulnerable code looks
              like and what the secure code looks like. This is accessible to anyone who solves the
              challenge, which considering the exploit is provided if you cannot figure out how to
              write it on your own, is literally anyone.
            </p>

            <p>
              And finally, as if this wall of text wasn't long enough, there is even more to it. If
              you want to run the webapp locally just follow the instructions on this
              <a
                href="https://github.com/neumaneuma/AppSec-Cheat-Codes/main/README.md"
                target="_blank"
                rel="noopener"
                class="link"
                >README</a
              >. Make any modifications you want. Add code, remove code, break things, figure out
              how to fix them. This is what I believe to be the most effective way for a developer
              to learn a concept: through code.
            </p>
          </div>
        </div>
      </div>

      <p v-if="!toggleIntroduction">
        <a class="intro-link" @click="toggleIntroduction = true">Click here</a> to view challenge
        background again.
      </p>
    </div>

    <template v-if="toggleIntroduction">
      <div class="section">
        <h3 class="section-title">{{ introduction }}</h3>
        <slot name="introduction"></slot>
      </div>
      <div class="section">
        <h3 class="section-title">Heard about it in the news?</h3>
        <slot name="news"></slot>
      </div>
    </template>

    <div class="section">
      <h3 class="section-title">Challenge</h3>

      <!-- Second Hint -->
      <div class="hint-container generic-hint">
        <div class="hint-header collapsible" @click="toggleSecondHint">
          <div class="hint-title">
            <h3 class="hint-text">Hint #1: <span class="hint-description">Generic Hint</span></h3>
          </div>
          <div class="hint-icons">
            <span class="plus" :class="{ hidden: isSecondHintOpen }">+</span>
            <span class="minus" :class="{ hidden: !isSecondHintOpen }">-</span>
          </div>
        </div>
        <div class="collapsible-content" ref="secondHintContent">
          <div class="content-wrapper">
            <p>If you are unsure on how to proceed, then the following may help:</p>

            <p>
              Most of the vulnerabilities in this CTF can be manually exploited simply through your
              browser. Alternatively, you can use a dedicated web security tool such as
              <a href="https://caido.io" target="_blank" rel="noopener" class="link">Caido</a>,
              <a href="https://portswigger.net/burp" target="_blank" rel="noopener" class="link"
                >Burp Suite</a
              >, or
              <a href="https://www.zaproxy.org" target="_blank" rel="noopener" class="link"
                >OWASP ZAP</a
              >. However, the focus of this CTF is on the code side of application security. Every
              challenge's exploit code is available as the third hint. You are encouraged to attempt
              to write the exploit code yourself before looking at the answer.
            </p>

            <p>
              In order to do this, you need to understand what fields are being set in the HTTP
              request being sent to the server from the browser. Think of this as the "anatomy" of
              the request. This is so that you can craft your own HTTP request from the script you
              write. You can use your
              <a
                href="https://www.twilio.com/blog/2017/09/everything-you-ever-wanted-to-know-about-secure.html-forms.html"
                target="_blank"
                rel="noopener"
                class="link"
                >browser's developer tools</a
              >
              to figure out this information, or you can use a tool that can decrypt encrypted
              traffic on your computer. All 3 of the aforementioned tools offer this feature.
              There's also
              <a href="https://mitmproxy.org" target="_blank" rel="noopener" class="link"
                >mitmproxy</a
              >
              if you want a tool dedicated to this purpose.
            </p>
          </div>
        </div>
      </div>

      <!-- Third Hint -->
      <div class="hint-container vulnerability-hint">
        <div class="hint-header collapsible" @click="toggleVulnerabilityHint">
          <div class="hint-title">
            <h3 class="hint-text">
              Hint #2:
              <span class="hint-description"
                >What does the server-side vulnerability look like?</span
              >
            </h3>
          </div>
          <div class="hint-icons">
            <span class="plus" :class="{ hidden: isVulnerabilityHintOpen }">+</span>
            <span class="minus" :class="{ hidden: !isVulnerabilityHintOpen }">-</span>
          </div>
        </div>
        <div class="collapsible-content" ref="vulnerabilityHintContent">
          <p>
            File truncated for brevity.
            <a :href="vulnerabilitySourceCode.fileLink" class="exploit-link" target="_blank"
              >Click here</a
            >
            to view full file.
          </p>
          <CodeSnippet :code="vulnerabilitySourceCode.snippet" :language="'python'" />
        </div>
      </div>

      <!-- Fourth Hint -->
      <div class="hint-container exploit-hint">
        <div class="hint-header collapsible" @click="toggleExploitHint">
          <div class="hint-title">
            <h3 class="hint-text">
              Hint #3:
              <span class="hint-description"
                >Couldn't figure out the answer? Here is the exploit</span
              >
            </h3>
          </div>
          <div class="hint-icons">
            <span class="plus" :class="{ hidden: isExploitHintOpen }">+</span>
            <span class="minus" :class="{ hidden: !isExploitHintOpen }">-</span>
          </div>
        </div>
        <div class="collapsible-content" ref="exploitHintContent">
          <p class="exploit-text">
            View the
            <a
              href="https://github.com/neumaneuma/AppSec-Cheat-Codes/main/exploits/README.md"
              target="_blank"
              rel="noopener"
              class="exploit-link"
              >exploit README</a
            >
            to run the exploits locally.
          </p>
          <p>
            File truncated for brevity.
            <a :href="exploitSourceCode.fileLink" class="exploit-link" target="_blank"
              >Click here</a
            >
            to view full file.
          </p>
          <CodeSnippet :code="exploitSourceCode.snippet" :language="'python'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, type Ref } from 'vue'
import CodeSnippet from '@/components/CodeSnippet.vue'

type SourceCodeLinks = {
  fileLink: string
  snippet: string
}

interface Props {
  title: string
  introduction: string
  shouldShowIntroduction: boolean
  vulnerabilitySourceCode: SourceCodeLinks
  exploitSourceCode: SourceCodeLinks
}

const props = defineProps<Props>()

// Initialize toggleIntroduction with the prop value
const toggleIntroduction = ref(props.shouldShowIntroduction)

// Watch for changes to the prop and update the internal state
watch(
  () => props.shouldShowIntroduction,
  (newValue) => {
    toggleIntroduction.value = newValue
  },
)

// Hint states and refs
const isFirstHintOpen = ref(false)
const isSecondHintOpen = ref(false)
const isVulnerabilityHintOpen = ref(false)
const isExploitHintOpen = ref(false)

const firstHintContent = ref<HTMLElement | null>(null)
const secondHintContent = ref<HTMLElement | null>(null)
const vulnerabilityHintContent = ref<HTMLElement | null>(null)
const exploitHintContent = ref<HTMLElement | null>(null)

// Toggle functions
const toggleCollapsible = (isOpen: Ref<boolean>, content: Ref<HTMLElement | null>) => {
  isOpen.value = !isOpen.value

  if (content.value) {
    if (content.value.style.maxHeight) {
      content.value.style.maxHeight = ''
    } else {
      content.value.style.maxHeight = `${content.value.scrollHeight}px`
    }
  }
}

const toggleFirstHint = () => toggleCollapsible(isFirstHintOpen, firstHintContent)
const toggleSecondHint = () => toggleCollapsible(isSecondHintOpen, secondHintContent)
const toggleVulnerabilityHint = () =>
  toggleCollapsible(isVulnerabilityHintOpen, vulnerabilityHintContent)
const toggleExploitHint = () => toggleCollapsible(isExploitHintOpen, exploitHintContent)
</script>

<style scoped>
.challenge-container {
  padding: 4rem 2rem;
  max-width: 64rem;
  margin: 0 auto;
  color: rgb(75, 85, 99);
}

.challenge-header {
  padding-top: 1rem;
}

.page-title {
  margin-top: 1.5rem;
  font-size: 2.25rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.intro-link {
  color: rgb(96, 165, 250);
  text-decoration: none;
}

.intro-link:hover {
  text-decoration: underline;
}

.section {
  padding-top: 1rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: rgb(17, 24, 39);
  margin-bottom: 1rem;
}

.hint-container {
  border-width: 1px;
  border: 1px solid rgb(17, 24, 39);
  border-radius: 0.375rem;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.hint-container.vulnerability-hint {
  border-color: rgb(127, 29, 29);
}

.hint-container.exploit-hint {
  border-color: rgb(20, 83, 45);
}

.hint-header {
  display: grid;
  grid-template-columns: 2fr 1fr;
  min-height: 1rem;
  cursor: pointer;
  border-radius: 0.375rem;
  padding: 0.5rem 0;
}

.vulnerability-hint .hint-header {
  background-color: rgb(254, 202, 202);
}

.vulnerability-hint .hint-header:hover {
  background-color: rgb(252, 165, 165);
}

.exploit-hint .hint-header {
  background-color: rgb(187, 247, 208);
}

.exploit-hint .hint-header:hover {
  background-color: rgb(134, 239, 172);
}

.hint-title {
  display: flex;
  align-items: center;
  padding-left: 1rem;
}

.hint-text {
  font-size: 1rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.vulnerability-hint .hint-description {
  color: rgb(185, 28, 28);
}

.vulnerability-hint .hint-description:hover {
  color: rgb(153, 27, 27);
}

.exploit-hint .hint-description {
  color: rgb(22, 163, 74);
}

.exploit-hint .hint-description:hover {
  color: rgb(21, 128, 61);
}

.hint-icons {
  display: flex;
  align-items: center;
  justify-content: right;
  padding-right: 1.5rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.hidden {
  display: none;
}

.collapsible-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
  padding: 0 1rem;
}

.exploit-text {
  margin-top: 1rem;
}

.exploit-link {
  color: rgb(96, 165, 250);
  text-decoration: none;
}

.exploit-link:hover {
  text-decoration: underline;
}

.meta-hint .hint-header {
  background-color: rgb(203, 205, 209);
}

.meta-hint .hint-header:hover {
  background-color: rgb(173, 176, 182);
}

.hint-container.generic-hint {
  border: 1px solid rgb(120, 113, 108);
}

.generic-hint .hint-header {
  background-color: rgb(254, 240, 138);
}

.generic-hint .hint-header:hover {
  background-color: rgb(253, 224, 71);
}

.generic-hint .hint-description {
  color: rgb(161, 98, 7);
}

.generic-hint .hint-description:hover {
  color: rgb(133, 77, 14);
}

.content-wrapper {
  display: flex;
  flex-direction: column;
}

.link {
  color: rgb(96, 165, 250);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.emphasis {
  font-style: italic;
}
</style>
