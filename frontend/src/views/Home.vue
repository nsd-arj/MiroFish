<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-brand">MIROFISH</div>
      <div class="nav-links">
        <LanguageSwitcher />
        <a href="https://github.com/666ghj/MiroFish" target="_blank" class="github-link">
          {{ $t('nav.visitGithub') }} <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- 上半部分：Hero 区域 -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="orange-tag">{{ $t('home.tagline') }}</span>
            <span class="version-text">{{ $t('home.version') }}</span>
          </div>
          
          <h1 class="main-title">
            {{ $t('home.heroTitle1') }}<br>
            <span class="gradient-text">{{ $t('home.heroTitle2') }}</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              <i18n-t keypath="home.heroDesc" tag="span">
                <template #brand><span class="highlight-bold">{{ $t('home.heroDescBrand') }}</span></template>
                <template #agentScale><span class="highlight-orange">{{ $t('home.heroDescAgentScale') }}</span></template>
                <template #optimalSolution><span class="highlight-code">{{ $t('home.heroDescOptimalSolution') }}</span></template>
              </i18n-t>
            </p>
            <p class="slogan-text">
              {{ $t('home.slogan') }}<span class="blinking-cursor">_</span>
            </p>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <!-- Logo 区域 -->
          <div class="logo-container">
            <img src="../assets/logo/MiroFish_logo_left.jpeg" alt="MiroFish Logo" class="hero-logo" />
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- 下半部分：双栏布局 -->
      <section class="dashboard-section">
        <!-- 左栏：状态与步骤 -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> {{ $t('home.systemStatus') }}
          </div>
          
          <h2 class="section-title">{{ $t('home.systemReady') }}</h2>
          <p class="section-desc">
            {{ $t('home.systemReadyDesc') }}
          </p>
          
          <!-- 数据指标卡片 -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricLowCost') }}</div>
              <div class="metric-label">{{ $t('home.metricLowCostDesc') }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricHighAvail') }}</div>
              <div class="metric-label">{{ $t('home.metricHighAvailDesc') }}</div>
            </div>
          </div>

          <!-- 项目模拟步骤介绍 (新增区域) -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> {{ $t('home.workflowSequence') }}
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step01Title') }}</div>
                  <div class="step-desc">{{ $t('home.step01Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step02Title') }}</div>
                  <div class="step-desc">{{ $t('home.step02Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step03Title') }}</div>
                  <div class="step-desc">{{ $t('home.step03Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step04Title') }}</div>
                  <div class="step-desc">{{ $t('home.step04Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step05Title') }}</div>
                  <div class="step-desc">{{ $t('home.step05Desc') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右栏：交互控制台 -->
        <div class="right-panel">
          <!-- Mode toggle -->
          <div class="mode-toggle">
            <button
              class="mode-btn"
              :class="{ active: mode === 'new' }"
              @click="switchMode('new')"
            >New Brand</button>
            <button
              class="mode-btn"
              :class="{ active: mode === 'audience' }"
              @click="switchMode('audience')"
            >Use Saved Audience</button>
          </div>

          <!-- Audience reuse panel -->
          <div v-if="mode === 'audience'" class="console-box">
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">Saved Audiences</span>
              </div>
              <div v-if="audiencesLoading" class="audience-loading">Loading...</div>
              <div v-else-if="audiences.length === 0" class="audience-empty">
                No saved audiences yet. Complete a simulation and save its audience from the environment setup step.
              </div>
              <div v-else class="audience-list">
                <div
                  v-for="aud in audiences"
                  :key="aud.audience_id"
                  class="audience-card"
                  :class="{ selected: selectedAudience?.audience_id === aud.audience_id }"
                  @click="selectedAudience = aud"
                >
                  <div class="audience-name">{{ aud.name }}</div>
                  <div class="audience-meta">
                    <span v-if="aud.brand_name" class="audience-brand">{{ aud.brand_name }}</span>
                    <span class="audience-count">{{ aud.profile_count }} agents</span>
                    <span class="audience-date">{{ formatAudienceDate(aud.created_at) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="console-divider"><span>New Scenario</span></div>

            <div class="console-section">
              <div class="console-header">
                <span class="console-label">Simulation Requirement</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="audienceScenario"
                  class="code-input"
                  placeholder="Describe what you want to simulate with this audience..."
                  rows="5"
                  :disabled="audienceLoading"
                ></textarea>
              </div>
            </div>

            <div class="console-section btn-section">
              <button
                class="start-engine-btn"
                @click="startFromAudience"
                :disabled="!selectedAudience || !audienceScenario.trim() || audienceLoading"
              >
                <span v-if="!audienceLoading">Run Simulation →</span>
                <span v-else>Starting...</span>
              </button>
              <div v-if="audienceError" class="audience-start-error">{{ audienceError }}</div>
            </div>
          </div>

          <div v-if="mode === 'new'" class="console-box">
            <!-- 上传区域 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.realitySeed') }}</span>
                <span class="console-meta">
                  {{ hasBrandContext ? 'Optional — brand context generates seed automatically' : $t('home.supportedFormats') }}
                </span>
              </div>
              
              <div 
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">{{ $t('home.dragToUpload') }}</div>
                  <div class="upload-hint">{{ $t('home.orBrowse') }}</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分割线 -->
            <div class="console-divider">
              <span>{{ $t('home.inputParams') }}</span>
            </div>

            <!-- 输入区域 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.simulationPrompt') }}</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  :placeholder="$t('home.promptPlaceholder')"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">{{ $t('home.engineBadge') }}</div>
              </div>
            </div>

            <!-- Brand context -->
            <div class="console-divider">
              <span>Brand Context <span class="divider-optional">(optional)</span></span>
            </div>

            <div class="console-section brand-section">
              <div class="brand-field">
                <label class="brand-label">Brand Name</label>
                <input
                  v-model="formData.brandName"
                  class="brand-input"
                  placeholder="e.g. Acme Co."
                  :disabled="loading"
                />
              </div>
              <div class="brand-field">
                <label class="brand-label">Brand URL</label>
                <input
                  v-model="formData.brandUrl"
                  class="brand-input"
                  placeholder="e.g. https://acme.com"
                  :disabled="loading"
                />
              </div>
              <div class="brand-field">
                <label class="brand-label">Primary Objection</label>
                <input
                  v-model="formData.primaryObjection"
                  class="brand-input"
                  placeholder="e.g. too expensive, privacy concerns"
                  :disabled="loading"
                />
              </div>
              <div class="brand-field">
                <label class="brand-label">Advocate Trigger</label>
                <input
                  v-model="formData.advocateTrigger"
                  class="brand-input"
                  placeholder="e.g. best customer support I've ever had"
                  :disabled="loading"
                />
              </div>
              <div class="brand-field">
                <label class="brand-label">Target Segment</label>
                <input
                  v-model="formData.targetSegment"
                  class="brand-input"
                  placeholder="e.g. small business owner, 30–45"
                  :disabled="loading"
                />
              </div>
            </div>

            <!-- 启动按钮 -->
            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">{{ $t('home.startEngine') }}</span>
                <span v-else>{{ $t('home.initializing') }}</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div><!-- end console-box (new brand) -->
        </div>
      </section>

      <!-- Recent Projects -->
      <section v-if="recentProjects.length > 0" class="recent-projects">
        <h3 class="recent-title">Recent Runs</h3>
        <div class="recent-list">
          <div
            v-for="proj in recentProjects"
            :key="proj.project_id"
            class="recent-card"
          >
            <div class="recent-card-info">
              <span class="recent-brand">{{ proj.brand_name || proj.name || proj.project_id }}</span>
              <span :class="['recent-status', statusLabel(proj.status).cls]">
                {{ statusLabel(proj.status).text }}
              </span>
            </div>
            <button class="recent-resume-btn" @click="resumeProject(proj.project_id)">
              Resume
            </button>
          </div>
        </div>
      </section>

      <!-- 历史项目数据库 -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import { listAudiences } from '../api/audience'
import { createSimulation } from '../api/simulation'
import { setPendingUpload } from '../store/pendingUpload'
import { listProjects } from '../api/graph'

const router = useRouter()

// 表单数据
const formData = ref({
  simulationRequirement: '',
  brandName: '',
  brandUrl: '',
  primaryObjection: '',
  advocateTrigger: '',
  targetSegment: '',
})

// 文件列表
const files = ref([])

// 状态
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// 文件输入引用
const fileInput = ref(null)

// Mode: 'new' = upload docs, 'audience' = use saved audience
const mode = ref('new')

// Audience reuse state
const audiences = ref([])
const audiencesLoading = ref(false)
const selectedAudience = ref(null)
const audienceScenario = ref('')
const audienceLoading = ref(false)
const audienceError = ref('')

const switchMode = async (m) => {
  mode.value = m
  if (m === 'audience' && audiences.value.length === 0) {
    audiencesLoading.value = true
    try {
      const res = await listAudiences()
      if (res.success) audiences.value = res.data
    } finally {
      audiencesLoading.value = false
    }
  }
}

const formatAudienceDate = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const startFromAudience = async () => {
  if (!selectedAudience.value || !audienceScenario.value.trim()) return
  audienceLoading.value = true
  audienceError.value = ''
  try {
    const res = await createSimulation({
      project_id: selectedAudience.value.project_id,
      graph_id: selectedAudience.value.graph_id,
      audience_id: selectedAudience.value.audience_id,
      simulation_requirement_override: audienceScenario.value.trim(),
    })
    if (res.success) {
      router.push({ name: 'Simulation', params: { simulationId: res.data.simulation_id } })
    } else {
      audienceError.value = res.error || 'Failed to start simulation'
    }
  } catch (e) {
    audienceError.value = e.message || 'Failed to start simulation'
  } finally {
    audienceLoading.value = false
  }
}

// 计算属性:是否可以提交
const hasBrandContext = computed(() =>
  formData.value.brandName.trim() !== ''
)

const canSubmit = computed(() => {
  if (!formData.value.simulationRequirement.trim()) return false
  // Files required only when brand context is not provided
  return files.value.length > 0 || hasBrandContext.value
})

// 触发文件选择
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// 处理拖拽相关
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// 添加文件
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// 移除文件
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// 滚动到底部
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// Recent projects
const recentProjects = ref([])
const recentLoading = ref(false)

const STATUS_LABEL = {
  created: { text: 'Ontology pending', cls: 'status-pending' },
  ontology_generated: { text: 'Ready to build', cls: 'status-pending' },
  graph_building: { text: 'Building graph…', cls: 'status-running' },
  graph_completed: { text: 'Graph ready', cls: 'status-done' },
  failed: { text: 'Failed', cls: 'status-failed' },
}

const statusLabel = (s) => STATUS_LABEL[s] || { text: s, cls: '' }

const loadRecentProjects = async () => {
  recentLoading.value = true
  try {
    const res = await listProjects(8)
    if (res.success) recentProjects.value = res.data
  } catch (_) {}
  finally { recentLoading.value = false }
}

const resumeProject = (projectId) => {
  router.push({ name: 'Process', params: { projectId } })
}

const FORM_STORAGE_KEY = 'mirofish_last_form'

const saveFormToStorage = () => {
  try {
    localStorage.setItem(FORM_STORAGE_KEY, JSON.stringify({
      simulationRequirement: formData.value.simulationRequirement,
      brandName: formData.value.brandName,
      brandUrl: formData.value.brandUrl,
      primaryObjection: formData.value.primaryObjection,
      advocateTrigger: formData.value.advocateTrigger,
      targetSegment: formData.value.targetSegment,
    }))
  } catch (_) {}
}

const restoreFormFromStorage = () => {
  try {
    const saved = JSON.parse(localStorage.getItem(FORM_STORAGE_KEY) || 'null')
    if (saved) {
      formData.value.simulationRequirement = saved.simulationRequirement || ''
      formData.value.brandName = saved.brandName || ''
      formData.value.brandUrl = saved.brandUrl || ''
      formData.value.primaryObjection = saved.primaryObjection || ''
      formData.value.advocateTrigger = saved.advocateTrigger || ''
      formData.value.targetSegment = saved.targetSegment || ''
    }
  } catch (_) {}
}

onMounted(() => {
  restoreFormFromStorage()
  loadRecentProjects()
})

// 开始模拟 - 立即跳转，API调用在Process页面进行
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return

  saveFormToStorage()

  setPendingUpload(files.value, formData.value.simulationRequirement, {
    brandName: formData.value.brandName,
    brandUrl: formData.value.brandUrl,
    primaryObjection: formData.value.primaryObjection,
    advocateTrigger: formData.value.advocateTrigger,
    targetSegment: formData.value.targetSegment,
  })

  router.push({
    name: 'Process',
    params: { projectId: 'new' }
  })
}
</script>

<style scoped>
/* 全局变量与重置 */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  /* 
    使用 Space Grotesk 作为主要标题字体，JetBrains Mono 作为代码/标签字体
    确保已在 index.html 引入这些 Google Fonts 
  */
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* 顶部导航 */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.github-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

/* 主要内容区 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero 区域 */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 500;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: var(--black);
}

.gradient-text {
  background: linear-gradient(90deg, #000000 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--black);
  font-weight: 700;
}

.highlight-orange {
  color: var(--orange);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--black);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: var(--black);
  letter-spacing: 1px;
  border-left: 3px solid var(--orange);
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: var(--orange);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
}

.hero-logo {
  max-width: 500px; /* 调整logo大小 */
  width: 100%;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--orange);
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--orange);
}

/* Dashboard 双栏布局 */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* 左侧面板 */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid var(--border);
  padding: 20px 30px;
  min-width: 150px;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
}

/* 项目模拟步骤介绍 */
.steps-container {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--black);
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* 右侧交互控制台 */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid #CCC; /* 外部实线 */
  padding: 8px; /* 内边距形成双重边框感 */
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

.upload-zone {
  border: 1px dashed #CCC;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #FAFAFA;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: #F0F0F0;
  border-color: #999;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #AAA;
}

/* Mode toggle */
.mode-toggle {
  display: flex;
  margin-bottom: 12px;
  border: 1px solid #E0E0E0;
}

.mode-btn {
  flex: 1;
  padding: 10px;
  background: transparent;
  border: none;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  letter-spacing: 0.04em;
  cursor: pointer;
  color: #888;
  transition: all 0.15s;
}

.mode-btn.active {
  background: #000;
  color: #fff;
}

/* Audience list */
.audience-loading,
.audience-empty {
  font-size: 0.85rem;
  color: #999;
  padding: 16px 0;
}

.audience-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 260px;
  overflow-y: auto;
}

.audience-card {
  padding: 12px;
  border: 1px solid #E0E0E0;
  cursor: pointer;
  transition: border-color 0.15s;
}

.audience-card:hover {
  border-color: #999;
}

.audience-card.selected {
  border-color: #000;
  background: #F9F9F9;
}

.audience-name {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.audience-meta {
  display: flex;
  gap: 12px;
  font-size: 0.75rem;
  color: #999;
}

.audience-brand {
  color: #FF6B35;
}

.audience-start-error {
  margin-top: 8px;
  font-size: 0.8rem;
  color: #c00;
}

.divider-optional {
  font-size: 0.75em;
  opacity: 0.5;
  font-weight: 400;
}

.brand-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px 0 4px;
}

.brand-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.brand-label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #888;
}

.brand-input {
  border: 1px solid #E0E0E0;
  background: transparent;
  padding: 8px 12px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  outline: none;
  transition: border-color 0.2s;
  color: inherit;
}

.brand-input:focus {
  border-color: #000;
}

.brand-input:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.start-engine-btn {
  width: 100%;
  background: var(--black);
  color: var(--white);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* 可点击状态（非禁用） */
.start-engine-btn:not(:disabled) {
  background: var(--black);
  border: 1px solid var(--black);
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E5E5;
}

/* 引导动画：微妙的边框脉冲 */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>

<style>
/* English locale adjustments (unscoped to target html[lang]) */
html[lang="en"] .main-title {
  font-size: 3.5rem;
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: -1px;
}

html[lang="en"] .hero-desc {
  text-align: left;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .slogan-text {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .tag-row {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .navbar .nav-links {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Left pane: system status + workflow */
html[lang="en"] .status-section {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .status-section .status-ready {
  font-size: 1.6rem;
}

html[lang="en"] .status-section .metric-value {
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 1.4rem;
}

html[lang="en"] .workflow-list .step-title {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .workflow-list .step-desc {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  font-size: 0.72rem !important;
  line-height: 1.4 !important;
}

html[lang="en"] .workflow-list {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Recent Projects */
.recent-projects {
  padding: 24px 32px;
  border-top: 1px solid var(--border, #E5E5E5);
}
.recent-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--gray-text, #666);
  margin-bottom: 12px;
}
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.recent-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border: 1px solid var(--border, #E5E5E5);
  border-radius: 6px;
  gap: 12px;
}
.recent-card-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.recent-brand {
  font-size: 13px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.recent-status {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  white-space: nowrap;
  flex-shrink: 0;
}
.status-pending  { background: #FFF3CD; color: #856404; }
.status-running  { background: #D1ECF1; color: #0C5460; }
.status-done     { background: #D4EDDA; color: #155724; }
.status-failed   { background: #F8D7DA; color: #721C24; }
.recent-resume-btn {
  font-size: 12px;
  font-weight: 600;
  padding: 5px 14px;
  border: 1px solid #000;
  border-radius: 4px;
  background: #000;
  color: #FFF;
  cursor: pointer;
  flex-shrink: 0;
  transition: opacity 0.15s;
}
.recent-resume-btn:hover { opacity: 0.75; }
</style>
