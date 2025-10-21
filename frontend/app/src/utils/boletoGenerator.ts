// Gerador de boleto bancário em HTML/PDF

export interface BoletoData {
  linha_digitavel: string;
  codigo_barras: string;
  valor: number;
  vencimento: string;
  beneficiario: {
    nome: string;
    cnpj: string;
    agencia: string;
    conta: string;
  };
  pagador: {
    nome: string;
    cpf_cnpj: string;
    endereco?: string;
  };
  numero_documento: string;
  data_documento: string;
  data_processamento: string;
}

export function gerarBoletoPDF(data: BoletoData): void {
  const boletoHTML = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boleto Bancário</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f5f5f5;
        }
        
        .boleto-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border: 1px solid #000;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border: 1px solid #000;
            margin-bottom: 2px;
        }
        
        .banco-logo {
            font-size: 24px;
            font-weight: bold;
        }
        
        .banco-codigo {
            font-size: 20px;
            font-weight: bold;
            padding: 0 10px;
            border-left: 2px solid #000;
            border-right: 2px solid #000;
        }
        
        .linha-digitavel-header {
            font-size: 14px;
            font-weight: bold;
            flex: 1;
            text-align: right;
        }
        
        .campo {
            border: 1px solid #000;
            border-top: none;
            padding: 5px;
            display: flex;
        }
        
        .campo-linha {
            display: flex;
            border: 1px solid #000;
            border-top: none;
        }
        
        .campo-item {
            padding: 5px;
            flex: 1;
            border-right: 1px solid #000;
        }
        
        .campo-item:last-child {
            border-right: none;
        }
        
        .campo-label {
            font-size: 9px;
            display: block;
            margin-bottom: 2px;
        }
        
        .campo-valor {
            font-size: 12px;
            font-weight: bold;
        }
        
        .instrucoes {
            border: 1px solid #000;
            border-top: none;
            padding: 10px;
            min-height: 80px;
        }
        
        .instrucoes-label {
            font-size: 9px;
            display: block;
            margin-bottom: 5px;
        }
        
        .codigo-barras {
            text-align: center;
            padding: 10px 0;
            margin: 10px 0;
        }
        
        .barcode {
            font-family: monospace;
            font-size: 18px;
            letter-spacing: 0;
            line-height: 1;
            word-break: break-all;
        }
        
        .linha-digitavel {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 2px;
            padding: 10px;
            border: 1px dashed #666;
            margin: 20px 0;
        }
        
        .ficha-compensacao {
            margin-top: 30px;
            border-top: 1px dashed #000;
            padding-top: 20px;
        }
        
        .titulo-secao {
            font-size: 10px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .no-print {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="boleto-container">
        <div class="header">
            <div class="banco-logo">Seu banco</div>
            <div class="banco-codigo">000-0</div>
            <div class="linha-digitavel-header">${formatarLinhaDigitavel(data.linha_digitavel)}</div>
        </div>
        
        <div class="campo-linha">
            <div class="campo-item" style="flex: 3;">
                <span class="campo-label">Local do pagamento</span>
                <span class="campo-valor">PAGÁVEL EM QUALQUER BANCO ATÉ O VENCIMENTO</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Vencimento</span>
                <span class="campo-valor">${data.vencimento}</span>
            </div>
        </div>
        
        <div class="campo-linha">
            <div class="campo-item" style="flex: 3;">
                <span class="campo-label">Cedente</span>
                <span class="campo-valor">${data.beneficiario.nome}</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Agência/Código Cedente</span>
                <span class="campo-valor">${data.beneficiario.agencia} / ${data.beneficiario.conta}</span>
            </div>
        </div>
        
        <div class="campo-linha">
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Data do documento</span>
                <span class="campo-valor">${data.data_documento}</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Nº do documento</span>
                <span class="campo-valor">${data.numero_documento}</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Espécie doc.</span>
                <span class="campo-valor">DM</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Aceite</span>
                <span class="campo-valor">N</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Data processamento</span>
                <span class="campo-valor">${data.data_processamento}</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Nosso número</span>
                <span class="campo-valor">${data.numero_documento}</span>
            </div>
        </div>
        
        <div class="campo-linha">
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Uso do banco</span>
                <span class="campo-valor"></span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Carteira</span>
                <span class="campo-valor">RG</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Espécie</span>
                <span class="campo-valor">R$</span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Quantidade</span>
                <span class="campo-valor"></span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Valor</span>
                <span class="campo-valor"></span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">(=) Valor do documento</span>
                <span class="campo-valor">${formatarValor(data.valor)}</span>
            </div>
        </div>
        
        <div class="instrucoes">
            <span class="instrucoes-label">Instruções</span>
            <p style="font-size: 11px; margin-top: 10px;">
                - Não receber após o vencimento<br>
                - Após o vencimento cobrar multa de 2%<br>
                - Após o vencimento cobrar juros de mora de 1% ao mês
            </p>
        </div>
        
        <div class="campo-linha">
            <div class="campo-item" style="flex: 3;">
                <span class="campo-label">Sacado</span>
                <span class="campo-valor">${data.pagador.nome}</span><br>
                <span class="campo-valor" style="font-size: 10px; font-weight: normal;">
                    CPF/CNPJ: ${formatarCPFCNPJ(data.pagador.cpf_cnpj)}
                </span>
            </div>
            <div class="campo-item" style="flex: 1;">
                <span class="campo-label">Valor cobrado</span>
                <span class="campo-valor">${formatarValor(data.valor)}</span>
            </div>
        </div>
        
        <div class="codigo-barras">
            <div class="barcode">${gerarCodigoBarrasVisual(data.codigo_barras)}</div>
        </div>
        
        <div class="linha-digitavel">
            ${formatarLinhaDigitavel(data.linha_digitavel)}
        </div>
        
        <div style="text-align: center; margin-top: 20px; padding: 10px;">
            <button onclick="window.print()" class="no-print" 
                style="padding: 10px 30px; font-size: 14px; background: #4F46E5; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Imprimir Boleto
            </button>
            <button onclick="window.close()" class="no-print"
                style="padding: 10px 30px; font-size: 14px; background: #6B7280; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px;">
                Fechar
            </button>
        </div>
    </div>
    
    <script>
        // Auto-print quando abrir
        // window.onload = function() {
        //     window.print();
        // }
    </script>
</body>
</html>
  `;

  // Abre o boleto em uma nova aba
  const novaJanela = window.open('', '_blank');
  if (novaJanela) {
    novaJanela.document.write(boletoHTML);
    novaJanela.document.close();
  } else {
    alert('Por favor, permita pop-ups para visualizar o boleto.');
  }
}

function formatarLinhaDigitavel(linha: string): string {
  // Formata linha digitável com espaços
  // Formato: XXXXX.XXXXX XXXXX.XXXXXX XXXXX.XXXXXX X XXXXXXXXXXXXXXXX
  if (!linha || linha.length < 47) return linha;
  
  return `${linha.substr(0, 5)}.${linha.substr(5, 5)} ${linha.substr(10, 5)}.${linha.substr(15, 6)} ${linha.substr(21, 5)}.${linha.substr(26, 6)} ${linha.substr(32, 1)} ${linha.substr(33)}`;
}

function formatarValor(valor: number): string {
  return valor.toLocaleString('pt-BR', { 
    style: 'currency', 
    currency: 'BRL' 
  });
}

function formatarCPFCNPJ(doc: string): string {
  const numeros = doc.replace(/\D/g, '');
  
  if (numeros.length === 11) {
    // CPF: 000.000.000-00
    return numeros.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  } else if (numeros.length === 14) {
    // CNPJ: 00.000.000/0000-00
    return numeros.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
  }
  
  return doc;
}

function gerarCodigoBarrasVisual(codigo: string): string {
  // Gera representação visual do código de barras
  // Usa blocos Unicode para simular barras
  let barras = '';
  
  for (let i = 0; i < codigo.length; i++) {
    const digito = parseInt(codigo[i]);
    // Alterna entre barras grossas e finas usando diferentes caracteres
    if (digito % 3 === 0) {
      barras += '█';
    } else if (digito % 3 === 1) {
      barras += '▌';
    } else {
      barras += '▐';
    }
  }
  
  return barras;
}

export function formatarDataBrasileira(data?: string): string {
  if (!data) {
    const hoje = new Date();
    return hoje.toLocaleDateString('pt-BR');
  }
  
  const date = new Date(data);
  return date.toLocaleDateString('pt-BR');
}

export function calcularVencimento(dias: number = 3): string {
  const data = new Date();
  data.setDate(data.getDate() + dias);
  return data.toLocaleDateString('pt-BR');
}

