<script>
import { getWebSettings } from "@/api/index.js"

(async () => {
  const response = await getWebSettings()
  localStorage.setItem("webInfo", JSON.stringify(response.data.data))
})()

</script>



<template>
  <router-view />
</template>
