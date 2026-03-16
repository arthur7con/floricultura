package br.com.floricultura.erp.controller;

import br.com.floricultura.erp.model.Usuario;
import br.com.floricultura.erp.security.TokenService;
import br.com.floricultura.erp.security.dto.AuthenticationDTO;
import br.com.floricultura.erp.security.dto.LoginResponseDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthenticationController {

    @Autowired private AuthenticationManager authenticationManager;
    @Autowired private TokenService tokenService;

    @PostMapping("/login")
    public ResponseEntity<LoginResponseDTO> login(
            @RequestBody AuthenticationDTO data) {

        var credentials = new UsernamePasswordAuthenticationToken(
                data.email(), data.senha());

        var auth = authenticationManager.authenticate(credentials);

        var token = tokenService.generateToken((Usuario) auth.getPrincipal());

        return ResponseEntity.ok(new LoginResponseDTO(token));
    }
}