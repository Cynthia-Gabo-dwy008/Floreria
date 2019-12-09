class usuario {
    nombre;
    correo;
    mensaje;

    setNombre(nombre) {
        this.nombre = nombre;
    }

    setCorreo(correo) {
        this.correo = correo;
    }

    setMensaje(mensaje) {
        this.mensaje = mensaje;
    }

    getNombre() {
        return this.nombre;
    }

    getCorreo() {
        return this.Correo;
    }

    getMensaje() {
        return this.mensaje;
    }

    imprimir() {
        return "Nombre: " + this.getNombre() + "Correo: " + this.getCorreo() + "Mensaje : " + this.getMensaje();
    }
}