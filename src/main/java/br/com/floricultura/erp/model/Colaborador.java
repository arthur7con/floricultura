package br.com.floricultura.erp.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "COLABORADOR")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Colaborador {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String matricula;

    @Column(nullable = false)
    private String nome;

    @Column(nullable = false, unique = true)
    private String cpf;

    @Column(nullable = false)
    private BigDecimal salario;

    @OneToOne
    @JoinColumn(name = "FK_IdUsuario", referencedColumnName = "id", unique = true)
    private Usuario usuario;

    @ManyToOne
    @JoinColumn(name = "FK_IdCargo", referencedColumnName = "id")
    private Cargo cargo;

    private LocalDate dataNascimento;
    private LocalDate dataContratacao;
}