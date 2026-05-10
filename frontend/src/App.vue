<script setup>
import { ref, onMounted } from 'vue'
import { getWebSettings } from "@/api/index.js"

const ready = ref(false)

onMounted(async () => {
  try {
    const response = await getWebSettings()
    localStorage.setItem("webInfo", JSON.stringify(response.data.data))
    ready.value = true
  } catch (error) {
    ready.value = true
  }
})
</script>

<template>
  <router-view v-if="ready" />
</template>
