package io.hadooplex.search.controller;

import java.io.IOException;

import io.hadooplex.search.services.IndiceInvertidoService;

public class IndiceInvertidoController {

    private final IndiceInvertidoService service;

    public IndiceInvertidoController() {
        this.service = new IndiceInvertidoService();
    }

    public void insertarDatosController(String archivoIds, String archivoPalabras) {
        try {
            try {
                service.insertarDatos(archivoIds, archivoPalabras);
            } catch (IOException e) {

                e.printStackTrace();
            }
            System.out.println("Datos insertados exitosamente!");
        } catch (RuntimeException e) {
            System.err.println("Error al insertar datos: " + e.getMessage());
            e.printStackTrace();
        }
    }
}