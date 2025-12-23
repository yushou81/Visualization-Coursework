import { defineStore } from 'pinia'
import { login, logout, getInfo } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getToken(),
    name: '',
    avatar: '',
    roles: []
  }),
  actions: {
    // 登录
    async login(userInfo) {
      const username = userInfo.username.trim()
      try {
        const response = await login(username, userInfo.password)
          const data = response.data
          setToken(data.token)
        this.token = data.token
      } catch (error) {
        throw error
      }
    },

    // 获取用户信息
    async getInfo() {
      try {
        const response = await getInfo(this.token)
          const data = response.data
        this.roles = data.roles
        this.name = data.name
        this.avatar = data.avatar
        return response
      } catch (error) {
        throw error
      }
    },

    // 登出
    async logOut() {
      try {
        await logout(this.token)
        this.token = ''
        this.roles = []
          removeToken()
      } catch (error) {
        throw error
      }
    },

    // 前端 登出
    fedLogOut() {
      this.token = ''
        removeToken()
    }
  }
})
