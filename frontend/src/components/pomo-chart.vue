<template>
  <div class="chart">
    <canvas ref="lineChart" width="400" height="200" class="canvas"></canvas>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  data() {
    return {
      pomodorosData: [],
      lastWeekData: [],
      chart: null
    }
  },
  mounted() {
    this.fetchPomodorosData()
  },
  methods: {
    async fetchPomodorosData() {
      try {
        const response = await axios.get(`/api/users/${localStorage.getItem('userId')}/pomodoros`)
        this.pomodorosData = response.data
        this.getLastWeekData()
        this.renderChart()
      } catch (error) {
        console.error('Error fetching data:', error)
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
        return {
          date,
          hours
        }
      })
    },
    renderChart() {
      const ctx = this.$refs.lineChart.getContext('2d')
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.lastWeekData.map((pomodoro) => pomodoro.date),
          datasets: [
            {
              label: 'Hours',
              data: this.lastWeekData.map((pomodoro) => pomodoro.hours),
              backgroundColor: 'rgba(255, 192, 192, 0)',
              borderColor: '#e13f5b'
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
    }
  }
}
</script>

<style lang="scss">
.chart {
  max-width: 600px;
  width: 100%;
}
</style>
