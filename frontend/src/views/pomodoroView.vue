<script setup>
import { ref } from 'vue'
const longInterval = ref(3)
const sessions = ref(0)
const workDuration = ref(0.1)
const breakDuration = ref(0.05)
const longDuration = ref(0.1)
const timerRunning = ref(false)
const timeLeft = ref(0)
const isWorking = ref(false)
let timerInterval

const startTimer = () => {
  timerRunning.value = true
  isWorking.value = !isWorking.value
  console.log(isWorking.value)
  if (isWorking.value) {
    timeLeft.value = workDuration.value * 60
  } else if (sessions.value % longInterval.value == 0 && !isWorking.value) {
    timeLeft.value = longDuration.value * 60
  } else {
    timeLeft.value = breakDuration.value * 60
  }
  timerInterval = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value === 0) {
      clearInterval(timerInterval)
      startTimer()
    }
  }, 1000)
  if (isWorking.value) {
    sessions.value++
  }
}

const stopTimer = () => {
  clearInterval(timerInterval)
  timerRunning.value = false
}

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`
}
</script>

<template>
  <div class="pomodoro-timer">
    <h1>Pomodoro Timer</h1>
    <font-awesome-icon icon="fa-solid fa-gear" />
    <div v-if="!timerRunning">
      <label for="work-duration">Work Duration (minutes):</label>
      <input type="number" id="work-duration" v-model="workDuration" />
      <br />
      <label for="break-duration">Break Duration (minutes):</label>
      <input type="number" id="break-duration" v-model="breakDuration" />
      <br />
      <label for="long-duration">Long Break Duration (minutes):</label>
      <input type="number" id="long-duration" v-model="longDuration" />
      <br />
      <label for="longInterval">Long Break interval:</label>
      <input type="number" id="longInterval" v-model="longInterval" />
      <br />
      <button @click="startTimer">Start</button>
    </div>
    <div v-else>
      <p v-if="isWorking">Working for {{ formatTime(timeLeft) }}</p>
      <p v-else-if="!isWorking && sessions % longInterval == 0">
        Long break for {{ formatTime(timeLeft) }}
      </p>
      <p v-else>Break for {{ formatTime(timeLeft) }}</p>
      <button @click="stopTimer">Stop</button>
      <p>session number {{ sessions }}</p>
    </div>
  </div>
</template>
<style scoped>
.pomodoro-timer {
  text-align: center;
  margin-top: 50px;
}
</style>
