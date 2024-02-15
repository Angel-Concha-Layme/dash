package io.hadooplex.search.model.entity;

import javax.persistence.Id;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name = "ids_documentos")
public class Documento {
    @Id
    private Integer id;

    @Column(name = "nombre_documento")
    private String nombreDocumento;

    public Documento() {
    }

    public Documento(Integer id, String nombreDocumento) {
        this.id = id;
        this.nombreDocumento = nombreDocumento;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNombreDocumento() {
        return nombreDocumento;
    }

    public void setNombreDocumento(String nombreDocumento) {
        this.nombreDocumento = nombreDocumento;
    }
}
