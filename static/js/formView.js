let position = 1; // Estado inicial

function changeState() {
        position = (position % 3) + 1; // Alternar entre 1, 2 y 3

        // Mover el slider a la posición correcta
        let slider = document.getElementById("slider");
        slider.style.transform = `translateX(${(position - 1) * 40}px)`;

        // Ocultar todos los contenidos
        document.querySelectorAll('.content').forEach(el => el.classList.remove('active'));

        // Mostrar el contenido correspondiente
        document.getElementById("content" + position).classList.add('active');
}