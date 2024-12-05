describe('Visualizar Perfil', () => {
  beforeEach(() => {
    cy.visit('/login');
    cy.get('input[name="username"]').type('usuario_teste');
    cy.get('input[name="password"]').type('senha_teste{enter}');
    cy.visit('http://127.0.0.1:8000/perfil');
  });

  it('Deve exibir as informações do perfil corretamente', () => {
    cy.get('.profile-picture img').should('have.attr', 'src').and('include', 'profile_pics/');
    cy.get('.user-fullname').should('contain', 'Usuario Teste');
    cy.get('.user-telefone').should('contain', '123456789');
    cy.get('.user-endereco').should('contain', 'Rua Exemplo, 123');
  });
});
