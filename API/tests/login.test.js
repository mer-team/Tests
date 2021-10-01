const app = require('../index');
const supertest = require('supertest')
const request = supertest(app);


describe('Login Test', () => {
  it('Erros nas credenciais de autenticação', async () => {
    const res = await request.post('/auth/login')
      .send({
        username: "usernameErrado",
        hashPassword: "passwordErrada"
      });
    expect(res.body.status).toBe("Username ou password errados");

    
  });

  it('Autenticação Correta', async () => {
    const res = await request.post('/auth/login')
      .send({
        username: "admin",
        hashPassword: "123Qwe.."
      });
    expect(res.body.status).toBe("Autenticado");
    
  });
});