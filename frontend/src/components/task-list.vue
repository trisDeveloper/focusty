<template>
  <div class="tasks">
    <div
      v-for="task in day.tasks"
      :key="task.title"
      :class="{ task, done: task.done }"
      @click="openTaskCard($event, task)"
    >
      <font-awesome-icon
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(task)"
        :class="{ done: task.done }"
      />
      <p>{{ task.title }}</p>
    </div>
    <div v-if="isopencard" class="task-card" ref="taskCard">
      <input class="task-title" :value="selectedTask.titles" />
      <p>{{ selectedTask.description }}</p>
      <p>{{ selectedTask.date }}</p>
      <button @click="deleteTask(selectedTask)">Delete</button>
      <!-- Other task details and actions -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: ["tasks", "day"],
  data() {
    return {
      selectedTask: null,
      isopencard: false,
    };
  },
  methods: {
    async updateTaskDoneStatus(task) {
      try {
        task.done = !task.done;
        await axios.patch(`/api/tasks/${task.id}/`, { done: task.done });
      } catch (error) {
        // Handle errors
        console.error(error);
      }
    },
    openTaskCard(event, task) {
      event.stopPropagation();
      this.isopencard = !this.isopencard;
      this.selectedTask = task;
      if (this.isopencard) {
        window.addEventListener("click", this.closeTaskCard);
      } else {
        window.removeEventListener("click", this.closeTaskCard);
      }
    },
    closeTaskCard(event) {
      if (this.$refs.taskCard && !this.$refs.taskCard.contains(event.target)) {
        this.isopencard = false;
        window.removeEventListener("click", this.closeTaskCard);
      }
    },
    // delete task
    async deleteTask(task) {
      try {
        task.done = !task.done;
        await axios.delete(`/api/tasks/${task.id}/`, { done: task.done });
      } catch (error) {
        // Handle errors
        console.error(error);
      }
    },
  },
  mounted() {
    document.body.addEventListener("click", this.closeTaskCard);
  },
  beforeUnmount() {
    document.body.removeEventListener("click", this.closeTaskCard);
  },
};
</script>

<style lang="scss">
@import "./../styles.scss";
.tasks {
  padding: 5px;
  .task {
    display: flex;
    align-items: stretch;
    font-size: 18px;
    position: relative;
    margin: 8px 0;
    padding: 8px;
    box-sizing: border-box;
    $border: 1px;
    color: #fff;
    background: $dark-back;
    background-clip: padding-box;
    border: solid $border transparent;
    border-radius: 7px;
    .checkbox {
      padding: 0 10px 0 0;
    }
    p {
      overflow: hidden;
    }
    &:hover {
      background-color: #121231;
      cursor: pointer;
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
  .done {
    color: #393949;
    text-decoration: line-through;
    transition: all 0.3s;
  }
  .task-card {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 400px;
    max-width: calc(100% - 10px);
    transform: translate(-50%, -50%);
    border-radius: 10px;
    padding: 20px;
    background-color: #393949;
    z-index: 10;
  }
}
</style>
