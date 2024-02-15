package io.hadooplex.search.main;

import io.hadooplex.search.controller.IndiceInvertidoController;

public class insertApp {
    public static void main(String[] args) {
        IndiceInvertidoController controller = new IndiceInvertidoController();
        controller.insertarDatosController("D:\\PROYECTOS ACADEMICOS\\hadoop-search-engine\\data\\Big\\IDs",
                "D:\\PROYECTOS ACADEMICOS\\hadoop-search-engine\\data\\Big\\indice");
    }
}