var currentTab = 0;
function showTab(t) {
    var e = document.getElementsByClassName("tab");
    e[t].style.display = "block",
    document.getElementById("prevBtn").style.display = 0 == t ? "none": "inline",
    t == e.length - 1 ? document.getElementById("nextBtn").innerHTML = "등록하기": document.getElementById("nextBtn").innerHTML = "다음으로"
}
function nextPrev(t) {
    var e = document.getElementsByClassName("tab");
    return ! (1 == t && !validateForm()) && (temp_currentTab = currentTab + t, temp_currentTab >= e.length ? ($("form").submit(), !1) : (e[currentTab].style.display = "none", void showTab(currentTab += t)))
}
function validateForm() {
    document.getElementsByClassName("tab")[currentTab].getElementsByTagName("input");
    return ! 0
}
$(document).ready(function(){
    showTab(currentTab);
});