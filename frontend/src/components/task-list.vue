<template>
  <div class="tasks">
    <div
      v-for="task in day.tasks"
      :key="task.title"
      :class="{ task, done: task.done }"
    >
      <font-awesome-icon
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(task)"
        :class="{ done: task.done }"
      />
      {{ task.title }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: ["tasks", "day"],
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
}
</style>
