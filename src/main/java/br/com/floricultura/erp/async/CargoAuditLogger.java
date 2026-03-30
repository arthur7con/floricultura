package br.com.floricultura.erp.async;

import br.com.floricultura.erp.model.Cargo;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class CargoAuditLogger {

    @Async
    public void logCargoCreation(Cargo cargo) {
        try {
            Thread.sleep(2000);

            log.info("AUDITORIA ASSÍNCRONA: Novo cargo criado - ID: {}, Nome: {}",
                    cargo.getId(), cargo.getNomeCargo());

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.error("Erro durante o log de auditoria assíncrono para o cargo {}: {}",
                    cargo.getNomeCargo(), e.getMessage());
        }
    }
}