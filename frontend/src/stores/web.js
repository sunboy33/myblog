import { defineStore } from "pinia"
import { ref } from "vue"
import { showError } from "@/utils/message.js"
import { getWebSettings } from "@/api/index.js"


export const webSettingStore = defineStore("webSetting", {
    state: () => ({
        title: '',
        poem: '',
        bgImage: '',
        copyright: '',
        contactEmail: '',
        icpNumber: ''
    }),
    actions: {
        async initialize() {
            const res = await getWebSettings()
            const data = res.data.data
            this.poem = data.poem
            this.title = data.title
            this.bgImage = data.backGroundPreview
            this.contactEmail = data.contactEmail,
            this.icpNumber = data.icpNumber,
            this.copyright = data.copyright

        }
    }
})
