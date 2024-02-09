import { defineStore } from 'pinia'

export const useStore = defineStore('storeId', {
  state: () => ({
    isopencard: false,
    selectedTask: {
      id: null,
      title: '',
      date: null,
      time: '00:00',
      description: '',
      done: false
    },
    timepic: {
      hours: 0,
      minutes: 0
    }
  }),
  actions: {
    setIsOpenCard(value) {
      this.isopencard = value
    },
    setSelectedTask(task) {
      this.selectedTask = task
    }
  }
})
