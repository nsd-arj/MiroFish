import service from './index'

export function listAudiences() {
  return service({ url: '/audience/list', method: 'get' })
}

export function getAudience(audienceId) {
  return service({ url: `/audience/${audienceId}`, method: 'get' })
}

export function saveAudience({ simulationId, name }) {
  return service({
    url: '/audience/save',
    method: 'post',
    data: { simulation_id: simulationId, name }
  })
}
