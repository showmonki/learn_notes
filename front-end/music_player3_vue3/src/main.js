import { createApp } from 'vue';
import App from './App.vue';
import router from "./router";
import store from './store'

const app = createApp(App);

// app.use({
//     router,
//     store,
//     render: h => h(App)
// }).mount('#app');
app.use(router).use(store).mount('#app');