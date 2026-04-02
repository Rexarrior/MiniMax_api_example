import { createRouter, createWebHistory } from 'vue-router'
import TitleScreen from '@/components/TitleScreen.vue'
import GameScreen from '@/components/GameScreen.vue'
import EndingScreen from '@/components/EndingScreen.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'title',
      component: TitleScreen
    },
    {
      path: '/play',
      name: 'game',
      component: GameScreen
    },
    {
      path: '/ending',
      name: 'ending',
      component: EndingScreen
    }
  ]
})

export default router