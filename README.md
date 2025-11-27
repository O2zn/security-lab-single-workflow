# Vulnerable Security Testing Repository

Este repositório contém uma aplicação intencionalmente vulnerável e exemplos de configurações inseguras em **código de infraestrutura (IaC)** e **recursos em nuvem** (AWS e GCP).  
O objetivo é **servir como ambiente de aprendizado e teste** para ferramentas de segurança, como **Trivy**, **Gitleaks**, **Bandit** e **Semgrep**, integradas em um workflow GitHub Actions.

---

## Estrutura do Repositório

.
├── .github/workflows/security-scans.yml   # Workflow CI para rodar os scanners
├── vulnerable-app/                        # Aplicação Flask com vulnerabilidades
│   └── app.py
├── iac-terraform/                         # Exemplos de IaC vulnerável
│   ├── aws_insecure.tf
│   └── gcp_insecure.tf
└── security-reports/                      # Relatórios gerados pelos scanners

---

## Vulnerabilidades incluídas

### 1. Aplicação Flask (`vulnerable-app/app.py`)
- **Hardcoded secrets** (detectável por Gitleaks).
- **Debug mode habilitado** expondo informações internas.
- **SQL Injection** via concatenação de entrada do usuário.
- **Command Injection** usando `subprocess` com input direto.
- **Insecure Deserialization** usando `pickle.loads`.
- **Exposição de segredo em endpoint público**.
- **Insecure File Upload** sem validação de nome ou tipo.
- **Insecure TLS** (`requests.get(..., verify=False)`).

### 2. IaC Vulnerável (Terraform)

#### `iac-terraform/aws_insecure.tf`
- S3 Bucket público (`acl = "public-read"`).
- Security Group permitindo tráfego **0.0.0.0/0** para SSH e HTTP.
- IAM policy com `Action = "*"`, `Resource = "*"`.

#### `iac-terraform/gcp_insecure.tf`
- Firewall permitindo tráfego externo irrestrito (`0.0.0.0/0`).
- Bucket GCS com acesso público.
- Service Account com papel de **Owner** (permissão excessiva).

---

## Ferramentas utilizadas

# 🔒 Security Workflow - Alternativa Completa ao GitHub Advanced Security

Este workflow implementa uma solução robusta e completa de segurança para repositórios GitHub, oferecendo cobertura equivalente ou superior ao GitHub Advanced Security (GHAS) utilizando ferramentas open-source de alta qualidade.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Ferramentas Incluídas](#ferramentas-incluídas)
- [Cobertura de Segurança](#cobertura-de-segurança)
- [Instalação e Configuração](#instalação-e-configuração)
- [Configurações Opcionais](#configurações-opcionais)
- [Interpretação dos Resultados](#interpretação-dos-resultados)
- [Troubleshooting](#troubleshooting)
- [Comparação com GHAS](#comparação-com-ghas)
- [Manutenção e Atualizações](#manutenção-e-atualizações)

---

## 🎯 Visão Geral

### O que este workflow faz?

Este workflow executa **9 ferramentas de segurança diferentes** que cobrem todas as áreas críticas de segurança de aplicações:

- **SAST** (Static Application Security Testing)
- **SCA** (Software Composition Analysis)
- **Secrets Detection** (Detecção de Credenciais)
- **IaC Security** (Infrastructure as Code)
- **Container Security** (Segurança de Containers)
- **Code Quality** (Qualidade de Código)

### Quando o workflow é executado?

- ✅ **Push** em qualquer branch
- ✅ **Pull Request** em qualquer branch
- ✅ **Agendamento** diário às 2h UTC
- ✅ **Manual** via workflow_dispatch (se configurado)

---

## 🛠️ Ferramentas Incluídas

### 1. SAST (Static Application Security Testing)

#### **Semgrep** 
- **Função:** Análise estática de código para identificar vulnerabilidades
- **Rulesets utilizados:**
  - `p/security-audit` - Auditoria de segurança abrangente
  - `p/owasp-top-ten` - OWASP Top 10 vulnerabilidades
  - `p/cwe-top-25` - CWE Top 25 vulnerabilidades mais perigosas
  - `p/ci` - Regras para CI/CD
- **Linguagens suportadas:** 30+ incluindo Python, JavaScript, Java, Go, Ruby, PHP, C#, etc.
- **Equivalente GHAS:** CodeQL

#### **SonarQube Scanner** (Opcional)
- **Função:** Análise profunda de qualidade e segurança de código
- **Requer:** Token do SonarCloud ou servidor SonarQube próprio
- **Equivalente GHAS:** CodeQL (análise complementar)

### 2. SCA (Software Composition Analysis)

#### **Trivy**
- **Função:** Análise de vulnerabilidades em dependências
- **Detecta:** CVEs em bibliotecas, problemas de licenciamento
- **Suporta:** npm, pip, Maven, Go modules, RubyGems, Composer, etc.
- **Equivalente GHAS:** Dependabot

#### **OWASP Dependency-Check**
- **Função:** Identificação de dependências com vulnerabilidades conhecidas
- **Database:** National Vulnerability Database (NVD)
- **Formatos suportados:** Maven, npm, Gradle, NuGet, Ruby, Python, etc.
- **Equivalente GHAS:** Dependabot (análise complementar)

### 3. Secrets Detection

#### **Gitleaks**
- **Função:** Detecção de credenciais e secrets em código e histórico Git
- **Detecta:** API keys, tokens, senhas, chaves privadas, etc.
- **Configurável:** Suporta arquivo `.gitleaks.toml` customizado
- **Equivalente GHAS:** Secret Scanning

#### **TruffleHog**
- **Função:** Detecção avançada de secrets com verificação de entropia
- **Diferencial:** Verifica se secrets estão ativos
- **Complemento:** Maior cobertura junto com Gitleaks
- **Equivalente GHAS:** Secret Scanning (cobertura expandida)

### 4. IaC Security (Infrastructure as Code)

#### **Trivy Config**
- **Função:** Análise de segurança em arquivos IaC
- **Suporta:** Kubernetes, Docker, Terraform, CloudFormation, etc.
- **Equivalente GHAS:** CodeQL (para IaC)

#### **Checkov**
- **Função:** Scanner de IaC focado em compliance e best practices
- **Suporta:** Terraform, CloudFormation, Kubernetes, ARM, Serverless, etc.
- **Frameworks:** 1000+ regras baseadas em benchmarks (CIS, PCI-DSS, HIPAA)
- **Equivalente GHAS:** CodeQL + custom queries

#### **KICS**
- **Função:** Scanner de IaC da Checkmarx
- **Suporta:** Terraform, Kubernetes, Docker, Ansible, CloudFormation, etc.
- **Regras:** 2000+ queries de segurança
- **Equivalente GHAS:** CodeQL + custom queries

### 5. Container Security

#### **Trivy Image**
- **Função:** Análise de vulnerabilidades em imagens Docker
- **Detecta:** CVEs em OS packages e dependências de aplicação
- **Equivalente GHAS:** Container Scanning (GitHub Packages)

#### **Grype**
- **Função:** Scanner de vulnerabilidades da Anchore
- **Diferencial:** Database de vulnerabilidades atualizado diariamente
- **Complemento:** Segunda opinião junto com Trivy
- **Equivalente GHAS:** Container Scanning

### 6. Code Quality

#### **Lizard**
- **Função:** Análise de complexidade ciclomática
- **Métricas:** CCN (Cyclomatic Complexity Number), NLOC, token count
- **Objetivo:** Identificar código complexo e difícil de manter
- **Complemento:** Indicador indireto de possíveis vulnerabilidades

---

## 🎯 Cobertura de Segurança

### Comparação de Cobertura

| Categoria | GHAS | Este Workflow |
|-----------|------|---------------|
| **SAST** | CodeQL | Semgrep + SonarQube |
| **SCA** | Dependabot | Trivy + OWASP Dependency-Check |
| **Secrets** | Secret Scanning | Gitleaks + TruffleHog |
| **IaC** | CodeQL (limitado) | Trivy + Checkov + KICS |
| **Container** | Container Scanning | Trivy + Grype |
| **Code Quality** | - | Lizard |

### Vulnerabilidades Detectadas

✅ **Injection Attacks** (SQL, Command, LDAP, etc.)  
✅ **Cross-Site Scripting (XSS)**  
✅ **Insecure Deserialization**  
✅ **Authentication & Authorization Issues**  
✅ **Cryptographic Failures**  
✅ **Security Misconfigurations**  
✅ **Vulnerable Dependencies** (CVEs conhecidos)  
✅ **Hardcoded Secrets & Credentials**  
✅ **IaC Misconfigurations**  
✅ **Container Vulnerabilities**  
✅ **License Compliance Issues**  
✅ **OWASP Top 10**  
✅ **CWE Top 25**  

---

## 🚀 Instalação e Configuração

### Passo 1: Adicionar o Workflow

1. Crie o diretório `.github/workflows/` no seu repositório (se não existir)
2. Copie o arquivo `security.yml` para este diretório
3. Commit e push para o repositório

```bash
mkdir -p .github/workflows
cp security.yml .github/workflows/
git add .github/workflows/security.yml
git commit -m "Add comprehensive security workflow"
git push
```

### Passo 2: Configurar Permissões

O workflow já está configurado com as permissões necessárias:

```yaml
permissions:
  contents: read           # Ler código do repositório
  actions: read           # Ler workflows
  security-events: write  # Escrever no Security tab
  pull-requests: write    # Comentar em PRs
```

### Passo 3: Verificar Execução

1. Acesse a aba **Actions** do seu repositório
2. Localize o workflow "Security Scans (GHAS Alternative)"
3. Verifique se a execução foi bem-sucedida
4. Acesse a aba **Security** → **Code scanning** para ver os alertas

---

## ⚙️ Configurações Opcionais

### 1. Secrets Recomendados

Configure os seguintes secrets no repositório para funcionalidades avançadas:

#### **SONAR_TOKEN** (Opcional - Análise SonarQube)

1. Acesse [SonarCloud](https://sonarcloud.io)
2. Crie uma conta e organização
3. Gere um token em: Account → Security → Generate Token
4. Adicione no GitHub: Settings → Secrets → Actions → New repository secret
   - Name: `SONAR_TOKEN`
   - Value: `seu_token_aqui`

#### **NVD_API_KEY** (Opcional - OWASP Dependency-Check)

1. Acesse [NVD API Key Request](https://nvd.nist.gov/developers/request-an-api-key)
2. Solicite uma API key gratuita
3. Adicione no GitHub: Settings → Secrets → Actions → New repository secret
   - Name: `NVD_API_KEY`
   - Value: `sua_api_key_aqui`

**Benefício:** Acelera significativamente os scans do Dependency-Check (de ~30min para ~5min)

### 2. Arquivo de Configuração do Gitleaks

Crie um arquivo `.gitleaks.toml` na raiz do repositório para customizar regras:

```toml
title = "Gitleaks Configuration"

[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''(?i)(api[_-]?key|apikey)['":\s]*[=:]\s*['"]?([a-zA-Z0-9]{32,})['"]?'''
tags = ["key", "API"]

[allowlist]
description = "Allowlist"
paths = [
    '''\.md$''',
    '''\.example$''',
    '''test/.*'''
]
```

### 3. Arquivo de Supressão do Dependency-Check

Crie um arquivo `.dependency-check-suppression.xml` para suprimir falsos positivos:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
    <suppress>
        <notes>Falso positivo - não afeta nosso uso</notes>
        <cve>CVE-2023-12345</cve>
    </suppress>
</suppressions>
```

### 4. Ajustar Severidades

Por padrão, o workflow reporta: **CRITICAL**, **HIGH** e **MEDIUM**

Para reportar apenas críticas e altas, edite as linhas:

```yaml
--severity CRITICAL,HIGH,MEDIUM
```

Para:

```yaml
--severity CRITICAL,HIGH
```

### 5. Desabilitar Ferramentas Específicas

Para desabilitar uma ferramenta, comente ou remova o step correspondente:

```yaml
# - name: Checkov IaC Scan
#   run: |
#     pip install checkov
#     ...
```

---

## 📊 Interpretação dos Resultados

### Onde Ver os Resultados?

#### 1. **Security Tab** (Principal)

- Acesse: Repositório → **Security** → **Code scanning alerts**
- Visualização: Todos os alertas categorizados por ferramenta
- Filtros disponíveis: Severidade, ferramenta, estado, branch

#### 2. **Pull Request Comments**

- Comentário automático com resumo dos scans executados
- Lista de ferramentas e status
- Link para visualização detalhada

#### 3. **Artifacts**

- Acesse: Actions → Workflow run → **Artifacts**
- Download: `security-reports-{sha}.zip`
- Contém: Todos os relatórios em SARIF e JSON

### Entendendo as Severidades

| Severidade | Descrição | Ação Recomendada |
|------------|-----------|------------------|
| **CRITICAL** | Vulnerabilidade crítica, exploração fácil | Corrigir imediatamente |
| **HIGH** | Vulnerabilidade séria, potencial de exploração | Corrigir em até 7 dias |
| **MEDIUM** | Vulnerabilidade moderada | Corrigir em até 30 dias |
| **LOW** | Problema menor ou best practice | Avaliar necessidade |
| **INFO** | Informativo, não é vulnerabilidade | Opcional |

### Categorias de Alertas

#### **semgrep-sast**
Vulnerabilidades no código-fonte (lógica, padrões inseguros)

#### **trivy-sca / owasp-dependency-check**
Vulnerabilidades em dependências de terceiros (bibliotecas, frameworks)

#### **gitleaks-secrets / trufflehog**
Credenciais, tokens, senhas expostas no código ou histórico

#### **trivy-iac / checkov-iac / kics-iac**
Configurações inseguras em arquivos de infraestrutura (Terraform, Kubernetes, Docker)

#### **trivy-container / grype-container**
Vulnerabilidades em imagens Docker (OS packages, dependências)

### Falsos Positivos

É normal ter alguns falsos positivos. Para gerenciá-los:

1. **Avaliar o Alerta:** Verificar se é realmente um falso positivo
2. **Marcar como Resolvido:** No Security tab, marcar como "Won't fix" ou "False positive"
3. **Adicionar Supressão:** Usar arquivos de configuração das ferramentas
4. **Documentar:** Sempre adicionar um comentário explicando o motivo

---

## 🔧 Troubleshooting

### Problema: Workflow falha completamente

**Possíveis causas:**
- Permissões insuficientes
- Quota de GitHub Actions excedida
- Dependências não disponíveis

**Solução:**
```bash
# Verificar permissões do repositório
Settings → Actions → General → Workflow permissions
# Selecionar "Read and write permissions"

# Verificar quota
Settings → Billing → Actions
```

### Problema: Nenhum alerta aparece no Security tab

**Possíveis causas:**
- Upload de SARIF falhou
- Arquivo SARIF vazio ou inválido
- Permissão `security-events: write` não configurada

**Solução:**
```bash
# Baixar artifacts e verificar conteúdo dos arquivos SARIF
# Verificar logs do workflow na etapa de upload
# Confirmar permissões no arquivo YAML
```

### Problema: Dependency-Check muito lento

**Causa:** Sem NVD_API_KEY configurada

**Solução:**
```bash
# Configurar NVD_API_KEY como secret
# Ou desabilitar Dependency-Check e usar apenas Trivy
```

### Problema: Muitos falsos positivos do Semgrep

**Solução:**
Crie um arquivo `.semgrepignore` na raiz:

```
# Ignorar arquivos de teste
test/
tests/
**/*_test.go
**/*.test.js

# Ignorar dependências
node_modules/
vendor/
.venv/

# Ignorar arquivos gerados
dist/
build/
*.min.js
```

### Problema: KICS falha com erro de Docker

**Causa:** Docker não disponível ou sem permissões

**Solução:**
```yaml
# Comentar o step do KICS ou usar instalação nativa:
- name: Install KICS
  run: |
    curl -sfL https://raw.githubusercontent.com/Checkmarx/kics/master/install.sh | bash
    kics scan -p . --report-formats sarif -o security-reports
```

### Problema: Timeout do workflow (>30min)

**Solução:**
```yaml
# Aumentar timeout
timeout-minutes: 60

# Ou otimizar removendo ferramentas redundantes
# Exemplo: remover Checkov e manter apenas Trivy + KICS
```

---

## 📈 Comparação com GHAS

### Vantagens desta Solução

✅ **Custo:** 100% gratuito vs $49/usuário/mês do GHAS  
✅ **Cobertura IaC:** 3 ferramentas especializadas vs limitações do CodeQL  
✅ **Container Security:** 2 ferramentas vs 1 no GHAS  
✅ **Secrets Detection:** 2 ferramentas com diferentes abordagens  
✅ **Flexibilidade:** Total controle sobre ferramentas e configurações  
✅ **Transparência:** Open-source, auditável, sem vendor lock-in  
✅ **Complementariedade:** Múltiplas ferramentas reduzem falsos negativos  

### Desvantagens

❌ **Manutenção:** Requer atualização manual das versões das ferramentas  
❌ **Performance:** Múltiplas ferramentas = tempo de execução maior  
❌ **UI:** Interface menos integrada que GHAS (mas ainda usa Security tab)  
❌ **Suporte:** Sem suporte oficial, dependência da comunidade  
❌ **Auto-fix:** Sem correção automática de PRs (presente no Dependabot)  

### Quando Usar Cada Opção

**Use GHAS se:**
- Orçamento permite
- Precisa de suporte enterprise
- Quer interface totalmente integrada
- Valoriza auto-fix do Dependabot

**Use esta solução se:**
- Quer economia significativa
- Precisa de mais controle e customização
- Busca cobertura mais abrangente (especialmente IaC)
- Já tem expertise em DevSecOps

---

## 🔄 Manutenção e Atualizações

### Atualizações Recomendadas

#### Mensal

```bash
# Verificar novas versões das ferramentas
# Trivy: https://github.com/aquasecurity/trivy/releases
# Semgrep: https://github.com/semgrep/semgrep/releases
# Gitleaks: https://github.com/gitleaks/gitleaks/releases
```

#### Trimestral

```bash
# Atualizar rulesets do Semgrep
semgrep --config p/security-audit --config p/owasp-top-ten

# Revisar falsos positivos acumulados
# Ajustar arquivos de supressão
```

#### Anual

```bash
# Avaliar novas ferramentas do mercado
# Revisar cobertura e eficácia
# Ajustar estratégia de segurança
```

### Exemplo de Atualização

```yaml
# Versão antiga
- name: Setup Trivy
  uses: aquasecurity/setup-trivy@v0.2.4
  with:
    version: v0.58.1

# Versão nova (verificar breaking changes antes)
- name: Setup Trivy
  uses: aquasecurity/setup-trivy@v0.3.0
  with:
    version: v0.60.0
```

### Monitoramento de Eficácia

Métricas a acompanhar:

- **Taxa de falsos positivos** (objetivo: <15%)
- **Tempo médio de correção** (MTTR)
- **Número de vulnerabilidades por severidade**
- **Cobertura de código** (linhas escaneadas)
- **Tempo de execução do workflow** (objetivo: <30min)

---

## 📚 Recursos Adicionais

### Documentação das Ferramentas

- [Semgrep](https://semgrep.dev/docs/)
- [Trivy](https://aquasecurity.github.io/trivy/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- [Checkov](https://www.checkov.io/documentation.html)
- [KICS](https://docs.kics.io/)
- [OWASP Dependency-Check](https://jeremylong.github.io/DependencyCheck/)
- [Grype](https://github.com/anchore/grype)

### Benchmarks de Segurança

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Comunidades

- [r/netsec](https://reddit.com/r/netsec)
- [OWASP Slack](https://owasp.org/slack/invite)
- [DevSecOps Community](https://www.devsecops.org/)

---

## 🤝 Contribuindo

Este workflow é uma base sólida, mas pode ser melhorado! Sugestões de melhorias:

1. **Adicionar suporte a mais linguagens**
2. **Integrar com ferramentas de ticketing** (Jira, Linear)
3. **Adicionar métricas customizadas**
4. **Criar dashboards de visualização**
5. **Automatizar correções com PRs**

---

## 📄 Licença

Este workflow é fornecido "como está", sem garantias. Use por sua conta e risco.

As ferramentas incluídas possuem suas próprias licenças (geralmente Apache 2.0 ou MIT).

---

## ✅ Checklist de Implementação

- [ ] Workflow adicionado ao repositório
- [ ] Permissões configuradas corretamente
- [ ] Primeira execução bem-sucedida
- [ ] Alertas visíveis no Security tab
- [ ] Secrets opcionais configurados (SONAR_TOKEN, NVD_API_KEY)
- [ ] Arquivos de configuração customizados (.gitleaks.toml, suppressions)
- [ ] Equipe treinada na interpretação dos resultados
- [ ] Processo de triagem de alertas definido
- [ ] SLA de correção estabelecido
- [ ] Monitoramento de métricas implementado

---

## 🆘 Suporte

Para questões ou problemas:

1. Revisar este README
2. Verificar logs do workflow no Actions
3. Consultar documentação das ferramentas
4. Abrir issue no repositório

**Lembre-se:** Segurança é um processo contínuo, não um evento único! 🔒

## Como rodar localmente

### Instalar dependências principais
```bash
pip install -r requirements.txt

Rodar aplicação vulnerável

cd vulnerable-app
python3 app.py

Aplicação será exposta em http://localhost:3001.

Rodar scanners manualmente

Trivy (filesystem e IaC)

trivy fs vulnerable-app/
trivy config iac-terraform/

Gitleaks

gitleaks detect --source . --report-format json --report-path gitleaks-report.json

Bandit

bandit -r vulnerable-app -f json -o bandit-report.json

Semgrep

semgrep --config p/ci --json --output semgrep-report.json


⸻

Objetivo do Projeto

Este projeto foi criado para:
	•	Testar ferramentas de segurança em CI/CD.
	•	Demonstrar como falhas comuns em aplicações, IaC e cloud são detectadas.
	•	Servir como laboratório educacional para times de DevSecOps, Cloud e Segurança.

⸻

Aviso Importante

Este repositório contém código e configurações intencionalmente vulneráveis.
Não utilize este código em produção. O propósito é exclusivamente educacional e de testes.
