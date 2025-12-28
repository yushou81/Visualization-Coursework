import { defineStore } from 'pinia'

export const useDemoStore = defineStore('demo', {
  state: () => ({
    count: 0
  }),
  getters: {
    statusText: (state) => `当前计数：${state.count}`
  },
  actions: {
    increment() {
      this.count += 1
    }
  }
})
