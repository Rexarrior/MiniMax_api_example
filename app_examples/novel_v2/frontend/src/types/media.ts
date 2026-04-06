export type MediaType = 'image' | 'audio' | 'video'

export interface AudioTrack {
  url: string
  type: 'music' | 'voice' | 'sfx'
  volume: number
  loop: boolean
}

export interface MediaState {
  isMuted: boolean
  musicVolume: number
  voiceVolume: number
  sfxVolume: number
  currentMusic: string | null
  isMusicPlaying: boolean
}

export interface VideoState {
  isPlaying: boolean
  currentVideo: string | null
  isFullscreen: boolean
}
