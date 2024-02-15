package io.hadooplex.search.model.entity;

import javax.persistence.Entity;
import javax.persistence.Id;

import javax.persistence.Table;

@Entity
@Table(name = "palabras")
public class Palabra {

    @Id
    private String palabra;

    private String ids;

    public Palabra() {
    }

    public Palabra(String palabra, String ids) {
        this.palabra = palabra;
        this.ids = ids;
    }

    public String getPalabra() {
        return palabra;
    }

    public String getIds() {
        return ids;
    }

    public void setPalabra(String palabra) {
        this.palabra = palabra;
    }

    public void setIds(String ids) {
        this.ids = ids;
    }

}
