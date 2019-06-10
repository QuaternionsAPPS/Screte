function switch_log() {

    let log_el = document.getElementById("log_in");
    let reg_el = document.getElementById("sign_up");
    let switcher = document.getElementById("dot_log_switch");

    if (! log_el.style.opacity) {
        log_el.style.opacity = getComputedStyle(log_el).opacity;
        reg_el.style.opacity = getComputedStyle(reg_el).opacity;
        switcher.style.borderBottomColor = getComputedStyle(switcher).borderBottomColor;
        switcher.style.borderTopColor = getComputedStyle(switcher).borderTopColor;
    }
    log_el.style.opacity = [reg_el.style.opacity, reg_el.style.opacity = log_el.style.opacity][0];
    switcher.style.borderBottomColor = [switcher.style.borderTopColor, switcher.style.borderTopColor = switcher.style.borderBottomColor][0];

}