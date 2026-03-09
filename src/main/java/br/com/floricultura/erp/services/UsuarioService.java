package br.com.floricultura.erp.services;
import br.com.floricultura.erp.model.Usuario;
import br.com.floricultura.erp.repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;
@Service
@RequiredArgsConstructor
public class UsuarioService {
    private final UsuarioRepository repository;
    private final PasswordEncoder passwordEncoder;
    public List<Usuario> listarTodos() { return repository.findAll(); }
    public Usuario salvar(Usuario usuario) {
        usuario.setSenha(passwordEncoder.encode(usuario.getSenha()));
        return repository.save(usuario);
    }
    public Optional<Usuario> buscarPorId(Long id) { return repository.findById(id); }
    public void excluir(Long id) { repository.deleteById(id); }
}