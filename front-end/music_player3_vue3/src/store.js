import { createApp } from "vue";

import Vuex from 'vuex'

// createApp.use(Vuex)

const COVER_URL = [
    new URL('https://p1.music.126.net/JyOMeV3PyJoC5x4mhedqcA==/109951166231841225.jpg').href,
    new URL('https://p1.music.126.net/sjZiF_jNwV64iy0FriQNOA==/109951165936889906.jpg').href,
    new URL('https://p1.music.126.net/BIfWzfoCZtGVbHmwIl0osQ==/109951167304704301.jpg').href
]

export default new Vuex.Store({
    state: {
        isPlaying: false,
        coverUrl: ''
    },
    getters: {},
    mutations: {
        togglePlay (state, toggle) {
            state.isPlaying = toggle !== undefined ? toggle : !state.isPlaying
        },
        changeCover (state) {
            while (1) {
                const index = Math.floor(Math.random() * 3)
                const coverUrl = COVER_URL[index]
                if (coverUrl !== state.coverUrl) {
                    state.coverUrl = coverUrl
                    break
                }
            }
        }
    },
    actions: {}
})