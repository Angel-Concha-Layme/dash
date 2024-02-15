package io.hadooplex.search.view;

import io.hadooplex.search.model.dao.PalabraDAO;
import io.hadooplex.search.model.entity.Documento;
import io.hadooplex.search.utils.JPAUtil;

import javax.persistence.EntityManager;
import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.util.ArrayList;
import java.util.List;

/*
 * public class MainFrame extends JFrame {
 * 
 * private JTextField searchField;
 * private JButton searchButton;
 * private JList<String> resultsList;
 * private DefaultListModel<String> listModel;
 * 
 * public MainFrame() {
 * setTitle("Motor de búsqueda");
 * setSize(600, 400);
 * setLayout(new BorderLayout());
 * setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
 * 
 * // Panel de búsqueda
 * JPanel searchPanel = new JPanel();
 * searchField = new JTextField(30);
 * searchButton = new JButton("Buscar");
 * searchButton.addActionListener(new SearchActionListener());
 * searchPanel.add(searchField);
 * searchPanel.add(searchButton);
 * 
 * // Panel de resultados
 * listModel = new DefaultListModel<>();
 * resultsList = new JList<>(listModel);
 * JScrollPane scrollPane = new JScrollPane(resultsList);
 * 
 * add(searchPanel, BorderLayout.NORTH);
 * add(scrollPane, BorderLayout.CENTER);
 * }
 * 
 * private List<String> formatResult(List<Documento> documentos) {
 * List<String> formattedNames = new ArrayList<>();
 * 
 * for (Documento doc : documentos) {
 * String formattedName = formatDocumentName(doc.getNombreDocumento());
 * formattedNames.add(formattedName);
 * }
 * 
 * return formattedNames;
 * }
 * 
 * private String formatDocumentName(String originalName) {
 * // Remover la extensión ".txt" al final
 * if (originalName.endsWith(".txt")) {
 * originalName = originalName.substring(0, originalName.length() - 4);
 * }
 * 
 * // Reemplazar todos los "_" por espacios
 * return originalName.replace("_", " ");
 * }
 * 
 * private class SearchActionListener implements ActionListener {
 * 
 * @Override
 * public void actionPerformed(ActionEvent e) {
 * // Lógica de búsqueda
 * String query = searchField.getText();
 * 
 * // Utiliza tu DAO para obtener las palabras que contienen la consulta
 * EntityManager em = JPAUtil.getEntityManager();
 * PalabraDAO palabraDAO = new PalabraDAO(em);
 * 
 * List<Palabra> palabras = palabraDAO.buscarPorConsulta(query);
 * 
 * listModel.clear(); // Limpia el modelo antes de agregar nuevos resultados
 * 
 * for (Palabra palabra : palabras) {
 * // Asumiendo que tienes una función en tu DAO que devuelva los Documentos
 * // relacionados con una Palabra
 * List<Documento> documentos = palabraDAO.getDocumentosPorPalabra(palabra);
 * 
 * List<String> formattedNames = formatResult(documentos);
 * for (String name : formattedNames) {
 * listModel.addElement(name);
 * }
 * }
 * 
 * em.close();
 * }
 * }
 * 
 * public static void main(String[] args) {
 * SwingUtilities.invokeLater(() -> {
 * new MainFrame().setVisible(true);
 * });
 * }
 * }
 * 
 * 
 */

public class MainFrame extends JFrame {

    private JTextField searchField;
    private JButton searchButton;
    private JList<String> resultsList;
    private DefaultListModel<String> listModel;

    public MainFrame() {
        try {
            for (UIManager.LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        setTitle("Motor de búsqueda");
        setSize(600, 400);
        setLayout(new BorderLayout(10, 10)); // Margen entre componentes
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Panel de búsqueda
        JPanel searchPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        searchField = new JTextField(30);
        searchField.setToolTipText("Ingresa tu búsqueda aquí");
        searchField.setForeground(Color.GRAY);
        searchField.setText("Buscar...");
        searchField.addFocusListener(new FocusAdapter() {
            @Override
            public void focusGained(FocusEvent e) {
                if ("Buscar...".equals(searchField.getText())) {
                    searchField.setText("");
                    searchField.setForeground(Color.BLACK);
                }
            }

            @Override
            public void focusLost(FocusEvent e) {
                if (searchField.getText().isEmpty()) {
                    searchField.setForeground(Color.GRAY);
                    searchField.setText("Buscar...");
                }
            }
        });

        searchButton = new JButton("Buscar");
        searchButton.addActionListener(new SearchActionListener());
        searchButton.setToolTipText("Haz clic para buscar");

        searchPanel.add(searchField);
        searchPanel.add(searchButton);

        // Panel de resultados
        listModel = new DefaultListModel<>();
        resultsList = new JList<>(listModel);
        JScrollPane scrollPane = new JScrollPane(resultsList);

        add(searchPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);

        setPadding((JComponent) getContentPane(), 10);

    }

    private void setPadding(JComponent component, int padding) {
        Border current = component.getBorder();
        Border empty = new EmptyBorder(padding, padding, padding, padding);
        component.setBorder(current == null ? empty : new CompoundBorder(empty, current));
    }

    private List<String> formatResult(List<Documento> documentos) {
        List<String> formattedNames = new ArrayList<>();

        for (Documento doc : documentos) {
            String formattedName = formatDocumentName(doc.getNombreDocumento());
            formattedNames.add(formattedName);
        }

        return formattedNames;
    }

    private String formatDocumentName(String originalName) {
        // Remover la extensión ".txt" al final
        if (originalName.endsWith(".txt")) {
            originalName = originalName.substring(0, originalName.length() - 4);
        }

        // Reemplazar todos los "_" por espacios
        return originalName.replace("_", " ");
    }

    private class SearchActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            // Lógica de búsqueda
            String query = searchField.getText();

            // Si el query es "Buscar..." o está vacío, simplemente retornar
            if (query.equals("Buscar...") || query.trim().isEmpty()) {
                return;
            }

            EntityManager em = JPAUtil.getEntityManager();
            PalabraDAO palabraDAO = new PalabraDAO(em);

            List<Integer> idsDocumentos = palabraDAO.obtenerDocumentosConTodasLasPalabras(query);

            // Obtenemos los documentos por sus IDs (necesitamos agregar este método en
            // PalabraDAO)
            List<Documento> documentos = palabraDAO.getDocumentosPorIds(idsDocumentos);

            listModel.clear(); // Limpia el modelo antes de agregar nuevos resultados

            List<String> formattedNames = formatResult(documentos);
            for (String name : formattedNames) {
                listModel.addElement(name);
            }

            em.close();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new MainFrame().setVisible(true);
        });
    }
}
