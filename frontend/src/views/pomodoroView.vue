<template>
  <div class="pomodoro">
    <div v-if="!isRunning">
      <label>Focus Duration (minutes):</label>
      <input type="number" v-model="focusDuration" min="1" max="60" />
      <label>Break Duration (minutes):</label>
      <input type="number" v-model="breakDuration" min="1" max="60" />
      <label>Sessions before Long Break:</label>
      <input type="number" v-model="sessionsBeforeLongBreak" min="1" />
      <label>Long Break Duration (minutes):</label>
      <input type="number" v-model="longBreakDuration" min="1" max="60" />
      <button @click="startTimer">Start</button>
    </div>
    <div v-else>
      <h1>{{ currentSessionType }}</h1>
      <h2>{{ formattedTime }}</h2>
      <button @click="stopTimer">Stop</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const focusDuration = ref(25)
const breakDuration = ref(5)
const sessionsBeforeLongBreak = ref(4)
const longBreakDuration = ref(15)
const isRunning = ref(false)
const currentSessionType = ref('Focus')
const totalTime = computed(() => {
  if (currentSessionType.value === 'Focus') {
    return focusDuration.value * 60
  } else if (currentSessionType.value === 'Break') {
    return breakDuration.value * 60
  } else {
    return longBreakDuration.value * 60
  }
})
const formattedTime = computed(() => {
  const minutes = Math.floor(totalTime.value / 60)
  const seconds = totalTime.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

let timer

const startTimer = () => {
  isRunning.value = true
  timer = setInterval(() => {
    if (totalTime.value > 0) {
      totalTime.value--
    } else {
      clearInterval(timer)
      if (currentSessionType.value === 'Focus') {
        currentSessionType.value = 'Break'
      } else if (currentSessionType.value === 'Break') {
        currentSessionType.value = 'Focus'
      }
      isRunning.value = false
    }
  }, 1000)
}

const stopTimer = () => {
  clearInterval(timer)
  isRunning.value = false
}
</script>

<style scoped>
.pomodoro {
  text-align: center;
}
</style>
