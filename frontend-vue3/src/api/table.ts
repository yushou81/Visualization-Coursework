import request from '@/utils/request'

export function getList(id: string | number) {
  return request({
    url: '/',
    method: 'get',
    params: { id }
  })
}
