import { ElMessage } from 'element-plus'


/** 显示错误信息 */
const showError = (message) => {
    ElMessage.error({
        message,
        duration: 3000,
        showClose: false,
        offset: 60,
        grouping: true
    })
}

/** 显示成功信息 */
const showSuccess = (message) => {
    ElMessage.success({
        message,
        duration: 3000,
        showClose: false,
        offset: 60,
        grouping: true
    })
}

/** 显示警告信息 */
const showWarning = (message) => {
    ElMessage.warning({
        message,
        duration: 3000,
        showClose: false,
        offset: 60,
        grouping: true
    })
}

/** 显示提示信息 */
const showInfo = (message) => {
    ElMessage.info({
        message,
        duration: 3000,
        showClose: false,
        offset: 60,
        grouping: true
    })
}

export { showError, showSuccess, showWarning, showInfo}

