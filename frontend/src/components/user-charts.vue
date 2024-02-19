<script setup>
import { ref } from 'vue'

const height = ref(window.innerWidth >= 600 ? 200 : 400)
const handleResize = () => {
  height.value = window.innerWidth >= 600 ? 200 : 400
}

window.addEventListener('resize', handleResize)
handleResize()
</script>

<template>
  <div>
    <div class="chart">
      <canvas ref="pomodoroChart" width="400" :height="height" class="canvas"></canvas>
    </div>
    <div class="chart">
      <canvas ref="taskChart" width="400" :height="height" class="canvas"></canvas>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  data() {
    return {
      pomodorosData: [],
      tasksData: [],
      lastWeekData: [],
      chart: null
    }
  },
  mounted() {
    this.fetchPomodorosData()
    this.fetchTasksCountData()
  },
  methods: {
    async fetchPomodorosData() {
      try {
        const response = await axios.get(`/api/users/${localStorage.getItem('userId')}/pomodoros`)
        this.pomodorosData = response.data
        this.getLastWeekData()
        this.renderPomodoroChart()
      } catch (error) {
        console.error('Error fetching Pomodoros data:', error)
      }
    },
    async fetchTasksCountData() {
      try {
        const response = await axios.get(`/api/users/${localStorage.getItem('userId')}/tasks/all`)
        this.tasksData = response.data
        this.getLastWeekData()
        this.renderTasksCountChart()
      } catch (error) {
        console.error('Error fetching Tasks Count data:', error)
      }
    },
    getLastWeekData() {
      const today = new Date()
      const lastWeek = new Date(today.getTime() - 6 * 24 * 60 * 60 * 1000)

      const lastWeekDates = []
      for (let i = 0; i < 7; i++) {
        const date = new Date(lastWeek)
        date.setDate(date.getDate() + i)
        lastWeekDates.push(date.toISOString().split('T')[0])
      }

      // Fill in minutes for each date, using 0 if no data exists
      this.lastWeekData = lastWeekDates.map((date) => {
        const matchingPomodoro = this.pomodorosData.find((pomodoro) => pomodoro.date === date)
        const hours = matchingPomodoro ? matchingPomodoro.minutes / 60 : 0
        const matchingTasks = this.tasksData.find((task) => task.date === date)
        const count = matchingTasks ? matchingTasks.tasks_count : 0
        return {
          date,
          hours,
          count
        }
      })
    },
    renderPomodoroChart() {
      const ctx = this.$refs.pomodoroChart.getContext('2d')
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.lastWeekData.map((pomodoro) => pomodoro.date),
          datasets: [
            {
              label: 'Hours',
              data: this.lastWeekData.map((pomodoro) => pomodoro.hours),
              backgroundColor: 'rgba(255, 192, 192, 0)',
              borderColor: '#ff889c'
            }
          ]
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Pomodoro Last Week',
              padding: {
                top: 10,
                bottom: 30
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              stepSize: 1
            }
          }
        }
      })
    },
    renderTasksCountChart() {
      const ctx = this.$refs.taskChart.getContext('2d')
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.lastWeekData.map((task) => task.date), // Corrected property name to labels
          datasets: [
            {
              label: 'Tasks Number',
              data: this.lastWeekData.map((task) => task.count),
              backgroundColor: 'rgba(192, 192, 255, 0)',
              borderColor: 'orange'
            }
          ]
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Tasks Count Last Week',
              padding: {
                top: 10,
                bottom: 30
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              stepSize: 1
            }
          }
        }
      })
    }
  }
}
</script>

<style lang="scss">
.chart {
  width: 100%;
  margin: 0 auto;
  margin-bottom: 25px;
  max-width: 600px;
}
</style>
