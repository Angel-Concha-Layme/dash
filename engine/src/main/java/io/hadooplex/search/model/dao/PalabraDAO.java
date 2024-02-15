package io.hadooplex.search.model.dao;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;

import io.hadooplex.search.model.entity.Documento;
import io.hadooplex.search.model.entity.Palabra;

public class PalabraDAO {
    private EntityManager em;

    public PalabraDAO(EntityManager em) {
        this.em = em;
    }

    public void guardar(Palabra palabra) {
        em.persist(palabra);
    }

    public List<String> obtenerNombresDeDocumentosParaPalabra(Palabra palabra) {
        List<String> nombresDocumentos = new ArrayList<>();

        // Convertir el string de ids a una lista de enteros
        String[] idsArray = palabra.getIds().split(",");
        List<Integer> idsList = Arrays.stream(idsArray)
                .map(String::trim)
                .map(Integer::parseInt)
                .collect(Collectors.toList());

        // Obtener los nombres de los documentos usando los IDs
        TypedQuery<String> query = em.createQuery(
                "SELECT d.nombreDocumento FROM Documento d WHERE d.ID IN :ids",
                String.class);
        query.setParameter("ids", idsList);
        nombresDocumentos.addAll(query.getResultList());

        return nombresDocumentos;
    }

    public List<Palabra> buscarPalabrasConSubstring(String substring) {
        return em.createQuery("FROM Palabra p WHERE p.palabra LIKE :substring", Palabra.class)
                .setParameter("substring", "%" + substring + "%")
                .getResultList();
    }

    public List<Documento> obtenerDocumentosParaPalabra(Palabra palabra) {
        // Convertir el string de ids a una lista de enteros
        String[] idsArray = palabra.getIds().split(",");
        List<Integer> idsList = Arrays.stream(idsArray)
                .map(String::trim)
                .map(Integer::parseInt)
                .collect(Collectors.toList());

        // Obtener los documentos usando los IDs
        TypedQuery<Documento> query = em.createQuery(
                "SELECT d FROM Documento d WHERE d.id IN :ids",
                Documento.class);
        query.setParameter("ids", idsList);

        return query.getResultList();
    }

    public List<Palabra> buscarPorConsulta(String query) {
        TypedQuery<Palabra> palabrasQuery = em.createQuery(
                "SELECT p FROM Palabra p WHERE p.palabra LIKE :query",
                Palabra.class);
        palabrasQuery.setParameter("query", "%" + query + "%");
        List<Palabra> palabras = palabrasQuery.getResultList();

        return palabras;
    }

    public List<Documento> getDocumentosPorPalabra(Palabra palabra) {
        String[] idsArray = palabra.getIds().split(",");
        List<Integer> idsList = Arrays.stream(idsArray)
                .map(String::trim)
                .map(Integer::parseInt)
                .collect(Collectors.toList());

        // Obtener los documentos usando los IDs
        TypedQuery<Documento> query = em.createQuery(
                "SELECT d FROM Documento d WHERE d.id IN :ids",
                Documento.class);
        query.setParameter("ids", idsList);

        return query.getResultList();
    }

    public List<Integer> convertIdsStringToList(String ids) {
        return Arrays.stream(ids.split(","))
                .map(String::trim)
                .map(Integer::parseInt)
                .collect(Collectors.toList());
    }

    public List<Integer> obtenerDocumentosConTodasLasPalabras(String consulta) {
        String[] palabras = consulta.split("\\s+"); // Divide el string por espacios

        List<Set<Integer>> listasDeIds = new ArrayList<>();

        for (String palabra : palabras) {
            List<Integer> idsParaPalabra = obtenerIdsParaPalabra(palabra);
            listasDeIds.add(new HashSet<>(idsParaPalabra));
        }

        // Intersecta todas las listas
        Set<Integer> intersection = listasDeIds.get(0);
        for (int i = 1; i < listasDeIds.size(); i++) {
            intersection.retainAll(listasDeIds.get(i));
        }

        return new ArrayList<>(intersection);
    }

    private List<Integer> obtenerIdsParaPalabra(String palabra) {
        TypedQuery<Palabra> query = em.createQuery(
                "SELECT p FROM Palabra p WHERE p.palabra = :palabra",
                Palabra.class);
        query.setParameter("palabra", palabra);
        Palabra result = query.getSingleResult(); // Asume que la palabra es única en la base de datos

        return convertIdsStringToList(result.getIds());
    }

    public List<Documento> getDocumentosPorIds(List<Integer> ids) {
        if (ids == null || ids.isEmpty()) {
            return new ArrayList<>();
        }

        TypedQuery<Documento> query = em.createQuery(
                "SELECT d FROM Documento d WHERE d.id IN :ids",
                Documento.class);
        query.setParameter("ids", ids);

        return query.getResultList();
    }

}