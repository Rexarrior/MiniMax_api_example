import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Title',
    component: () => import('../components/ui/TitleScreen.vue'),
  },
  {
    path: '/play/:storyId',
    name: 'Game',
    component: () => import('../components/game/GameScreen.vue'),
    props: true,
  },
  {
    path: '/ending',
    name: 'Ending',
    component: () => import('../components/game/EndingScreen.vue'),
  },
  {
    path: '/tests/image',
    name: 'TestImage',
    component: () => import('../pages/tests/ImageTest.vue'),
  },
  {
    path: '/tests/video',
    name: 'TestVideo',
    component: () => import('../pages/tests/VideoTest.vue'),
  },
  {
    path: '/tests/soundtrack',
    name: 'TestSoundtrack',
    component: () => import('../pages/tests/SoundtrackTest.vue'),
  },
  {
    path: '/tests/replica',
    name: 'TestReplica',
    component: () => import('../pages/tests/ReplicaTest.vue'),
  },
  {
    path: '/tests',
    name: 'TestsIndex',
    component: () => import('../pages/tests/TestsIndex.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router