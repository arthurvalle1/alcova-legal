# Crescimento dentro do produto (custo zero, precisa de desenvolvimento)

> O Character.AI não cresceu por anúncio: cresceu porque o produto gera divulgação sozinho.
> Estas são as mudanças no app que fazem o mesmo no modelo de catálogo. Ordem = impacto ÷ esforço.

## 0. Personalização: fechar a única fraqueza do ALCOVA (prioridade máxima)

Quem vem do Character.AI espera personalizar. Roadmap em camadas (detalhes em
`ESTUDO-CHARACTER-AI.md` §4):

1. **Persona do usuário** (curto prazo): nome/apelido, pronomes, aparência e 2–3 traços do protagonista,
   usados pela personagem na saga. Entra no prompt; não quebra o roteiro.
2. **Ajuste da personagem antes da saga:** tom (doce / provocadora / misteriosa), ritmo (lento /
   intenso), 1 entre 3 cenários de abertura.
3. **Votação de novas personagens:** a comunidade escolhe arquétipos; os vencedores viram drops.
4. **Estúdio ALCOVA (UGC moderado):** usuário cria a personagem → revisão (IA + humano, regras +18 e
   tolerância zero com aparência infantil) → entra no catálogo com crédito ao criador → criador ganha
   saga grátis a cada X matches. Cada personagem criada vira página pública e link compartilhável: é
   o motor nº 1 do Character.AI, com moderação.

Cada etapa lançada vira campanha de marketing ("agora você cria o seu protagonista").

## 1. Botão "Compartilhar esta fala"

- Em qualquer mensagem da personagem: toque longo → **Compartilhar**.
- Gera uma imagem 1080×1920 (formato story): fundo escuro da marca, a fala em serifa, nome da
  personagem, selo +18 e "ALCOVA — escolha a sua" + link curto com UTM `utm_source=share`.
- Usa o *share sheet* nativo do Android (WhatsApp, Instagram Stories, TikTok).
- **Filtro de segurança:** só permite compartilhar falas que passaram pela moderação e bloqueia
  mensagens do usuário (privacidade). Isso também protege contra prints explícitos atribuídos à marca.
- Meta: 0,2 compartilhamentos por usuário ativo.

## 2. Página pública de cada personagem

- URL `/personagens/<nome>/` no site (pode ser gerada pelo mesmo esquema do blog).
- Conteúdo: imagem, idade (sempre adulta), 3 tags de temperamento, frase de abertura, sinopse da
  saga sem spoiler, botão "Dar match no app" (deep link / loja com UTM `utm_campaign=<nome>`).
- Cada personagem lançada = 1 página indexável + 1 link para os vídeos. É o substituto direto das
  páginas de personagens criadas por usuários do Character.AI.

## 3. Pedido de avaliação no momento certo

- Usar a **Google Play In-App Review API** logo **após o clímax** ou o final de uma saga (pico emocional),
  nunca no primeiro uso e nunca depois de um erro.
- Mais avaliações 5★ → melhor posição na busca da loja → mais instalações grátis.

## 4. Indicação ("Convide alguém para a Alcova")

- Cada usuário tem um código. Quem indica ganha **desconto ou 1 saga grátis** quando o indicado
  compra a primeira saga paga (evita abuso com contas falsas).
- Custo real: só o custo de API da saga dada (o preço "cheio" não sai do caixa).
- Usar o *Install Referrer* do Google Play para atribuir automaticamente.

## 5. Preço e empacotamento (testar, não adivinhar)

R$ 24,90 é alto comparado a concorrentes gratuitos. Testes sugeridos (um por vez):
1. **Pacote de 3 sagas** por R$ 59,90 (âncora de economia).
2. **"Capítulo 1" grátis em todas as personagens** (os primeiros ~15 min), e paga para continuar — o
   catálogo inteiro vira vitrine em vez de uma única saga grátis. Isso combina muito com o modelo
   Tinder: o usuário "conversa um pouco" com várias antes de escolher com quem ficar.
3. **Saga curta** (~1 h) por R$ 9,90 como degrau de entrada.

Métrica de decisão: receita por instalação (não só taxa de conversão).

## 6. Mecânicas de catálogo (o "Tinder" a favor da retenção)

- **Drops com data marcada** (ex.: toda quarta, 20h) + notificação local: cria hábito, igual a
  lançamento de episódio.
- **"Ela te mandou uma mensagem"**: notificação local depois de 24–48 h sem abrir, escrita na voz da
  personagem da saga em andamento (sem conteúdo sensível na prévia da notificação — discrição).
- **Fila de "curtidas"**: personagens que o usuário curtiu mas não começou ficam numa lista de desejos
  → lembrete quando houver promoção.
- **Personagem "em destaque" do dia** no topo do catálogo — dá motivo para abrir o app diariamente.
- **Contador social leve:** "1,2 mil pessoas confessaram com ela esta semana" (só com números reais).

## 7. Lista de espera para iPhone

- Formulário gratuito (Google Forms) linkado na landing: "Avise-me quando chegar no iPhone".
- Mede a demanda e já dá uma base de e-mails para o lançamento no iOS.

## 8. Instrumentação mínima (para saber o que funciona)

Eventos para registrar no backend (sem dados pessoais sensíveis, coerente com a política de privacidade):
`catalog_view` · `card_swipe_left/right` · `character_open` · `saga_start` · `saga_milestone_n` ·
`saga_finish` · `purchase` · `share_line` · `review_prompt_shown` · `referral_sent/converted`.

Com isso dá para responder: quais personagens geram mais match? Onde as pessoas abandonam a saga?
Qual personagem converte mais em compra? → isso decide quais drops fazer a seguir e quais personagens
viram estrelas dos vídeos.

> ⚠️ Se novos dados forem coletados (ex.: código de indicação), atualize a Política de Privacidade.
