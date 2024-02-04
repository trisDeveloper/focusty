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
        <div class="tasks">
          <div v-for="task in day.tasks" :key="task.title" class="task">
            {{ task.title }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      today: new Date(),
      isWideScreen: window.innerWidth >= 1075,
      tasks: [
        { title: "Task 1", date: "2024-02-05" },
        { title: "Task 2", date: "2024-02-08" },
      ],
    };
  },
  computed: {
    displayedDays() {
      const daysToDisplay = this.isWideScreen ? 7 : 4;
      const displayedDays = this.next7Days.slice(0, daysToDisplay);

      // Populate tasks for each day
      displayedDays.forEach((day) => {
        day.tasks = this.getTasksForDate(day.date);
      });

      return displayedDays;
    },
    next7Days() {
      const nextDays = [];
      for (let i = 0; i < 7; i++) {
        const nextDay = new Date();
        nextDay.setDate(this.today.getDate() + i);
        nextDays.push({
          weekday: this.formatDatePart(nextDay, "weekday"),
          month: this.formatDatePart(nextDay, "month"),
          day: this.formatDatePart(nextDay, "day"),
          date: nextDay.toISOString().split("T")[0], // Add the date property
        });
      }
      return nextDays;
    },
  },
  methods: {
    formatDatePart(date, part) {
      const options = {
        weekday: "short",
        month: "short",
        day: "numeric",
      };
      return date.toLocaleDateString("en-US", { [part]: options[part] });
    },
    getTasksForDate(date) {
      return this.tasks.filter((task) => task.date === date);
    },
    getDayColor(weekday) {
      // Add logic to determine color based on weekday
      switch (weekday) {
        case "Sun":
          return "#ff8d84";
        case "Mon":
          return "#ff9dd7";
        case "Tue":
          return "#29ff7c";
        case "Wed":
          return "#c4a3ff";
        case "Thu":
          return "#8dc4ff";
        case "Fri":
          return "#ffcf3f";
        case "Sat":
          return "#ffff69";
        default:
          return "#ddd"; // Default color
      }
    },
    handleResize() {
      this.isWideScreen = window.innerWidth >= 1075;
    },
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

<style lang="scss" scoped>
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
    .tasks {
      padding: 5px;
      .task {
        margin-top: 5px;
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
