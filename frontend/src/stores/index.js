import { defineStore } from 'pinia'

export const useStore = defineStore('storeId', {
  state: () => ({
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
    selectedTask: {
      id: null,
      title: '',
      date: null,
      time: '00:00',
      description: '',
      done: false,
      user: null
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
    },
    setUser(user) {
      this.user = user
    }
  }
})
