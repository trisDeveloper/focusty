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
        <task-list :tasks="tasks" :day="day" />
      </div>
    </div>
  </div>
</template>

<script>
import taskList from "../components/task-list.vue";
import axios from "axios";

export default {
  components: { taskList },
  data() {
    return {
      today: new Date(),
      isWideScreen: window.innerWidth >= 1075 || window.innerWidth <= 600,
      tasks: [],
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
      const tasksForDate = this.tasks.filter((task) => task.date === date);
      return tasksForDate.sort((a, b) =>
        a.done === b.done ? 0 : a.done ? 1 : -1
      );
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
      this.isWideScreen = window.innerWidth >= 1075 || window.innerWidth <= 600;
    },
    fetchData() {
      // get tasks list
      axios
        .get("/api/tasks/")
        .then((response) => {
          console.log(response.data);
          this.tasks = response.data;
        })
        .catch((error) => {
          // Handle errors
          console.error(error);
        });
    },
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
    // from backend
    this.fetchData();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

<style lang="scss" scoped>
@import "./../styles.scss";
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
        display: flex;
        align-items: stretch;
        font-size: 18px;
        position: relative;
        margin: 8px 0;
        padding: 10px;
        box-sizing: border-box;
        $border: 1px;
        color: #fff;
        background: $dark-back;
        background-clip: padding-box;
        border: solid $border transparent;
        border-radius: 7px;
        .checkbox {
          padding: 0 10px 0 0;
          &:hover {
            color: yellow;
          }
        }

        &:hover {
          background-color: #121231;
        }
        &:before {
          content: "";
          position: absolute;
          top: 0;
          right: 0;
          bottom: 0;
          left: 0;
          z-index: -1;
          margin: -$border;
          border-radius: inherit;
          background: $rainbow-gradient;
        }
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
