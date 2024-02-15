<script setup>
import { useStore } from '@/stores'
import { ref, watch } from 'vue'

const store = useStore()
const msg = ref('')
msg.value = 'welcome ' + store.user.id
watch(
  () => store.user.id,
  () => {
    msg.value = 'welcome ' + store.user.id
  }
)
</script>

<template>
  <div class="home">
    <h1>{{ msg }}</h1>
  </div>
</template>
