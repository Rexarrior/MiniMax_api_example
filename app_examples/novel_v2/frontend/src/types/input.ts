export type InputMode = 'keyboard' | 'voice' | 'gamepad'

export interface KeyboardState {
  enterPressed: boolean
  numberKeys: number[]
}

export interface VoiceInputState {
  isListening: boolean
  isSupported: boolean
  lastResult: string | null
}

export interface GamepadState {
  isSupported: boolean
  lastButton: string | null
}
