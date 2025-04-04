<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="banner">
    <nav class="nav-container">
      <div class="left-nav">
        <RouterLink to="/" class="nav-link large-font">AppSec Cheat Codes</RouterLink>
      </div>
      <div class="right-nav">
        <RouterLink to="/about" class="nav-link">About</RouterLink>
        <a href="https://github.com/neumaneuma/AppSec-Cheat-Codes" class="nav-link">GitHub</a>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
.banner {
  background-color: #ffffff;
  padding: 10px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%; /* Ensure the banner takes the full width */
  position: fixed; /* Optional: Fix the banner to the top */
  top: 0;
  left: 0;
  z-index: 1000; /* Ensure it stays on top of other elements */
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 60%;
  margin: 0 auto;
  padding: 0 20px;
}

.left-nav {
  flex: 1;
}

.right-nav {
  display: flex;
  gap: 20px;
}

.large-font {
  font-size: 24px;
  font-weight: bold;
}

.nav-link {
  color: #3d474b;
  text-decoration: none;
  font-size: 18px;
  padding: 8px 12px;
  border-radius: 4px;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.nav-link:hover {
  background-color: #bfdbfe;
  color: #1d4ed8;
}

@media (max-width: 768px) {
  .nav-container {
    width: 90%;
    padding: 0 10px;
  }

  .nav-link {
    font-size: 16px;
    padding: 6px 10px;
  }

  .large-font {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .nav-link {
    font-size: 14px;
    padding: 4px 8px;
  }

  .large-font {
    font-size: 18px;
  }

  .right-nav {
    gap: 10px;
  }
}

@media (max-width: 400px) {
  .nav-container {
    flex-direction: column;
  }

  .nav-link {
    font-size: 12px;
  }

  .large-font {
    font-size: 15px;
  }
}
</style>
