const input = document.getElementById("file-upload");
const output = document.getElementById("api-output");

input.addEventListener("change", enviarArquivo);

async function enviarArquivo() {
  const arquivo = input.files[0];

  if (!arquivo) return;

  const formData = new FormData();
  formData.append("file", arquivo);

  output.textContent = "Enviando...";

  try {
    const response = await fetch("http://localhost:8000/document/extract", {
      method: "POST",
      body: formData,
    });

    const resultado = await response.json();
    output.innerHTML = montarResposta(resultado);
  } catch (erro) {
    output.textContent = `Erro: ${erro.message}`;
  }
}

function montarResposta(dados) {
  if (!dados || typeof dados !== "object") {
    return `
      <div class="info-grid">
        <article class="info-item">
          <span>Resposta</span>
          <strong>${escaparHtml(formatarValor(dados))}</strong>
        </article>
      </div>
    `;
  }

  const ordemCampos = [
    "data_criacao",
    "nome_fantasia",
    "razao_social",
    "cnpj",
    "situacao",
    "nome_socio",
  ];

  const campos = Array.isArray(dados)
    ? dados.flatMap((item, index) =>
        Object.entries(item).map(([campo, valor]) => [
          `Item ${index + 1} - ${campo}`,
          valor,
        ])
      )
    : Object.entries(dados).sort(
        ([a], [b]) => ordemCampos.indexOf(a) - ordemCampos.indexOf(b)
      );

  return `
    <div class="info-grid">
      ${campos
        .map(
          ([campo, valor]) => `
        <article class="info-item">
          <span>${escaparHtml(formatarCampo(campo))}</span>
          <strong>${escaparHtml(formatarValor(valor))}</strong>
        </article>
      `
        )
        .join("")}
    </div>
  `;
}

function formatarCampo(campo) {
  const nomes = {
    cnpj: "CNPJ",
    razao_social: "Nome Social",
    nome_fantasia: "Nome",
    data_criacao: "Data de Criação",
    situacao: "Situação",
    nome_socio: "Nome do Sócio",
  };

  return (
    nomes[campo] ||
    campo
      .replaceAll("_", " ")
      .replace(/\b\w/g, (letra) => letra.toUpperCase())
  );
}

function formatarValor(valor) {
  if (valor == null || valor === "") return "Não informado";

  if (typeof valor === "boolean") return valor ? "Sim" : "Não";

  if (Array.isArray(valor)) {
    return valor.map(formatarValor).join(", ");
  }

  if (typeof valor === "object") {
    return Object.entries(valor)
      .map(([campo, item]) => `${formatarCampo(campo)}: ${formatarValor(item)}`)
      .join(" | ");
  }

  return String(valor);
}

function escaparHtml(texto) {
  return String(texto)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}