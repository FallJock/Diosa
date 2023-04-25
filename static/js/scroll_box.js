
    //прокрутка
    let left = dvig.clientLeft;
dvigr.onclick = function() {
    if (dvig.clientWidth + (left - caps2.clientWidth) >= caps2.clientWidth) {
    left -= caps2.clientWidth;} 
    else if (dvig.clientWidth + (left - (caps2.clientWidth / 3 * 2)) >= caps2.clientWidth) {
        left -= (caps2.clientWidth / 3 * 2);}
    else if (dvig.clientWidth + (left - (caps2.clientWidth / 3)) >= caps2.clientWidth) {
        left -= (caps2.clientWidth / 3);}
    else if (dvig.clientWidth + left + caps2.clientWidth > 0) {
        left -= dvig.clientWidth + left - caps2.clientWidth;}
 dvig.style.left = left + "px";
}
dvigl.onclick = function() {
    if (dvig.clientWidth - (left + caps2.clientWidth) >= dvig.clientWidth) {
    left += caps2.clientWidth;} 
    else if (dvig.clientWidth - (left + (caps2.clientWidth / 3 * 2)) >= dvig.clientWidth) {
        left += (caps2.clientWidth / 3 * 2);}
    else if (dvig.clientWidth - (left + (caps2.clientWidth / 3)) >= dvig.clientWidth) {
        left += (caps2.clientWidth / 3);}
    else if (dvig.clientWidth - left - caps2.clientWidth <= 0) {
        left -= dvig.clientWidth - left + caps2.clientWidth;}
 dvig.style.left = left + "px";
}

