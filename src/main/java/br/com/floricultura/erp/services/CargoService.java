package br.com.floricultura.erp.services;

import br.com.floricultura.erp.model.Cargo;
import br.com.floricultura.erp.repository.CargoRepository;
import br.com.floricultura.erp.async.CargoAuditLogger;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CargoService {

    private final CargoRepository repository;
    private final CargoAuditLogger auditLogger;

    public List<Cargo> listarTodos() {
        return repository.findAll();
    }

    public Cargo buscarPorId(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("ID inválido: " + id));
    }

    public Cargo salvar(Cargo cargo) {
        Cargo savedCargo = repository.save(cargo);
        auditLogger.logCargoCreation(savedCargo);
        return savedCargo;
    }

    public void excluir(Long id) {
        repository.deleteById(id);
    }
}