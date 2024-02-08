import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useGlobalStore = defineStore('global', {
  state: () => ({
    isopencard: false,
    selectedTask: null,
  }),
  actions: {
    setIsOpenCard(value) {
      this.isopencard = value;
    },
    setSelectedTask(task) {
      this.selectedTask = task;
    },
  },
});

