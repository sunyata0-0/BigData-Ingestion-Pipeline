const viewer = document.getElementById("svgViewer");
const img = document.getElementById("nifiSvg");

let scale = 0.28;
let x = 20;
let y = 20;

let dragging = false;
let startX = 0;
let startY = 0;

function update() {
    img.style.transform =
        `translate(${x}px, ${y}px) scale(${scale})`;
}

viewer.addEventListener("wheel", e => {

    e.preventDefault();

    const zoom = e.deltaY < 0 ? 1.1 : 0.9;

    scale *= zoom;

    scale = Math.min(Math.max(scale,0.1),4);

    update();

}, { passive: false });

viewer.addEventListener("mousedown", e => {

    dragging = true;

    startX = e.clientX - x;
    startY = e.clientY - y;

});

window.addEventListener("mouseup", () => {

    dragging = false;

});

window.addEventListener("mousemove", e => {

    if(!dragging) return;

    x = e.clientX - startX;
    y = e.clientY - startY;

    update();

});

update();