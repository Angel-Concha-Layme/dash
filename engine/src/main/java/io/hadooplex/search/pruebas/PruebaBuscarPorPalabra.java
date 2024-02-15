package io.hadooplex.search.pruebas;

import java.util.List;

import javax.persistence.EntityManager;

import io.hadooplex.search.model.dao.PalabraDAO;
import io.hadooplex.search.model.entity.Documento;
import io.hadooplex.search.model.entity.Palabra;
import io.hadooplex.search.utils.JPAUtil;

public class PruebaBuscarPorPalabra {
    public static void main(String[] args) {
        EntityManager em = JPAUtil.getEntityManager();
        PalabraDAO palabraDAO = new PalabraDAO(em);
        List<Palabra> palabras = palabraDAO.buscarPalabrasConSubstring("tech");

        for (Palabra palabraObj : palabras) {
            System.out.println("Palabra: " + palabraObj.getPalabra());
            List<Documento> documentos = palabraDAO.obtenerDocumentosParaPalabra(palabraObj);
            documentos.forEach(doc -> System.out
                    .println("\tDocumento ID: " + doc.getId() + ", Nombre: " + doc.getNombreDocumento()));
        }

        em.close();
    }

}
