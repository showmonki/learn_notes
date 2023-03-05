import * as Vue from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue';

// Vue.use(Router)
const router = createRouter({
    history: createWebHistory(),
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        }
    ]
});
export default router;