<template>
  <div class="home">
    <HelloWorld :msg="msg" />
  </div>
</template>

<script setup>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import { useStore } from '@/stores'
const store = useStore()
const msg = 'welcome ' + store.user.id
</script>
