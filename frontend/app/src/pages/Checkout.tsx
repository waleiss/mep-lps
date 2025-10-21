import { useState, useMemo, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";
import { consultarCEP, criarEndereco } from "../services/addressApi";
import { 
  processarPagamentoCartao, 
  processarPagamentoPix, 
  processarPagamentoBoleto 
} from "../services/paymentApi";
import { createOrder } from "../services/ordersApi";
import type { PaymentMethod } from "../types/payment";
import { 
  gerarBoletoPDF, 
  formatarDataBrasileira, 
  calcularVencimento 
} from "../utils/boletoGenerator";

type FormAddress = {
  name: string;
  zip: string;
  street: string;
  number: string;
  complement?: string;
  city: string;
  state: string;
  neighborhood: string;
};

type CardData = {
  holder: string;
  number: string;
  exp: string; // MM/AA
  cvv: string;
};

const money = (v: number) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export default function Checkout() {
  const nav = useNavigate();
  const { user } = useAuth();
  const { items, subtotal, shipping, total, clear } = useCart();

  // ------------------ estado do formulário ------------------
  const [address, setAddress] = useState<FormAddress>({
    name: user?.name ?? "",
    zip: "",
    street: "",
    number: "",
    complement: "",
    city: "",
    state: "",
    neighborhood: "",
  });

  const [loadingCep, setLoadingCep] = useState(false);
  const [cepError, setCepError] = useState("");
  const [processing, setProcessing] = useState(false);
  const [paymentError, setPaymentError] = useState("");

  const [payMethod, setPayMethod] = useState<PaymentMethod>("card");
  const [card, setCard] = useState<CardData>({
    holder: "",
    number: "",
    exp: "",
    cvv: "",
  });
  const [cpfCnpj, setCpfCnpj] = useState("");

  // ------------------ buscar CEP ------------------
  useEffect(() => {
    const cepLimpo = address.zip.replace(/\D/g, "");
    
    if (cepLimpo.length === 8) {
      setLoadingCep(true);
      setCepError("");
      
      consultarCEP(cepLimpo)
        .then((data) => {
          if (data.erro) {
            setCepError("CEP não encontrado");
            return;
          }
          
          setAddress((prev) => ({
            ...prev,
            street: data.logradouro || prev.street,
            neighborhood: data.bairro || prev.neighborhood,
            city: data.localidade || prev.city,
            state: data.uf || prev.state,
            complement: data.complemento || prev.complement,
          }));
        })
        .catch((err) => {
          console.error("Erro ao consultar CEP:", err);
          setCepError("Erro ao buscar CEP. Digite manualmente.");
        })
        .finally(() => {
          setLoadingCep(false);
        });
    }
  }, [address.zip]);

  // ------------------ validações simples ------------------
  const perfilIncompleto = !user || !user.email || !user.name;

  const addressValid = useMemo(() => {
    const { name, zip, street, number, city, state, neighborhood } = address;
    return [name, zip, street, number, city, state, neighborhood].every(
      (v) => v && v.trim().length > 0
    );
  }, [address]);

  const paymentValid = useMemo(() => {
    if (payMethod === "pix") return true;
    
    if (payMethod === "boleto") {
      // Valida CPF ou CNPJ (apenas formato simples)
      const doc = cpfCnpj.replace(/\D/g, "");
      return doc.length === 11 || doc.length === 14;
    }
    
    // cartão bem simples (não é validação de verdade)
    return (
      card.holder.trim().length > 4 &&
      /^\d{13,19}$/.test(card.number.replace(/\s/g, "")) &&
      /^\d{2}\/\d{2}$/.test(card.exp) &&
      /^\d{3,4}$/.test(card.cvv)
    );
  }, [payMethod, card, cpfCnpj]);

  const canFinish =
    !!user &&
    items.length > 0 &&
    !perfilIncompleto &&
    addressValid &&
    paymentValid;

  // ------------------ finalizar pedido ------------------
  const finishOrder = async () => {
    if (!canFinish || !user) return;

    setProcessing(true);
    setPaymentError("");

    try {
      // 1. Criar endereço
      const enderecoData = {
        usuario_id: parseInt(user.id),
        cep: address.zip.replace(/\D/g, ""),
        logradouro: address.street,
        numero: address.number,
        complemento: address.complement || "",
        bairro: address.neighborhood,
        cidade: address.city,
        estado: address.state,
        apelido: "Endereço de entrega",
        principal: false,
      };

      const enderecoResponse = await criarEndereco(enderecoData);
      console.log("Endereço criado:", enderecoResponse);

      if (!enderecoResponse || !enderecoResponse.id) {
        throw new Error("Erro ao criar endereço: ID não retornado");
      }

      // 2. Criar pedido no backend
      const orderData = {
        usuario_id: parseInt(user.id),
        endereco_entrega_id: enderecoResponse.id, // Usa o ID do endereço criado
        valor_frete: shipping,
        items: items.map(item => ({
          livro_id: parseInt(item.book.id),
          quantidade: item.qty,
          preco_unitario: item.book.price,
        })),
        observacoes: `Pagamento: ${payMethod === "card" ? "Cartão" : payMethod === "pix" ? "PIX" : "Boleto"}`,
      };

      const pedido = await createOrder(orderData);
      
      if (!pedido) {
        throw new Error("Erro ao criar pedido");
      }
      
      const pedidoId = pedido.id;
      console.log("Pedido criado:", pedido);

      // 3. Processar pagamento
      let paymentResponse;
      
      if (payMethod === "card") {
        paymentResponse = await processarPagamentoCartao({
          usuario_id: parseInt(user.id),
          pedido_id: pedidoId,
          valor: total,
          numero_cartao: card.number.replace(/\s/g, ""),
          nome_titular: card.holder,
          validade: card.exp,
          cvv: card.cvv,
          parcelas: 1,
        });
      } else if (payMethod === "pix") {
        paymentResponse = await processarPagamentoPix({
          usuario_id: parseInt(user.id),
          pedido_id: pedidoId,
          valor: total,
        });
        
        // Se for PIX, mostrar QR Code
        if (paymentResponse.qr_code) {
          alert(`Pagamento PIX gerado!\n\nQR Code: ${paymentResponse.qr_code.substring(0, 50)}...\n\nPague e aguarde confirmação.`);
        }
      } else if (payMethod === "boleto") {
        paymentResponse = await processarPagamentoBoleto({
          usuario_id: parseInt(user.id),
          pedido_id: pedidoId,
          valor: total,
          cpf_cnpj: cpfCnpj.replace(/\D/g, ""),
        });
        
        // Gera e abre o boleto em PDF em nova aba
        if (paymentResponse.linha_digitavel && paymentResponse.codigo_barras) {
          gerarBoletoPDF({
            linha_digitavel: paymentResponse.linha_digitavel,
            codigo_barras: paymentResponse.codigo_barras,
            valor: total,
            vencimento: calcularVencimento(3),
            beneficiario: {
              nome: "Mundo em Palavras LTDA",
              cnpj: "12.345.678/0001-90",
              agencia: "1234",
              conta: "56789-0",
            },
            pagador: {
              nome: address.name,
              cpf_cnpj: cpfCnpj,
              endereco: `${address.street}, ${address.number} - ${address.city}/${address.state}`,
            },
            numero_documento: paymentResponse.codigo_transacao,
            data_documento: formatarDataBrasileira(),
            data_processamento: formatarDataBrasileira(),
          });
        }
      }

      console.log("Pagamento processado:", paymentResponse);

      if (paymentResponse?.status === "recusado") {
        setPaymentError(paymentResponse.mensagem || "Pagamento recusado. Tente outro cartão.");
        return;
      }

      // 4. Limpar carrinho e redirecionar
      clear();
      alert("Pedido realizado com sucesso! 🎉");
      nav("/account");
    } catch (error: any) {
      console.error("Erro ao finalizar pedido:", error);
      
      // Trata diferentes formatos de erro da API
      let errorMessage = "Erro ao processar pedido. Tente novamente.";
      
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        
        // Se detail for um array de erros de validação
        if (Array.isArray(detail)) {
          errorMessage = detail
            .map((err: any) => {
              const field = err.loc ? err.loc.join(" -> ") : "campo";
              return `${field}: ${err.msg}`;
            })
            .join(", ");
        } 
        // Se detail for uma string
        else if (typeof detail === "string") {
          errorMessage = detail;
        }
        // Se detail for um objeto
        else if (typeof detail === "object") {
          errorMessage = JSON.stringify(detail);
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setPaymentError(errorMessage);
    } finally {
      setProcessing(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-2xl font-bold mb-2">Seu carrinho está vazio</h1>
        <Link to="/" className="text-indigo-700 underline">
          Voltar à loja
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-6 grid md:grid-cols-3 gap-8">
      {/* Coluna esquerda: Itens + Formulários */}
      <div className="md:col-span-2 space-y-8">
        <h1 className="text-2xl font-bold text-indigo-900">Finalizar compra</h1>

        {!user && (
          <div className="p-4 border rounded-lg bg-yellow-50 text-sm">
            Você precisa{" "}
            <Link to="/login" className="text-indigo-700 underline">
              entrar
            </Link>{" "}
            para finalizar.
          </div>
        )}

        {user && perfilIncompleto && (
          <div className="p-4 border rounded-lg bg-yellow-50 text-sm">
            Complete seus dados em{" "}
            <Link to="/account/profile" className="text-indigo-700 underline">
              Minha conta
            </Link>
            .
          </div>
        )}

        {/* Itens do carrinho */}
        <ul className="divide-y rounded-xl border bg-white">
          {items.map((it) => (
            <li key={it.book.id} className="p-4 flex gap-4">
              <img
                src={it.book.cover}
                className="w-16 h-16 rounded-lg object-cover"
              />
              <div className="flex-1">
                <div className="font-semibold">{it.book.title}</div>
                <div className="text-sm text-slate-600">{it.book.author}</div>
              </div>
              <div className="text-sm">x{it.qty}</div>
              <div className="font-semibold">
                {money(it.book.price * it.qty)}
              </div>
            </li>
          ))}
        </ul>

        {/* Endereço de entrega */}
        <section className="rounded-xl border p-4 bg-white">
          <h2 className="font-semibold mb-3">Endereço de entrega</h2>
          <div className="grid sm:grid-cols-2 gap-3">
            <Input
              label="Nome completo"
              value={address.name}
              onChange={(v) => setAddress((a) => ({ ...a, name: v }))}
            />
            <div>
              <Input
                label="CEP"
                placeholder="00000-000"
                value={address.zip}
                onChange={(v) => setAddress((a) => ({ ...a, zip: v }))}
              />
              {loadingCep && (
                <p className="text-xs text-blue-600 mt-1">Buscando CEP...</p>
              )}
              {cepError && (
                <p className="text-xs text-red-600 mt-1">{cepError}</p>
              )}
            </div>
            <Input
              label="Rua"
              value={address.street}
              onChange={(v) => setAddress((a) => ({ ...a, street: v }))}
              disabled={loadingCep}
            />
            <Input
              label="Número"
              value={address.number}
              onChange={(v) => setAddress((a) => ({ ...a, number: v }))}
            />
            <Input
              label="Bairro"
              value={address.neighborhood}
              onChange={(v) => setAddress((a) => ({ ...a, neighborhood: v }))}
              disabled={loadingCep}
            />
            <Input
              label="Complemento (opcional)"
              value={address.complement ?? ""}
              onChange={(v) => setAddress((a) => ({ ...a, complement: v }))}
            />
            <Input
              label="Cidade"
              value={address.city}
              onChange={(v) => setAddress((a) => ({ ...a, city: v }))}
              disabled={loadingCep}
            />
            <Input
              label="Estado"
              value={address.state}
              onChange={(v) => setAddress((a) => ({ ...a, state: v }))}
              disabled={loadingCep}
            />
          </div>
          {!addressValid && (
            <p className="text-xs text-red-600 mt-2">
              Preencha todos os campos obrigatórios.
            </p>
          )}
        </section>

        {/* Pagamento */}
        <section className="rounded-xl border p-4 bg-white">
          <h2 className="font-semibold mb-3">Pagamento</h2>

          <div className="flex gap-3 mb-4">
            <Toggle
              value={payMethod}
              thisValue="card"
              onChange={setPayMethod}
              label="Cartão"
            />
            <Toggle
              value={payMethod}
              thisValue="pix"
              onChange={setPayMethod}
              label="PIX"
            />
            <Toggle
              value={payMethod}
              thisValue="boleto"
              onChange={setPayMethod}
              label="Boleto"
            />
          </div>

          {payMethod === "card" && (
            <div className="grid sm:grid-cols-2 gap-3">
              <Input
                label="Nome impresso no cartão"
                value={card.holder}
                onChange={(v) => setCard((c) => ({ ...c, holder: v }))}
              />
              <Input
                label="Número"
                placeholder="0000 0000 0000 0000"
                value={card.number}
                onChange={(v) => setCard((c) => ({ ...c, number: v }))}
              />
              <Input
                label="Validade (MM/AA)"
                placeholder="MM/AA"
                value={card.exp}
                onChange={(v) => {
                  // Remove non-digits
                  const cleaned = v.replace(/\D/g, '');
                  // Add the / after 2 digits if we have at least 2 digits
                  let formatted = cleaned;
                  if (cleaned.length >= 2) {
                    formatted = cleaned.slice(0, 2) + '/' + cleaned.slice(2);
                  }
                  // Limit to MM/AA format (5 characters)
                  formatted = formatted.slice(0, 5);
                  setCard((c) => ({ ...c, exp: formatted }));
                }}
              />
              <Input
                label="CVV"
                placeholder="000"
                value={card.cvv}
                onChange={(v) => setCard((c) => ({ ...c, cvv: v }))}
              />
            </div>
          )}

          {payMethod === "pix" && (
            <p className="text-sm text-slate-600">
              O QR Code será exibido após confirmar o pedido (mock).
            </p>
          )}

          {payMethod === "boleto" && (
            <div className="space-y-3">
              <Input
                label="CPF ou CNPJ"
                placeholder="000.000.000-00 ou 00.000.000/0000-00"
                value={cpfCnpj}
                onChange={(v) => setCpfCnpj(v)}
              />
              <p className="text-sm text-slate-600">
                O boleto será gerado após confirmar o pedido.
              </p>
            </div>
          )}

          {!paymentValid && (
            <p className="text-xs text-red-600 mt-2">
              Preencha os dados de pagamento corretamente.
            </p>
          )}
        </section>
      </div>

      {/* Coluna direita: Resumo */}
      <aside className="h-fit rounded-xl border p-4 bg-white">
        <h2 className="font-semibold mb-3">Resumo</h2>
        <div className="flex justify-between text-sm mb-1">
          <span>Subtotal</span>
          <span>{money(subtotal)}</span>
        </div>
        <div className="flex justify-between text-sm mb-3">
          <span>Frete</span>
          <span>{money(shipping)}</span>
        </div>
        <hr />
        <div className="flex justify-between font-semibold text-lg mt-3">
          <span>Total</span>
          <span>{money(total)}</span>
        </div>

        <button
          disabled={!canFinish || processing}
          onClick={finishOrder}
          className={`w-full mt-4 rounded-lg py-2.5 ${
            canFinish && !processing
              ? "bg-indigo-700 text-white hover:bg-indigo-800"
              : "bg-slate-200 text-slate-500 cursor-not-allowed"
          }`}
        >
          {processing ? "Processando..." : "Finalizar compra"}
        </button>

        {paymentError && (
          <p className="text-xs text-red-600 mt-2">{paymentError}</p>
        )}

        <p className="text-xs text-slate-500 mt-2">
          Ao finalizar, você concorda com nossos termos e condições.
        </p>
      </aside>
    </div>
  );
}

/* ------------------ pequenos componentes UI ------------------ */
function Input({
  label,
  value,
  onChange,
  placeholder,
  disabled,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  disabled?: boolean;
}) {
  return (
    <label className="text-sm">
      <span className="block text-slate-600 mb-1">{label}</span>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className={`w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-400 outline-none ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
      />
    </label>
  );
}

function Toggle({
  value,
  thisValue,
  onChange,
  label,
}: {
  value: PaymentMethod;
  thisValue: PaymentMethod;
  onChange: (v: PaymentMethod) => void;
  label: string;
}) {
  const active = value === thisValue;
  return (
    <button
      type="button"
      onClick={() => onChange(thisValue)}
      className={`px-3 py-1.5 rounded-full border ${
        active
          ? "border-indigo-600 text-indigo-700 bg-indigo-50"
          : "border-slate-200"
      }`}
    >
      {label}
    </button>
  );
}
