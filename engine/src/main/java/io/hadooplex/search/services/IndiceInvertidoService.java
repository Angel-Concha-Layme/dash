package io.hadooplex.search.services;

import java.io.IOException;
import java.util.List;
import java.util.Map;

import javax.persistence.EntityManager;

import io.hadooplex.search.model.entity.Documento;
import io.hadooplex.search.model.entity.Palabra;
import io.hadooplex.search.utils.IndiceInvertidoParse;
import io.hadooplex.search.utils.JPAUtil;

public class IndiceInvertidoService {

    public void insertarDatos(String archivoIds, String archivoPalabras) throws IOException {
        EntityManager em = JPAUtil.getEntityManager();
        em.getTransaction().begin();

        try {
            Map<String, Documento> documentos = IndiceInvertidoParse.parseDocumentos(archivoIds);
            for (Documento doc : documentos.values()) {
                em.persist(doc);
            }

            List<Palabra> palabras = IndiceInvertidoParse.parsePalabras(archivoPalabras, documentos);
            for (Palabra palabra : palabras) {
                em.persist(palabra);
            }

            em.getTransaction().commit();
        } finally {
            em.close();
        }
    }
}