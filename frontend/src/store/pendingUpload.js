/**
 * 临时存储待上传的文件和需求
 * 用于首页点击启动引擎后立即跳转，在Process页面再进行API调用
 */
import { reactive } from 'vue'

const state = reactive({
  files: [],
  simulationRequirement: '',
  brandName: '',
  primaryObjection: '',
  advocateTrigger: '',
  targetSegment: '',
  isPending: false
})

export function setPendingUpload(files, requirement, brandContext = {}) {
  state.files = files
  state.simulationRequirement = requirement
  state.brandName = brandContext.brandName || ''
  state.primaryObjection = brandContext.primaryObjection || ''
  state.advocateTrigger = brandContext.advocateTrigger || ''
  state.targetSegment = brandContext.targetSegment || ''
  state.isPending = true
}

export function getPendingUpload() {
  return {
    files: state.files,
    simulationRequirement: state.simulationRequirement,
    brandName: state.brandName,
    primaryObjection: state.primaryObjection,
    advocateTrigger: state.advocateTrigger,
    targetSegment: state.targetSegment,
    isPending: state.isPending
  }
}

export function clearPendingUpload() {
  state.files = []
  state.simulationRequirement = ''
  state.brandName = ''
  state.primaryObjection = ''
  state.advocateTrigger = ''
  state.targetSegment = ''
  state.isPending = false
}

export default state
