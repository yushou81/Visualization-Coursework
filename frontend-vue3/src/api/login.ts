import request from '@/utils/request'

export interface LoginPayload {
  username: string
  password: string
}

export function login(data: LoginPayload) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token: string) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}
