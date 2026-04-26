import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export type Language = 'en' | 'ru'

export const useSettingsStore = defineStore('settings', () => {
  // State - with localStorage persistence
  const cps = ref(Number(localStorage.getItem('settings_cps') ?? '50'))
  const voiceEnabled = ref(localStorage.getItem('settings_voice') === 'true')
  const autoAdvance = ref(localStorage.getItem('settings_auto') === 'true')
  const skipOngoing = ref(localStorage.getItem('settings_skip') === 'true')
  const language = ref<Language>(localStorage.getItem('settings_language') as Language || 'en')

  // Watch for changes and persist
  watch(cps, (val) => localStorage.setItem('settings_cps', String(val)))
  watch(voiceEnabled, (val) => localStorage.setItem('settings_voice', String(val)))
  watch(autoAdvance, (val) => localStorage.setItem('settings_auto', String(val)))
  watch(skipOngoing, (val) => localStorage.setItem('settings_skip', String(val)))
  watch(language, (val) => localStorage.setItem('settings_language', val))

  // Actions
  function setCps(value: number) {
    cps.value = Math.max(40, Math.min(60, value))
  }

  function toggleVoice() {
    voiceEnabled.value = !voiceEnabled.value
  }

  function toggleAutoAdvance() {
    autoAdvance.value = !autoAdvance.value
  }

  function toggleSkipOngoing() {
    skipOngoing.value = !skipOngoing.value
  }

  function setLanguage(lang: Language) {
    language.value = lang
  }

  function resetToDefaults() {
    cps.value = 50
    voiceEnabled.value = false
    autoAdvance.value = false
    skipOngoing.value = false
  }

  return {
    // State
    cps,
    voiceEnabled,
    autoAdvance,
    skipOngoing,
    language,
    // Actions
    setCps,
    toggleVoice,
    toggleAutoAdvance,
    toggleSkipOngoing,
    setLanguage,
    resetToDefaults,
  }
})
