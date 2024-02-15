package io.hadooplex.search.utils;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

public class JPAUtil {
    private static EntityManagerFactory FACTORY = Persistence.createEntityManagerFactory("indice_invertido_mediano");

    public static EntityManager getEntityManager() {
        return FACTORY.createEntityManager();
    }
}
