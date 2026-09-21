/**
 * 临时存储待上传的文件和需求
 * 用于首页点击启动引擎后立即跳转，在Process页面再进行API调用
 *
 * Text fields are also mirrored to sessionStorage so they survive a
 * component re-mount triggered by router.replace (Vue Router 4 can
 * remount the same component when params change).  Files can't be
 * serialised, but in the brand-context-only flow there are none.
 */
import { reactive } from 'vue'

const SESSION_KEY = 'mirofish_pending'

const state = reactive({
  files: [],
  simulationRequirement: '',
  brandName: '',
  brandUrl: '',
  primaryObjection: '',
  advocateTrigger: '',
  targetSegment: '',
  isPending: false
})

function _saveToSession() {
  try {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify({
      simulationRequirement: state.simulationRequirement,
      brandName: state.brandName,
      brandUrl: state.brandUrl,
      primaryObjection: state.primaryObjection,
      advocateTrigger: state.advocateTrigger,
      targetSegment: state.targetSegment,
      isPending: state.isPending,
    }))
  } catch (_) {}
}

function _clearSession() {
  try { sessionStorage.removeItem(SESSION_KEY) } catch (_) {}
}

export function setPendingUpload(files, requirement, brandContext = {}) {
  state.files = files
  state.simulationRequirement = requirement
  state.brandName = brandContext.brandName || ''
  state.brandUrl = brandContext.brandUrl || ''
  state.primaryObjection = brandContext.primaryObjection || ''
  state.advocateTrigger = brandContext.advocateTrigger || ''
  state.targetSegment = brandContext.targetSegment || ''
  state.isPending = true
  _saveToSession()
}

export function getPendingUpload() {
  // If in-memory state was wiped by a re-mount, recover text fields from sessionStorage.
  if (!state.isPending) {
    try {
      const saved = JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null')
      if (saved && saved.isPending) {
        state.simulationRequirement = saved.simulationRequirement || ''
        state.brandName = saved.brandName || ''
        state.brandUrl = saved.brandUrl || ''
        state.primaryObjection = saved.primaryObjection || ''
        state.advocateTrigger = saved.advocateTrigger || ''
        state.targetSegment = saved.targetSegment || ''
        state.isPending = true
      }
    } catch (_) {}
  }

  return {
    files: state.files,
    simulationRequirement: state.simulationRequirement,
    brandName: state.brandName,
    brandUrl: state.brandUrl,
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
  state.brandUrl = ''
  state.primaryObjection = ''
  state.advocateTrigger = ''
  state.targetSegment = ''
  state.isPending = false
  _clearSession()
}

export default state
