<script setup lang="ts">
import Button from "primevue/button"
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <Button :label="`You clicked me ${count} times`" @click="count++" class="mt-4" ></Button>
</template>
