<script setup>
import { ref } from 'vue'
const longInterval = ref(3)
const sessions = ref(0)
const label = ref('')
const timerRunning = ref(false)
const timeLeft = ref(0)
const paused = ref(false)

const focus = ref({
  duration: 0.2,
  title: 'Focus'
})
const shortBreak = ref({
  duration: 0.05,
  title: 'Short Break'
})
const longBreak = ref({
  duration: 0.1,
  title: 'Long Break'
})

let timerInterval

const focusing = () => {
  timeLeft.value = focus.value.duration * 60
  label.value = focus.value.title
  sessions.value++
}
const shortresting = () => {
  timeLeft.value = shortBreak.value.duration * 60
  label.value = shortBreak.value.title
}
const longresting = () => {
  timeLeft.value = longBreak.value.duration * 60
  label.value = longBreak.value.title
}

const setNextStep = () => {
  if (label.value == shortBreak.value.title || label.value == longBreak.value.title) {
    //setnotification("Rest", "focus");
    focusing()
  } else if (label.value == focus.value.title && sessions.value % longInterval.value == 0) {
    //setnotification("Focus", "take a long rest");
    longresting()
  } else if (label.value == focus.value.title) {
    //setnotification("Focus", "take a short rest");
    shortresting()
  } else {
    focusing()
  }
}

const startTimer = () => {
  timerRunning.value = true
  setNextStep()
  timerInterval = setInterval(() => {
    if (!paused.value) {
      timeLeft.value--
    }
    if (timeLeft.value === 0) {
      clearInterval(timerInterval)
      startTimer()
    }
  }, 1000)
}

const stopTimer = () => {
  clearInterval(timerInterval)
  timerRunning.value = false
  sessions.value = 1
  label.value = ''
}

const togglePause = () => {
  paused.value = !paused.value
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
      <label for="work-duration">Focus Duration (minutes):</label>
      <input type="number" id="work-duration" v-model="focus.duration" />
      <br />
      <label for="break-duration">Break Duration (minutes):</label>
      <input type="number" id="break-duration" v-model="shortBreak.duration" />
      <br />
      <label for="long-duration">Long Break Duration (minutes):</label>
      <input type="number" id="long-duration" v-model="longBreak.duration" />
      <br />
      <label for="longInterval">Long Break interval:</label>
      <input type="number" id="longInterval" v-model="longInterval" />
      <br />
      <button @click="startTimer">Start</button>
    </div>
    <div v-else>
      <div>
        <button @click="focusing">Focus</button>
        <button @click="shortresting">Short Break</button>
        <button @click="longresting">Long Break</button>
      </div>
      <p>{{ label }} {{ formatTime(timeLeft) }}</p>
      <div class="actions">
        <button @click="togglePause">
          <font-awesome-icon v-if="!paused" icon="fa-solid fa-pause" />
          <font-awesome-icon v-else icon="fa-solid fa-forward-step" />
        </button>
        <button @click="stopTimer">stop</button>
      </div>
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
