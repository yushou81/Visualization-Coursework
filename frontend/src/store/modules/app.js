import { defineStore } from 'pinia'
import Cookies from 'js-cookie'

export const useAppStore = defineStore('app', {
  state: () => ({
    sidebar: {
      opened: !+Cookies.get('sidebarStatus')
    }
  }),
  actions: {
    toggleSideBar() {
      if (this.sidebar.opened) {
        Cookies.set('sidebarStatus', 1)
      } else {
        Cookies.set('sidebarStatus', 0)
      }
      this.sidebar.opened = !this.sidebar.opened
    }
  }
})
