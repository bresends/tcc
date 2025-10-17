"""
Sistema de autenticação simples usando session_state.
"""
import streamlit as st
import hashlib
import os


class AuthManager:
    """Gerenciador de autenticação simples."""

    def __init__(self):
        # Carrega credenciais do .env
        self.username = os.getenv("STREAMLIT_USERNAME")
        self.password_hash = os.getenv("STREAMLIT_PASSWORD_HASH")

        if not self.username or not self.password_hash:
            raise ValueError(
                "STREAMLIT_USERNAME e STREAMLIT_PASSWORD_HASH devem estar definidos no .env"
            )

    def _hash_password(self, password: str) -> str:
        """Gera hash SHA256 da senha."""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> bool:
        """
        Autentica o usuário.

        Args:
            username: Nome de usuário
            password: Senha do usuário

        Returns:
            True se login bem-sucedido, False caso contrário
        """
        # Verifica se o usuário corresponde
        if username != self.username:
            return False

        # Verifica a senha
        password_hash = self._hash_password(password)
        if password_hash != self.password_hash:
            return False

        # Atualiza session state
        st.session_state.authenticated = True
        st.session_state.username = username

        return True

    def logout(self):
        """Remove autenticação."""
        st.session_state.authenticated = False
        st.session_state.username = None

    def is_authenticated(self) -> bool:
        """Verifica se o usuário está autenticado."""
        return st.session_state.get("authenticated", False)

    def get_current_user(self) -> str:
        """Retorna o nome do usuário autenticado."""
        return st.session_state.get("username", "")
