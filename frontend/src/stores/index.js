import { defineStore } from 'pinia'

export const useStore = defineStore('storeId', {
  state: () => ({
    isopencard: false,
    isdatepicker: false,
    selectedTask: {
      id: null,
      title: '',
      date: null,
      description: '',
      done: false
    }
  }),
  actions: {
    setIsOpenCard(value) {
      this.isopencard = value
    },
    setSelectedTask(task) {
      this.selectedTask = task
    },
    toggledatepicker(value) {
      this.isdatepicker = value
    }
  }
})
