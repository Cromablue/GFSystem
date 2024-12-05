describe('Login', () => {
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000//login'); // Substitua pelo caminho do login
  });

  it('Deve exibir a página de login corretamente', () => {
    cy.get('h1').should('contain', 'Login');
    cy.get('input[name="username"]').should('exist');
    cy.get('input[name="password"]').should('exist');
    cy.get('button[type="submit"]').should('contain', 'Entrar');
  });

  it('Deve fazer login com credenciais válidas', () => {
    cy.get('input[name="username"]').type('usuario_teste');
    cy.get('input[name="password"]').type('senha_teste{enter}');
    cy.url().should('include', '/perfil');
    cy.get('.welcome-message').should('contain', 'Bem-vindo, usuario_teste');
  });

  it('Deve exibir erro com credenciais inválidas', () => {
    cy.get('input[name="username"]').type('usuario_invalido');
    cy.get('input[name="password"]').type('senha_errada{enter}');
    cy.get('.alert').should('contain', 'Credenciais inválidas');
  });
});
