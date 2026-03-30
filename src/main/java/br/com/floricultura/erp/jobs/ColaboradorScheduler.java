package br.com.floricultura.erp.jobs;
import br.com.floricultura.erp.model.Colaborador;
import br.com.floricultura.erp.repository.ColaboradorRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import java.time.LocalDate;
import java.util.List;
@Component
@RequiredArgsConstructor
@Slf4j
public class ColaboradorScheduler {
    private final ColaboradorRepository colaboradorRepository;
    @Scheduled(cron = "0 0 8 * * *")
    public void verificarAniversariantes() {
        log.info("Iniciando verificação de aniversariantes do dia...");
        LocalDate hoje = LocalDate.now();
        List<Colaborador> aniversariantes =
                colaboradorRepository.findByDataNascimentoMonthAndDay(hoje.getMonthValue(), hoje.getDayOfMonth());
        if (aniversariantes.isEmpty()) {
            log.info("Nenhum colaborador aniversariante hoje.");
        } else {
            aniversariantes.forEach(colaborador -> {
                log.info("🎉 Parabéns, {}! Aniversário de {} hoje.", colaborador.getNome(), colaborador.getNome());
            });
        }
        log.info("Verificação de aniversariantes concluída.");
    }
    @Scheduled(fixedRate = 1800000)
    public void verificarStatusContratos() {
        log.info("Iniciando verificação de status de contratos de colaboradores...");
        List<Colaborador> colaboradoresComContratosPendentes = colaboradorRepository.findAll();
        colaboradoresComContratosPendentes.stream()
                .filter(c -> c.getDataContratacao() != null &&
                        c.getDataContratacao().plusYears(1).isBefore(LocalDate.now()))
                .forEach(colaborador -> {
                    log.warn("⚠️ Contrato do colaborador {} (ID: {}) pode precisar de atenção. Data de contratação: {}",
                            colaborador.getNome(), colaborador.getId(), colaborador.getDataContratacao());
                });
        log.info("Verificação de status de contratos concluída.");
    }
}