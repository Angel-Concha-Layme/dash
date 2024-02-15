package io.hadooplex.search.utils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import io.hadooplex.search.model.entity.Documento;
import io.hadooplex.search.model.entity.Palabra;

public class IndiceInvertidoParse {

    public static Map<String, Documento> parseDocumentos(String archivo) throws IOException {
        Map<String, Documento> documentos = new HashMap<>();
        List<String> lineas = Files.readAllLines(Paths.get(archivo));

        for (String linea : lineas) {
            String[] partes = linea.split("\\t");
            if (partes.length != 2) {
                System.out
                        .println("Advertencia: La línea '" + linea + "' no tiene el formato correcto y será omitida.");
                continue;
            }

            Documento documento = new Documento();
            documento.setId(Integer.parseInt(partes[1].trim()));
            documento.setNombreDocumento(partes[0]); // ¡No olvides esta línea!
            documentos.put(partes[0], documento);
        }

        return documentos;
    }

    public static List<Palabra> parsePalabras(String archivo, Map<String, Documento> documentos) throws IOException {
        List<Palabra> palabras = new ArrayList<>();
        List<String> lineas = Files.readAllLines(Paths.get(archivo));

        for (String linea : lineas) {
            String[] partes = linea.split("\\s+", 2); // Dividir por espacios en blanco

            if (partes.length != 2) {
                System.out
                        .println("Advertencia: La línea '" + linea + "' no tiene el formato correcto y será omitida.");
                continue;
            }

            Palabra palabra = new Palabra();
            palabra.setPalabra(partes[0]);
            palabra.setIds(partes[1]);
            palabras.add(palabra);
        }

        return palabras;
    }
}