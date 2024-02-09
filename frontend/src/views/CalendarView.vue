<template>
  <div class="container">
    <div class="calendar">
      <div v-for="(day, index) in displayedDays" :key="index" class="day">
        <div class="dayname">
          <div class="weekday" :style="{ color: getDayColor(day.weekday) }">
            {{ day.weekday }}
          </div>
          <div class="daynum">{{ day.month }} {{ day.day }}</div>
        </div>
        <task-list :tasks="tasks" :day="day" :fetch="fetchData" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import TaskList from '../components/task-list.vue'

export default {
  components: { TaskList },
  data() {
    return {
      today: new Date(),
      // resposive week view
      isWideScreen: window.innerWidth >= 1075 || window.innerWidth <= 600,
      tasks: []
    }
  },
  computed: {
    // responsive week view
    displayedDays() {
      const daysToDisplay = this.isWideScreen ? 7 : 4
      const displayedDays = this.next7Days.slice(0, daysToDisplay)
      displayedDays.forEach((day) => {
        day.tasks = this.getTasksForDate(day.date)
      })
      return displayedDays
    },
    // weekly view
    next7Days() {
      const nextDays = []
      for (let i = 0; i < 7; i++) {
        const nextDay = new Date()
        nextDay.setDate(this.today.getDate() + i)
        nextDays.push({
          weekday: this.formatDatePart(nextDay, 'weekday'),
          month: this.formatDatePart(nextDay, 'month'),
          day: this.formatDatePart(nextDay, 'day'),
          date: nextDay.toISOString().split('T')[0]
        })
      }
      return nextDays
    }
  },
  methods: {
    // date format    - thu feb 8 -
    formatDatePart(date, part) {
      const options = {
        weekday: 'short',
        month: 'short',
        day: 'numeric'
      }
      return date.toLocaleDateString('en-US', { [part]: options[part] })
    },
    // filter tasks per day
    getTasksForDate(date) {
      return this.tasks
        .filter((task) => task.date === date)
        .sort((a, b) => (a.done === b.done ? 0 : a.done ? 1 : -1))
    },
    // set colors per day
    getDayColor(weekday) {
      const colors = {
        Sun: '#ff8d84',
        Mon: '#ff9dd7',
        Tue: '#29ff7c',
        Wed: '#c4a3ff',
        Thu: '#8dc4ff',
        Fri: '#ffcf3f',
        Sat: '#ffff69'
      }
      return colors[weekday] || '#ddd'
    },
    handleResize() {
      this.isWideScreen = window.innerWidth >= 1075 || window.innerWidth <= 600
    },
    // get tasks list from backend
    fetchData() {
      axios
        .get('/api/tasks/')
        .then((response) => {
          this.tasks = response.data
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  // responsive week view
  mounted() {
    window.addEventListener('resize', this.handleResize)
    this.fetchData()
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
  }
}
</script>

<style lang="scss" scoped>
@import './../styles.scss';

.container {
  max-width: 1500px;
  margin: 0 auto;
}

.calendar {
  display: flex;
  justify-content: center;
  flex-wrap: nowrap;
  flex-direction: row;
  min-height: calc(100vh - 65px);

  .day {
    width: calc(100% / 7);
    padding: 5px;
    border: 1px solid #ffffff0f;
    display: flex;
    flex-direction: column;

    .dayname {
      height: fit-content;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-direction: row;

      .weekday {
        padding: 5px;
        font-size: 19px;
      }

      .daynum {
        padding: 5px;
        font-size: 23px;
        color: #fff;
      }
    }
  }

  @media (max-width: 1075px) {
    .day {
      width: calc(100% / 4);
    }
  }
}

@media (max-width: 600px) {
  .calendar {
    flex-wrap: nowrap;
    flex-direction: column;
    justify-content: flex-start;

    .day {
      width: calc(100%);
      border-bottom: 1px solid #ffffff0f;
    }
  }
}
</style>
