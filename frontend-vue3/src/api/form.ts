import request from '@/utils/request'

export function getChart(params: Record<string, any>) {
  return request({
    url: 'form/chart',
    method: 'get',
    params
  })
}
