import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n);

export const supported_lang = ['en'];
const browser_lang = navigator.language.split('-')[0];

let locale = 'en';
supported_lang.includes(browser_lang) && (locale = browser_lang)

export default new VueI18n({
    locale,
    silentTranslationWarn: true,
    messages: {
        en: {
            appbar: {
                home: "Home"
            },
            header: {
            },
            button: {
            }
        }
    }
})