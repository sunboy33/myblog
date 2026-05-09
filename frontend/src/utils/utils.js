import CryptoJS from 'crypto-js'


const CRYPTOJS_KEY = import.meta.env.VITE_CRYPTOJS_KEY



const encrypt = (password) => {
    const t = {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    }
    const a = CryptoJS.enc.Utf8.parse(CRYPTOJS_KEY)
    const n = CryptoJS.AES.encrypt(password, a, t)
    return n.toString().replace(/\//g, '_').replace(/\+/g, '-')
}



export { encrypt }