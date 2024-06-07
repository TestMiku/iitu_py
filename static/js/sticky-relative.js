
function stickyRelativeUpdatePositions(relativeElement = null) {
    for (const stickyRelative of (relativeElement || document).getElementsByClassName("sticky-relative")) {
        const offsetParent = $(stickyRelative).offsetParent()[0];
        if (offsetParent) {
            const offsetParentDomRect = offsetParent.getBoundingClientRect();
            const stickyRelativeDomRect = stickyRelative.getBoundingClientRect();
            if (stickyRelative.classList.contains("sticky-relative-left")) {
                const left = stickyRelativeDomRect.x - offsetParentDomRect.x;
                stickyRelative.style.left = `${left}px`;
            }
            if (stickyRelative.classList.contains("sticky-relative-top")) {
                const top = stickyRelativeDomRect.y - offsetParentDomRect.y;
                stickyRelative.style.top = `${top}px`;
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    stickyRelativeUpdatePositions();
});