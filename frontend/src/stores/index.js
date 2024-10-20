import { defineStore } from 'pinia'

export const useStore = defineStore('storeId', {
  state: () => ({
    tasks: [],
    user: {
      id: null,
      username: null,
      email: null,
      pic: null,
      birthday: null,
      country: null,
      join: null
    },
    isopencard: false,
    isRepeatOpen: false,
    selectedTask: {
      id: null,
      title: '',
      date: null,
      time: '00:00',
      description: '',
      repeatParameters: null,
      repeatId: null,
      done: false,
      user: null
    },
    timepic: {
      hours: 0,
      minutes: 0
    }
  }),
  actions: {
    setTasks(tasks) {
      this.tasks = tasks
    },
    setIsOpenCard(value) {
      this.isopencard = value
    },
    setIsRepeatOpen(value) {
      this.isRepeatOpen = value
    },
    setSelectedTask(task) {
      this.selectedTask = task
    },
    setUser(user) {
      this.user = user
    }
  }
})
