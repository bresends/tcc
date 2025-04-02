# Plano de Trabalho de Conclusão de Curso - CBMGO

## Título Preliminar
**Inteligência Artificial para Consulta a Normas Técnicas do CBMGO: Impacto de Estratégias de Fragmentação, Modelos de Incorporação e Desempenho dos LLMs para um Sistema RAG**

## Objetivo Geral
Desenvolver e avaliar um sistema de Recuperação Aumentada por Geração (RAG) para consulta às normas técnicas do CBMGO, analisando o impacto de diferentes estratégias de fragmentação de documentos, modelos de incorporação e tipos de LLMs no desempenho, acurácia e usabilidade do sistema.

## Objetivos Específicos
1. Comparar diferentes estratégias de fragmentação de documentos (por parágrafo, por seção, por página, por chunks de tamanho fixo) para identificar o método mais eficaz para as normas técnicas do CBMGO.
2. Avaliar diversos modelos de incorporação (embedding models) em termos de precisão na recuperação de informações relevantes das normas técnicas.
3. Testar diferentes Modelos de Linguagem de Grande Porte (LLMs) para determinar qual oferece melhor desempenho em acurácia, tempo de resposta e rastreabilidade.
4. Quantificar o potencial impacto na celeridade das consultas às normas técnicas com a implementação de um sistema RAG otimizado no CBMGO.
5. Desenvolver um protótipo funcional de sistema RAG para consulta às normas técnicas do CBMGO que possa ser posteriormente implementado pela instituição.

## Justificativa
A consulta às normas técnicas do CBMGO é uma atividade frequente e essencial para o trabalho dos bombeiros militares, especialmente nas áreas de vistorias e atividades técnicas. O processo tradicional de busca em documentos extensos é demorado e suscetível a erros humanos. Um sistema RAG otimizado pode revolucionar esse processo, proporcionando respostas rápidas, precisas e com referências diretas às fontes normativas, resultando em maior eficiência operacional e melhor serviço à população.

## Metodologia

### 1. Preparação do Corpus
- Digitalização e/ou coleta das normas técnicas do CBMGO em formato processável.
- Pré-processamento dos documentos (limpeza, formatação, indexação).

### 2. Implementação de Estratégias de Fragmentação
- Implementação de diferentes métodos de fragmentação (chunking):
  - Por parágrafos
  - Por seções/subseções
  - Por número fixo de tokens
  - Por contexto semântico
  - Híbridos

### 3. Avaliação de Modelos de Incorporação (Embedding)
- Teste de diferentes modelos de incorporação:
  - OpenAI Embeddings (text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large)
  - Modelos open-source (BERT, Sentence-BERT, MPNet)
  - Embeddings específicos para domínio jurídico/normativo

### 4. Implementação e Teste de LLMs
- Implementação de diferentes LLMs como geradores de respostas:
  - GPT-4
  - Claude (Anthropic)
  - Llama 3
  - Outros modelos open-source relevantes

### 5. Construção do Sistema RAG
- Desenvolvimento da arquitetura RAG:
  - Sistema de armazenamento vetorial (vector database)
  - Pipeline de recuperação
  - Componente de geração de respostas
  - Interface de usuário para consultas

### 6. Avaliação de Desempenho
- Definição de métricas:
  - Precisão e recall das respostas
  - Tempo médio de resposta
  - Relevância das citações recuperadas
  - Rastreabilidade das fontes
- Condução de testes comparativos entre diferentes configurações

### 7. Análise de Impacto
- Mensuração do ganho de tempo em comparação com métodos tradicionais
- Avaliação da satisfação do usuário
- Análise custo-benefício da implementação

## Resultados Esperados
1. Identificação da combinação ótima de estratégias de fragmentação, modelos de incorporação e LLMs para consulta às normas técnicas do CBMGO.
2. Quantificação do ganho de eficiência proporcionado pelo sistema RAG em comparação com métodos tradicionais.
3. Desenvolvimento de um protótipo funcional que possa ser implementado no CBMGO.
4. Estabelecimento de diretrizes para futura expansão do sistema para outras áreas normativas da corporação.

## Limitações e Desafios
- Necessidade de recursos computacionais para processamento e armazenamento
- Potenciais restrições orçamentárias para uso de API de LLMs proprietários
- Desafios na adaptação de modelos gerais para o domínio específico das normas do CBMGO
- Potencial resistência à adoção de novas tecnologias

## Considerações Éticas e Institucionais
- Garantia de conformidade com políticas de segurança da informação do CBMGO
- Transparência sobre as limitações do sistema para evitar uso inadequado

## Recursos Necessários
- Acesso às normas técnicas do CBMGO em formato digital
- Infraestrutura computacional para processamento e armazenamento
- Acesso às APIs de LLMs ou recursos para fine-tuning de modelos open-source
- Participação de bombeiros militares para testes e validação do sistema