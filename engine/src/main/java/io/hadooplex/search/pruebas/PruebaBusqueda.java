package io.hadooplex.search.pruebas;

import javax.persistence.EntityManager;

import io.hadooplex.search.model.dao.PalabraDAO;
import io.hadooplex.search.utils.JPAUtil;

import java.util.List;

public class PruebaBusqueda {

    public static void main(String[] args) {
        // Inicializar el EntityManager
        EntityManager em = JPAUtil.getEntityManager();

        try {
            // Instanciar PalabraDAO
            PalabraDAO palabraDAO = new PalabraDAO(em);

            // Buscar documentos con las palabras "love" y "power"
            List<Integer> idsDocumentos = palabraDAO
                    .obtenerDocumentosConTodasLasPalabras("Spero equidem quod gloriam eorum");

            // Imprimir los resultados
            if (idsDocumentos.isEmpty()) {
                System.out.println("No se encontraron documentos que contengan las palabras 'love' y 'power'.");
            } else {
                System.out.println("Documentos que contienen las palabras 'love' y 'power': ");
                for (Integer id : idsDocumentos) {
                    System.out.println("Documento ID: " + id);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // Cerrar el EntityManager
            em.close();
        }
    }
}
