"""
Página de login simples.
"""
import streamlit as st
from auth import AuthManager


def show_login_page(auth_manager: AuthManager):
    """
    Exibe a página de login.

    Args:
        auth_manager: Instância do gerenciador de autenticação
    """
    # Centralizar o formulário
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🔐 Login")
        st.write("Acesse o sistema de consulta de Normas Técnicas CBMGO")

        # Formulário de login
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input(
                "Usuário",
                placeholder="Digite seu usuário",
            )

            password = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
            )

            submit_button = st.form_submit_button(
                "Entrar",
                use_container_width=True
            )

            if submit_button:
                if not username or not password:
                    st.error("Por favor, preencha todos os campos.")
                else:
                    if auth_manager.login(username, password):
                        st.success(f"Bem-vindo, {username}!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")

        st.caption("🔒 Suas credenciais são verificadas de forma segura.")
