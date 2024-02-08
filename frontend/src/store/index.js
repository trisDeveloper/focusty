import { createStore } from "vuex";

export default createStore({
  state: {
    isopencard: false,
    selectedTask: {
      id: null,
      title: "",
      date: null,
      description: "",
      done: false,
    },
  },
  mutations: {
    UPDATE_ISOPENCARD(state, payload) {
      state.isopencard = payload;
    },
    UPDATE_SELECTED_TASK(state, payload) {
      // Create a copy of the selectedTask to avoid accidental mutations
      state.selectedTask = Object.assign({}, state.selectedTask, payload);
    },
  },
  actions: {
    setIsopencard({ commit }, payload) {
      commit("UPDATE_ISOPENCARD", payload);
    },
    setSelectedTask({ commit }, payload) {
      commit("UPDATE_SELECTED_TASK", payload);
    },
  },
});
