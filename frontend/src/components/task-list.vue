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
      <div class="task-actions">
        <!-- delete icon -->
        <font-awesome-icon
          icon="fa-regular fa-trash-can"
          class="trash"
          @click="deleteTask(selectedTask)"
        />
        <font-awesome-icon
          icon="fa-regular fa-check-square"
          class="checkbox"
          @click="updateTaskDoneStatus(selectedTask)"
          :class="{ done: selectedTask.done }"
        />
      </div>
      <!-- title -->
      <div class="task-title">
        <input
          class="task-title"
          v-model="selectedTask.title"
          placeholder="Title"
        />
        <font-awesome-icon icon="fa-solid fa-pencil" />
      </div>
      <!-- date input -->
      <button class="task-date">
        <font-awesome-icon icon="fa-solid fa-calendar-days" />{{
          selectedTask.date
        }}
      </button>
      <input
        class="task-desc"
        v-model="selectedTask.description"
        placeholder="Description"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: ["tasks", "day"],
  data() {
    return {
      selectedTask: {
        title: "",
        date: this.day.date,
        description: "",
      },
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
        document.body.addEventListener("click", this.closeTaskCard);
      } else {
        document.body.removeEventListener("click", this.closeTaskCard);
      }
    },
    closeTaskCard(event) {
      if (this.$refs.taskCard && !this.$refs.taskCard.contains(event.target)) {
        this.isopencard = false;
        document.body.removeEventListener("click", this.closeTaskCard);
      }
    },
    // delete task
    async deleteTask(task) {
      try {
        task.done = !task.done;
        this.isopencard = false;
        await axios.delete(`/api/tasks/${task.id}/`, { done: task.done });
        this.$emit("task-deleted", task.id);
      } catch (error) {
        // Handle errors
        console.error(error);
      }
    },
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
  flex-grow: 1;
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
    box-shadow: 0px 2px 8px 2px #0202087e;
    z-index: 10;
    .task-actions {
      display: flex;
      flex-direction: row-reverse;
      margin-bottom: 10px;
      color: #ddd;
      font-size: 18px;
      .trash,
      .checkbox {
        padding-left: 10px;
        &:hover {
          color: #c4a3ff;
        }
      }
    }
    .task-title input,
    .task-desc,
    .task-date {
      border: none;
      background: #06061c;
      color: white;
      margin: 10px 0;
      width: 100%;
      padding: 5px;
      font-size: 20px;
      border-bottom: 1px solid transparent;
      &:hover {
        background-color: #121231;
      }
      &:focus-visible {
        outline: none;
        border-bottom: 1px solid white;
      }
    }
    .task-title {
      position: relative;
      display: flex;
      align-items: center;
      input {
        border-bottom: 1px solid #ddd;
      }
      svg {
        position: absolute;
        right: 5px;
        color: #ccc;
      }
    }
    .task-date {
      margin: 5px 0;
      font-size: 16px;
      text-align: left;
      border: none;
      padding: 10px 5px;
      svg {
        padding-right: 10px;
      }
    }
    .task-desc {
      font-size: 15px;
      color: #ffffffc4;
    }
  }
}
</style>
