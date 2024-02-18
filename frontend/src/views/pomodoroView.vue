<script setup>
import axios from 'axios'
import endaudio from '@/assets/pomodoro.mp3'
import { ref, onMounted, onUnmounted } from 'vue'
const longInterval = ref(4)
const sessions = ref(0)
const label = ref('')
const settings = ref(false)
const timeLeft = ref(0)
let notification = null
const audio = new Audio(endaudio)
const paused = ref(true)
const activeButton = ref(0)
const focus = ref({
  duration: 25,
  title: 'Focus'
})
const shortBreak = ref({
  duration: 5,
  title: 'Short Break'
})
const longBreak = ref({
  duration: 15,
  title: 'Long Break'
})

let timerInterval

const focusing = () => {
  activeButton.value = 0
  timeLeft.value = focus.value.duration * 60
  label.value = focus.value.title
  sessions.value++
}
const shortresting = () => {
  activeButton.value = 1
  timeLeft.value = shortBreak.value.duration * 60
  label.value = shortBreak.value.title
}
const longresting = () => {
  activeButton.value = 2
  timeLeft.value = longBreak.value.duration * 60
  label.value = longBreak.value.title
}

const setNextStep = () => {
  if (label.value == shortBreak.value.title || label.value == longBreak.value.title) {
    setnotification('Rest', 'focus')
    focusing()
  } else if (label.value == focus.value.title && sessions.value % longInterval.value == 0) {
    setnotification('Focus', 'take a long rest')
    longresting()
  } else if (label.value == focus.value.title) {
    setnotification('Focus', 'take a short rest')
    shortresting()
  } else {
    focusing()
  }
}

const startTimer = () => {
  setNextStep()
  timerInterval = setInterval(() => {
    if (!paused.value) {
      timeLeft.value--
    }
    if (timeLeft.value === 0) {
      clearInterval(timerInterval)
      if (label.value === 'Focus') {
        axios
          .post(`/api/users/${localStorage.getItem('userId')}/pomodoros/`, {
            minutes: focus.value.duration
          })
          .then((response) => {
            console.log(response.data)
          })
          .catch((error) => {
            console.error(error)
          })
      }
      startTimer()
      audio.play()
    }
  }, 1000)
}

const stopTimer = () => {
  clearInterval(timerInterval)
  sessions.value = 0
  timeLeft.value = ''
  label.value = ''
  paused.value = true
  startTimer()
}

const togglePause = () => {
  paused.value = !paused.value
}

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes < 10 ? '0' : ''}${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`
}

const togglesettings = (event) => {
  event.stopPropagation()
  settings.value = !settings.value
  if (settings.value) {
    window.addEventListener('click', closesettings)
  } else {
    window.removeEventListener('click', closesettings)
  }
}

const closesettings = (event) => {
  if (settings.value) {
    if (!document.querySelector('.settings').contains(event.target)) {
      settings.value = false
      window.removeEventListener('click', closesettings)
    }
  }
}
const setnotification = (done, next) => {
  notification = new Notification('Pomodoro', {
    body: `${done} session is over it's time to ${next}`
  })
  notification.onclick = () => {
    window.focus()
  }
}
onMounted(() => {
  startTimer()
  window.addEventListener('click', closesettings)
})
onUnmounted(() => {
  window.removeEventListener('click', closesettings)
})
</script>

<template>
  <div class="pomodoro-timer">
    <h4>Pomodoro Timer</h4>
    <font-awesome-icon icon="fa-solid fa-gear" class="gear" @click="togglesettings" />
    <div v-if="settings" class="settings">
      <h3><font-awesome-icon icon="fa-regular fa-clock" /> Timer (minutes)</h3>
      <div class="time">
        <div>
          <label for="work-duration">Focus</label>
          <input type="number" id="work-duration" v-model="focus.duration" @change="stopTimer" />
        </div>
        <div>
          <label for="break-duration">Break</label>
          <input
            type="number"
            id="break-duration"
            v-model="shortBreak.duration"
            @change="stopTimer"
          />
        </div>
        <div>
          <label for="long-duration">Long Break</label>
          <input
            type="number"
            id="long-duration"
            v-model="longBreak.duration"
            @change="stopTimer"
          />
        </div>
      </div>
      <div class="interval">
        <label for="longInterval">Long Break interval</label>
        <input type="number" id="longInterval" v-model="longInterval" @change="stopTimer" />
      </div>
    </div>
    <div class="timer">
      <div class="sessions">
        <button :class="{ active: activeButton === 0 }" @click="focusing">Pomodoro</button>
        <button :class="{ active: activeButton === 1 }" @click="shortresting">Short Break</button>
        <button :class="{ active: activeButton === 2 }" @click="longresting">Long Break</button>
      </div>

      <div class="time">{{ formatTime(timeLeft) }}</div>
      <div class="actions">
        <button @click="togglePause" class="pause">
          <font-awesome-icon v-if="!paused" icon="fa-solid fa-pause" />
          <font-awesome-icon v-else icon="fa-solid fa-forward-step" />
        </button>
        <button @click="stopTimer" class="stop">stop</button>
      </div>
      <p>session number {{ sessions }}</p>
    </div>
  </div>
</template>

<style lang="scss">
.pomodoro-timer {
  margin: 10px auto;
  position: relative;
  max-width: 650px;
  border: 2px solid rgba(255, 255, 255, 0.031372549);
  border-radius: 8px;
  padding: 7px;
  margin-top: 50px;
  * {
    transition: all 0.2s ease-in-out;
  }
  h4 {
    font-size: 17px;
    padding: 15px;
    color: #ffffff54;
  }
  .gear {
    position: absolute;
    top: 15px;
    padding: 5px;
    right: 15px;
    font-size: 23px;
    color: #ffffffc9;
    &:hover {
      color: white;
    }
  }
}
.settings {
  position: fixed;
  display: flex;
  flex-direction: column;
  top: 50%;
  left: 50%;
  width: 400px;
  max-width: calc(100% - 10px);
  transform: translate(-50%, -50%);
  border-radius: 10px;
  padding: 20px;
  background-color: #06061c;
  border: 1px solid #8269ac;
  box-shadow: 0px 2px 10px 2px #03030e41;
  z-index: 10;
  input {
    border-radius: 4px;
    background-color: #121231;
    color: white;
    width: 100%;
    padding: 5px;
    font-size: 20px;
    border: 1px solid transparent;
    &:focus-visible {
      outline: none;
      border: 1px solid #ffffff5e;
    }
  }
  h3 {
    margin: 15px 0;
    color: #ffffffa6;
  }
  .time {
    display: flex;
    flex-direction: row;
    gap: 12px;
    align-items: flex-end;
    justify-content: center;
    flex-wrap: nowrap;
    margin: 0 0 20px 0;
  }
  .interval {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;

    input {
      max-width: 80px;
      margin-left: 5px;
    }
  }
}
.timer {
  text-align: center;
  padding: 15px 0;
  background: #5a5a8514;
  border-radius: 8px;
  .sessions {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: nowrap;
    margin-bottom: 15px;
    button {
      width: 110px;
      border: none;
      overflow: hidden;
      background: transparent;
      color: white;
      border-radius: 4px;
      font-size: 18px;
      padding: 5px 7px;
      white-space: nowrap;
      &:hover {
        background: #06061c;
      }
    }
    .active {
      color: #ff889c;
      background: #ff889c18;
    }
  }
  p {
    color: #ffffff54;
  }
  .time {
    font-size: 100px;
    font-weight: bold;
  }
  .pause {
    border: none;
    overflow: hidden;
    background: transparent;
    border-radius: 4px;
    font-size: 18px;
    padding: 10px 15px;
    margin: 10px;
    white-space: nowrap;
    color: #2dff61;
    background: #79ff9a18;
    transition: all 0.3s ease-in;
    &:hover {
      background: #64ff8b3d;
      box-shadow: 0px 0px 8px #4fff7b40;
    }
  }

  .stop {
    border: none;
    overflow: hidden;
    background: transparent;
    border-radius: 4px;
    margin: 10px;
    font-size: 18px;
    padding: 10px 15px;
    white-space: nowrap;
    color: #ff889c;
    background: #ff889c18;
    transition: all 0.3s ease-in;
    &:hover {
      background: #ff819638;
      box-shadow: 0px 0px 8px #ff819648;
    }
  }
}
</style>
