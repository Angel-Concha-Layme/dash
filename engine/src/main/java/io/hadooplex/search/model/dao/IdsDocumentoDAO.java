package io.hadooplex.search.model.dao;

import javax.persistence.EntityManager;

import io.hadooplex.search.model.entity.Documento;

public class IdsDocumentoDAO {
    private EntityManager em;

    public IdsDocumentoDAO(EntityManager em) {
        this.em = em;
    }

    public void guardar(Documento documento) {
        em.persist(documento);
    }

}
